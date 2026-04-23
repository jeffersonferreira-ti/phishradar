# Arquitetura do PhishRadar

O PhishRadar foi projetado como um motor de detecção de phishing explicável, determinístico e fácil de evoluir. A arquitetura atual prioriza clareza de decisão: cada sinal de risco pode ser rastreado, pontuado, agrupado por camada e exposto ao consumidor final por meio de `label`, `reasons` e `breakdown`.

Este documento descreve como o Risk Engine v2 está estruturado e como o score final é produzido.

---

## Visão Geral

Em alto nível, o fluxo de análise segue esta sequência:

```text
Entrada textual -> Normalização -> Extração de URLs e domínios -> Avaliação por camadas
-> Agregação de score e reasons -> Breakdown por categoria -> Score final capado -> Label final
```

O motor roda hoje no backend FastAPI e serve tanto a API quanto as superfícies de consumo do projeto, como web app e extensão Chrome.

---

## Princípio de Design

### Explainability First

O princípio central do engine é explicabilidade.

Isso significa que:

- cada regra é determinística
- cada regra retorna uma razão legível
- cada regra contribui para uma categoria explícita de score
- a resposta final expõe não só o total, mas também a composição do risco

Na prática, o resultado de análise responde três perguntas importantes:

1. O conteúdo parece arriscado?
2. Quais sinais levaram a essa decisão?
3. Em que camada arquitetural esse risco se concentrou?

---

## Estrutura do Risk Engine

O engine principal está em [`app/analyzers/risk_engine.py`](/c:/Users/jluiz/Documents/GitHub/phishradar/app/analyzers/risk_engine.py).

As estruturas centrais são:

- `RiskAnalysis`: objeto final retornado ao chamador
- `RuleEvaluation`: shape normalizado para o resultado de cada regra
- `_evaluate_rules(...)`: orquestra a execução das regras
- `_build_analysis(...)`: consolida score, reasons, breakdown e label

Cada avaliador de regra segue o mesmo contrato:

- informa se houve match
- informa o score atribuído
- retorna uma razão textual
- aponta a categoria agregadora da regra

Esse formato mantém o engine simples de ler e simples de expandir.

---

## Pipeline de Análise

### 1. Normalização

Antes de avaliar sinais, o conteúdo é normalizado com:

- `casefold()` para reduzir diferenças de caixa
- `unicodedata.normalize("NFKD", ...)` para remover dependência de acentuação

Isso permite matching consistente para textos como:

- `Alfândega` -> `alfandega`
- `atualização cadastral` -> `atualizacao cadastral`

---

### 2. Extração Estrutural

O engine extrai:

- URLs presentes no conteúdo
- hostnames únicos
- domínios relevantes para análise estrutural

Essa etapa separa o que é análise semântica de conteúdo do que é análise técnica de URL e domínio.

---

### 3. Avaliação por Camadas

As regras são agrupadas em cinco camadas lógicas:

- `content`
- `url`
- `domain`
- `brand`
- `correlation`

Essas camadas não são apenas conceituais: elas também dirigem o `breakdown` final.

---

## Camadas de Análise

### 1. Content Layer

Esta camada avalia sinais presentes diretamente no texto analisado.

Exemplos atuais:

- linguagem de urgência
- pedidos de credenciais ou pagamento
- padrões narrativos de golpes brasileiros

Objetivo:

- capturar engenharia social explícita
- detectar fraude mesmo quando a URL isoladamente parece pouco suspeita

Categorias de breakdown:

- `content_score`

---

### 2. URL Layer

Esta camada analisa a estrutura da URL e seus componentes.

Exemplos atuais:

- URL shorteners
- palavras sensíveis em hostname, path, query ou fragment
- estrutura suspeita de path e parâmetros
- TLDs de maior risco em contexto sensível

Objetivo:

- identificar links com características comuns em phishing
- elevar score quando a URL carrega semântica de login, verificação, cobrança ou sessão

Categorias de breakdown:

- `url_score`

---

### 3. Domain Layer

Esta camada olha para o domínio como artefato estrutural.

Exemplos atuais:

- muitos hífens
- subdomínios em excesso
- labels longos ou artificiais
- labels com mistura suspeita de letras e números

Objetivo:

- capturar domínios construídos para parecer plausíveis, mas com traços típicos de fraude

Categorias de breakdown:

- `domain_score`

---

### 4. Brand Layer

Esta camada trata do abuso de marca em dois sentidos diferentes:

1. `brand lookalike`
   Detecta domínios que imitam marcas conhecidas com substituições visuais, como leetspeak.

2. `brand mismatch`
   Detecta quando o conteúdo menciona uma marca conhecida, mas os links presentes não pertencem aos domínios oficiais esperados.

Exemplo conceitual:

