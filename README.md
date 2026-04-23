<div align="center">

<img src="https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
<img src="https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi&logoColor=white"/>
<img src="https://img.shields.io/badge/Next.js-Frontend-000000?style=for-the-badge&logo=nextdotjs&logoColor=white"/>
<img src="https://img.shields.io/badge/Chrome%20Extension-MV3-4285F4?style=for-the-badge&logo=googlechrome&logoColor=white"/>
<img src="https://img.shields.io/badge/Focus-Phishing%20Risk%20Analysis-8E24AA?style=for-the-badge"/>
<img src="https://img.shields.io/badge/Status-M9%20Complete-00C853?style=for-the-badge"/>

<br/><br/>

# PhishRadar

**Ferramenta full stack para análise heurística de phishing, fraude e URLs suspeitas**

*Analyze. Explain. Prevent.*

</div>

---

## O Problema

Phishing continua explorando sinais simples, mas eficazes: urgência, links manipulados, domínios enganosos e pedidos indevidos de credenciais.

| Problema | Impacto |
|---|---|
| URLs suspeitas podem parecer legítimas à primeira vista | Aumenta a chance de clique indevido |
| Mensagens com urgência induzem ação impulsiva | Reduz a avaliação crítica do usuário |
| Domínios lookalike confundem marcas confiáveis com imitações | Facilita roubo de credenciais |
| Usuários nem sempre têm contexto técnico para avaliar risco | A decisão fica lenta ou imprecisa |

---

## A Solução

O **PhishRadar** entrega uma análise explicável e determinística de conteúdo suspeito via API, web app e extensão Chrome.

O sistema recebe texto, URL ou conteúdo bruto de e-mail e retorna:

- `score`: pontuação de risco de `0` a `100`
- `label`: classificação final (`LOW_RISK`, `SUSPICIOUS`, `HIGH_RISK`)
- `reasons`: sinais identificados que explicam a decisão

Além da análise manual, a extensão também executa análise automática da página ativa, atualiza badge dinamicamente e reutiliza cache por URL.

---

## Pipeline

```text
Texto/URL -> FastAPI /analyze -> Risk Engine Heurístico -> Score -> Label -> Reasons -> Web App / Chrome Extension
```

---

## Funcionalidades

### Backend e Risk Engine

- API FastAPI com rotas de health check e análise
- motor heurístico determinístico e explicável
- scoring por categorias com thresholds previsíveis
- resposta padronizada para todos os clientes

---

### Heurísticas de Risco

Detecta sinais como:

- linguagem de urgência
- encurtadores de URL
- padrões suspeitos de domínio
- pedidos de credenciais ou pagamento
- keywords suspeitas na URL
- TLDs de maior risco em contexto sensível
- brand lookalikes simples com substituições visuais
- estrutura suspeita de path e query params

Cada regra adiciona score de forma controlada e com motivo explícito no resultado.

---

### Web App

- interface em Next.js + TypeScript para análise manual
- integração com backend via rota server-side
- exibição clara de score, label e reasons
- tratamento simples de loading e erro

---

### Extensão Chrome

- análise manual da aba atual
- análise manual de texto ou URL colado
- análise automática ao trocar de página
- badge dinâmica baseada no risco retornado pela API
- cache por URL em `chrome.storage.local`

---

### Risk Scoring

| Score | Classificação |
|---|---|
| 0-34 | LOW_RISK |
| 35-69 | SUSPICIOUS |
| 70+ | HIGH_RISK |

---

## Caso de Uso

### Entrada

```text
Urgent: confirm your password at https://login-secure-account-update.example.com now.
```

### Saída

```json
{
  "score": 100,
  "label": "HIGH_RISK",
  "reasons": [
    "Message uses urgent language to pressure the recipient.",
    "Message contains a suspicious domain pattern.",
    "Message requests credentials or payment action.",
    "URL contains suspicious phishing-related keywords."
  ]
}
```

---

## Stack

| Camada | Tecnologia |
|---|---|
| Backend | FastAPI, Pydantic, Uvicorn |
| Risk Engine | Python, heurísticas determinísticas |
| Testes | pytest |
| Frontend | Next.js, React, TypeScript |
| Extensão | Chrome Extension, Manifest V3, JavaScript |
| Deploy | Railway e Vercel |

---

## Produção

- Web app: https://phishradar.vercel.app
- Backend API: https://phishradar-production.up.railway.app

---

## Como Rodar Localmente

### Backend

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend local:

```text
http://localhost:8000
```

Rotas principais:

- `GET /health`
- `POST /analyze`

---

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Configure `frontend/.env.local`:

```text
PHISHRADAR_API_BASE_URL=http://localhost:8000
```

Frontend local:

```text
http://localhost:3000
```

---

### Extensão Chrome

A extensão fica em [`extension/`](/c:/Users/jluiz/Documents/GitHub/phishradar/extension).

Para carregar localmente:

1. Acesse `chrome://extensions`
2. Ative `Developer mode`
3. Clique em `Load unpacked`
4. Selecione a pasta `extension/`

Comportamento atual:

- popup com análise manual
- leitura automática do resultado da URL ativa
- badge dinâmica por nível de risco
- cache local por URL

---

## Testes

### Backend

```bash
pytest
```

### Frontend

```bash
cd frontend
npm run typecheck
npm run build
```

### Extensão

Validação atual:

- carregamento local no Chrome
- checagem de sintaxe dos scripts

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

Espaço reservado para imagens do projeto:

- web app com formulário de análise
- resultado `LOW_RISK`
- resultado `HIGH_RISK`
- popup da extensão com análise automática
- badge da extensão nos estados `LOW_RISK`, `SUSPICIOUS` e `HIGH_RISK`

---

## Limitações

- não usa machine learning
- não consulta reputação externa
- não faz análise de histórico de navegação
- não substitui análise humana em contexto real de incidentes

---

## Roadmap

| Versão | Foco | Status |
|---|---|---|
| M1-M4 | Backend, engine inicial e API | Concluído |
| M5-M6 | Web app em Next.js | Concluído |
| M7-M9 | Extensão Chrome, automação, badge e cache | Concluído |
| Próximo | Screenshots, testes de integração e novos sinais de e-mail | Planejado |

---

## Objetivo

Demonstrar:

- desenvolvimento full stack com FastAPI e Next.js
- construção de um risk engine explicável e determinístico
- integração entre backend, frontend e extensão Chrome
- uso de Manifest V3 em um fluxo de análise automática
- deploy desacoplado entre Railway e Vercel

---

## Resumo do Projeto

O PhishRadar mostra como um produto de segurança enxuto pode combinar regras heurísticas, API bem definida e múltiplas interfaces sem depender de serviços externos ou modelos complexos.

O resultado é um MVP funcional, testável e claro para portfólio técnico.

---

## 👨‍💻Desenvolvido por **Jefferson Ferreira**.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=flat&logo=linkedin)](https://www.linkedin.com/in/jefferson-ferreira-ti/)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-181717?style=flat&logo=github)](https://github.com/jeffersonferreira-ti)

---

<div align="center">
  <sub>PhishRadar · 2026</sub>
</div>
