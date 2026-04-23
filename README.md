<div align="center">

<img src="https://img.shields.io/badge/version-2.0-blue?style=for-the-badge"/>
<img src="https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
<img src="https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi&logoColor=white"/>
<img src="https://img.shields.io/badge/Next.js-Frontend-000000?style=for-the-badge&logo=nextdotjs&logoColor=white"/>
<img src="https://img.shields.io/badge/Chrome%20Extension-MV3-4285F4?style=for-the-badge&logo=googlechrome&logoColor=white"/>
<img src="https://img.shields.io/badge/Focus-Phishing%20Detection%20Engine-8E24AA?style=for-the-badge"/>
<img src="https://img.shields.io/badge/Status-v2.0%20Engine-00C853?style=for-the-badge"/>

<br/>

# 🛡️ PhishRadar

<div align="center">
Analyze. Explain. Prevent.
</div>

**Plataforma de deteccao de phishing com scoring explicavel e correlacao de sinais em tempo real**

</div>
---

## Visao Geral do Projeto

O PhishRadar e uma plataforma de deteccao de phishing baseada em scoring explicavel e correlacao de sinais. O que comecou como um analisador heuristico simples evoluiu para um mecanismo mais robusto, capaz de combinar sinais de conteudo, estrutura de URL, caracteristicas de dominio, abuso de marca e correlation rules.

A plataforma retorna uma avaliacao deterministica de risco pensada para depuracao, calibracao e apresentacao de produto:

- `score`: pontuacao final de risco de `0` a `100`
- `label`: classificacao final (`LOW_RISK`, `MODERATE`, `SUSPICIOUS`, `HIGH_RISK`)
- `reasons`: explicacoes legiveis dos sinais detectados
- `breakdown`: atribuicao de score por categoria para explainability

O PhishRadar e exposto por um backend FastAPI, uma interface web em Next.js e uma extensao Chrome capaz de analisar a pagina ativa e refletir o risco por meio de badge.

---

## Principais Recursos

### Detection Engine

- scoring de phishing deterministico e explicavel
- deteccao hibrida em conteudo, URLs, dominios, sinais de marca e correlation rules
- calibracao aprimorada com modelo de quatro niveis de risco
- breakdown por categoria para depuracao e tuning
- cobertura focada em cenarios reais de phishing e golpes

---

### Explainability

- `reasons` explicitas para cada sinal acionado
- `breakdown` estruturado por familia de score:
  - `content_score`
  - `url_score`
  - `domain_score`
  - `brand_score`
  - `correlation_score`
- saida estavel e facil de inspecionar em testes, demos e apresentacoes de portfolio

---

### Superficies de Uso

- API FastAPI para integracao programatica
- web app em Next.js para analise manual
- extensao Chrome com feedback de risco por badge e cache de resultados por URL

---

## Como Funciona

```text
Texto/URL -> FastAPI /analyze -> risk engine -> Sinais base + correlation rules -> Score + Label + Reasons + Breakdown -> Web App / Chrome Extension
```

Fluxo do engine em alto nivel:

1. Normaliza o conteudo e extrai URLs e dominios.
2. Avalia regras base em conteudo, URL, dominio e sinais de marca.
3. Aplica correlation rules quando sinais arriscados aparecem em conjunto.
4. Agrega os totais brutos por categoria e produz o score final, com cap em `MAX_SCORE = 100`.
5. Retorna o label final, os motivos acionados e o breakdown do score.

---

## Explicacao dos Niveis de Risco

| Score | Label | Significado |
|---|---|---|
| 0-19 | `LOW_RISK` | Nenhum indicador relevante de phishing ou apenas sinais isolados fracos |
| 20-44 | `MODERATE` | Comportamento suspeito suficiente para revisao |
| 45-69 | `SUSPICIOUS` | Presenca de caracteristicas de phishing em multiplos sinais |
| 70+ | `HIGH_RISK` | Indicadores fortes ou correlacionados com alta confianca |

O score final e capado em `100`. O breakdown permanece bruto por categoria para permitir calibracao e leitura diagnostica do total.

---

## Capacidades de Deteccao

O PhishRadar cobre hoje um conjunto pratico de cenarios de phishing e golpe, incluindo:

- linguagem de urgencia e pressao
- pedidos de credenciais ou pagamento
- URL shorteners em contexto suspeito
- caracteristicas suspeitas de dominio e estruturas arriscadas de URL
- palavras sensiveis em URL e uso de TLDs de maior risco
- dominios lookalike com substituicoes visuais
- brand mismatch entre o conteudo da mensagem e os dominios linkados
- regras aditivas de correlacao, como:
  - urgencia + acao sensivel
  - shortener + acao sensivel
  - dominio suspeito + acao sensivel