- o texto fala de `PayPal`
- a URL aponta para `secure-check.example.com`

Objetivo:

- capturar tentativas de impersonação que não dependem apenas de um domínio visualmente parecido

Categorias de breakdown:

- `brand_score`

---

### 5. Correlation Layer

Esta é a camada mais importante da evolução para o v2.

Em vez de tratar todos os sinais isoladamente, o engine agora reconhece combinações de sinais que aumentam a confiança de fraude.

Exemplos atuais:

- urgência + ação sensível
- shortener + ação sensível
- domínio suspeito + ação sensível

Objetivo:

- reduzir falsos negativos
- distinguir mensagens realmente perigosas de sinais fracos isolados

Categorias de breakdown:

- `correlation_score`

---

## Modelo de Scoring

O scoring é aditivo e determinístico.

Cada regra possui:

- uma condição de match
- um score fixo
- uma razão textual
- uma categoria de agregação

Exemplos de scores atuais:

- urgência: `10`
- URL shortener: `10`
- domínio suspeito: `18`
- credencial/pagamento: `20`
- brand mismatch: `30`
- golpe brasileiro especializado: `25`
- correlação urgência + ação sensível: `20`

O objetivo desse modelo não é simular probabilidade estatística, mas produzir uma classificação previsível, auditável e fácil de recalibrar.

---

## Thresholds e Labels

O score final é mapeado para quatro níveis:

| Faixa | Label |
|---|---|
| `0-19` | `LOW_RISK` |
| `20-44` | `MODERATE` |
| `45-69` | `SUSPICIOUS` |
| `70+` | `HIGH_RISK` |

O engine mantém `MAX_SCORE = 100`.

Se a soma bruta ultrapassar esse valor:

- o `score` final é capado em `100`
- o `breakdown` permanece bruto

Essa decisão é intencional: o cap evita números artificiais na resposta principal, enquanto o breakdown preserva valor diagnóstico para tuning e depuração.

---

## Breakdown System

O `breakdown` agrega o score bruto por família de sinais:

```json
{
  "content_score": 0,
  "url_score": 0,
  "domain_score": 0,
  "brand_score": 0,
  "correlation_score": 0
}
```

### Como funciona

Durante a agregação:

1. cada `RuleEvaluation` bem-sucedido adiciona seu `score` ao total bruto
2. o mesmo score é somado à categoria correspondente no `breakdown`
3. ao final, o total é capado, mas o breakdown não

### Por que isso importa

Esse sistema permite responder perguntas como:

- o risco veio mais do texto ou da URL?
- houve abuso de marca ou correlação multi-sinal?
- o score alto é resultado de várias regras fracas ou de poucos sinais fortes?

Isso torna o engine mais útil para:

- debugging
- tuning de score
- demonstração técnica
- apresentação de portfólio

---

## Contrato de Resposta

O objeto final de análise expõe:

- `score`
- `label`
- `reasons`
- `breakdown`

Exemplo simplificado:

```json
{
  "score": 75,
  "label": "HIGH_RISK",
  "reasons": [
    "URL appears to mimic a known brand name.",
    "Message mentions Paypal but linked URLs do not use its official domains."
  ],
  "breakdown": {
    "content_score": 0,
    "url_score": 20,
    "domain_score": 0,
    "brand_score": 55,
    "correlation_score": 0
  }
}
```

---

## Decisões Arquiteturais Relevantes

### Motor determinístico em vez de modelo opaco

Escolha:

- regras explícitas em Python

Motivação:

- previsibilidade
- facilidade de testes
- facilidade de ajuste fino
- melhor valor demonstrativo para engenharia

---

### Regras isoladas com shape comum

Escolha:

- cada avaliador retorna `RuleEvaluation`

Motivação:

- simplifica manutenção
- evita lógica implícita espalhada
- facilita adição de novas famílias de sinais

---

### Correlação como camada própria

Escolha:

- regras combinadas não substituem regras-base; elas são aditivas

Motivação:

- manter granularidade
- preservar explainability
- capturar cenários de fraude mais próximos do mundo real

---

### Breakdown separado do score final

Escolha:

- `score` capado, `breakdown` bruto

Motivação:

- leitura simples para o usuário final
- visibilidade diagnóstica para quem calibra o motor

---

## Leitura para Recrutadores e Engenheiros

Do ponto de vista de produto, o PhishRadar demonstra um sistema de segurança enxuto, mas com arquitetura clara de decisão.

Do ponto de vista técnico, ele mostra:

- separação de responsabilidades por camada
- contrato estável para regras
- scoring calibrável
- explainability incorporada ao design
- evolução do engine de sinais isolados para detecção híbrida e correlacionada

Essa combinação torna o projeto legível para recrutadores e defensável para engenheiros.