- narrativas de golpes brasileiros envolvendo:
  - entrega retida
  - taxa pendente
  - alfandega e Correios
  - PIX para liberacao
  - atualizacao cadastral e confirmacao de dispositivo

Isso torna o engine util para cenarios reais como phishing de pagamento, tentativa de takeover de conta, falso aviso de entrega, impersonacao de dominio e ataques de engenharia social com sinais mistos.

---

## Exemplo de Resposta da API

### Entrada

```text
Urgent PayPal notice: entrega retida. Confirm your password at https://bit.ly/login now.
```

### Saida

```json
{
  "score": 100,
  "label": "HIGH_RISK",
  "reasons": [
    "Message uses urgent language to pressure the recipient.",
    "Message requests credentials or payment action.",
    "Content matches common Brazilian delivery, fee, or payment scam patterns.",
    "Message contains a URL shortening service.",
    "URL contains suspicious phishing-related keywords.",
    "URL structure includes suspicious phishing-related patterns.",
    "Message mentions Paypal but linked URLs do not use its official domains.",
    "Urgent language is combined with a sensitive action request.",
    "A URL shortener is combined with a sensitive action signal."
  ],
  "breakdown": {
    "content_score": 55,
    "url_score": 30,
    "domain_score": 0,
    "brand_score": 30,
    "correlation_score": 40
  }
}
```

---

## Tech Stack

| Camada | Tecnologia |
|---|---|
| Backend API | FastAPI, Pydantic, Uvicorn |
| Risk Engine | Python, regras deterministicas de scoring |
| Testes | pytest |
| Frontend | Next.js, React, TypeScript |
| Extensao | Chrome Extension, Manifest V3, JavaScript |
| Deploy | Railway, Vercel |

---

## Producao

- Web app: https://phishradar.vercel.app
- Backend API: https://phishradar-production.up.railway.app

---

## Arquitetura

```text
phishradar/
|-- app/
|   |-- analyzers/
|   |   `-- risk_engine.py
|   |-- api/
|   |   `-- routes/
|   |       |-- analyze.py
|   |       `-- health.py
|   |-- schemas/
|   |   `-- analyze.py
|   `-- main.py
|-- extension/
|   |-- background.js
|   |-- manifest.json
|   |-- popup.html
|   |-- popup.css
|   `-- popup.js
|-- frontend/
|   |-- app/
|   |   |-- api/analyze/route.ts
|   |   `-- page.tsx
|   |-- lib/
|   |   `-- phishradar-api.ts
|   `-- types/
|       `-- analysis.ts
|-- tests/
|   `-- test_risk_engine.py
|-- docs/
|-- Procfile
`-- requirements.txt
```

---

## Screenshots

Espaco reservado para visuais de portfolio:

- formulario de analise no web app
- resultado `LOW_RISK`
- resultados `MODERATE` e `HIGH_RISK`
- popup da extensao com analise automatica
- badge da extensao em multiplos niveis de risco

---

## Limitacoes

- nao usa machine learning nem reputation feeds
- nao consulta threat intelligence externa
- ainda nao possui pipeline nativo de parsing de e-mail
- nao realiza analise comportamental ou historica de navegacao
- nao substitui revisao humana em contexto real de incident response

---

## Roadmap

| Versao | Foco | Status |
|---|---|---|
| M1-M4 | Backend inicial, API e motor de regras | Concluido |
| M5-M6 | Interface web em Next.js | Concluido |
| M7-M9 | Extensao Chrome, badge e cache | Concluido |
| Atual | Correlacao, calibracao, brand mismatch, cobertura BR e breakdown explicavel | Concluido |
| Proximo | Novos sinais de e-mail, melhor visualizacao e ampliacao de cenarios | Planejado |

---

## Objetivo

O PhishRadar demonstra:

- engenharia backend orientada a seguranca com FastAPI
- construcao de um phishing detection engine explicavel
- evolucao de regras com calibracao e testes de regressao
- integracao entre API, aplicacao web e extensao Chrome
- ferramental de seguranca com valor tecnico e de portfolio

---

## Resumo do Projeto

O PhishRadar mostra como um produto enxuto de seguranca pode evoluir alem de heuristicas basicas e chegar a um motor de deteccao de phishing mais maduro, sem depender de modelos opacos.

O resultado e um sistema pratico que prioriza explainability, clareza de engenharia e cobertura de cenarios reais. Cada sinal importante de risco pode ser observado, atribuido e testado.

---

## Desenvolvido por **Jefferson Ferreira**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=flat&logo=linkedin)](https://www.linkedin.com/in/jefferson-ferreira-ti/)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-181717?style=flat&logo=github)](https://github.com/jeffersonferreira-ti)

---

<div align="center">
  <sub>PhishRadar · 2026</sub>
</div>
