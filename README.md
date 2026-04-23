<div align="center">

<img src="https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
<img src="https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi&logoColor=white"/>
<img src="https://img.shields.io/badge/Next.js-Frontend-000000?style=for-the-badge&logo=nextdotjs&logoColor=white"/>
<img src="https://img.shields.io/badge/Focus-Phishing%20Risk%20Analysis-8E24AA?style=for-the-badge"/>
<img src="https://img.shields.io/badge/Version-MVP-00C853?style=for-the-badge"/>

<br/><br/>

# PhishRadar

**Analisador de risco para phishing, fraudes e mensagens suspeitas**

*Paste. Analyze. Explain.*

</div>

---

## O Problema

Mensagens de phishing costumam misturar urgencia, links suspeitos e pedidos de credenciais para pressionar usuarios.

| Problema | Impacto |
|---|---|
| Links encurtados escondem o destino real | Dificulta a avaliacao rapida |
| Linguagem urgente induz acao impulsiva | Aumenta risco de fraude |
| Dominios parecidos ou estranhos confundem usuarios | Facilita impersonacao |
| Pedidos de senha ou pagamento aparecem fora do fluxo normal | Pode levar a roubo de credenciais ou prejuizo financeiro |

---

## A Solucao

O **PhishRadar** recebe texto, URL ou conteudo bruto de e-mail e retorna uma analise simples, explicavel e deterministica.

O sistema entrega:

- `score`: pontuacao de risco de 0 a 100
- `label`: classificacao final (`LOW_RISK`, `SUSPICIOUS`, `HIGH_RISK`)
- `reasons`: sinais detectados que explicam a decisao

---

## Pipeline

```text
Conteudo -> API FastAPI -> Risk Engine -> Heuristicas -> Score -> Label -> Reasons -> UI Next.js
```

---

## Funcionalidades

### Analise de Conteudo

- entrada livre via textarea
- suporte a texto, URLs e conteudo bruto de e-mail
- resposta em tempo real pela interface web
- integracao entre frontend e backend via proxy server-side do Next.js

---

### Risk Engine Heuristico

Detecta sinais como:

- linguagem de urgencia
- encurtadores de URL
- padroes suspeitos de dominio
- pedidos de senha, credenciais ou pagamento

Cada categoria contribui no maximo uma vez por analise.

---

### Risk Scoring

| Score | Classificacao |
|---|---|
| 0-34 | LOW_RISK |
| 35-69 | SUSPICIOUS |
| 70+ | HIGH_RISK |

---

## Exemplo de Resultado

### Entrada

```text
Urgent: confirm your password at https://login-secure-account-update.example.com now.
```

### Saida

```json
{
  "score": 100,
  "label": "HIGH_RISK",
  "reasons": [
    "Message uses urgent language to pressure the recipient.",
    "Message contains a suspicious domain pattern.",
    "Message requests credentials or payment action."
  ]
}
```

---

## Stack

| Camada | Tecnologia |
|---|---|
| Backend | FastAPI, Pydantic |
| Risk Engine | Python, heuristicas deterministicas |
| Testes | pytest |
| Frontend | Next.js, React, TypeScript |
| Deploy Backend | Railway |
| Deploy Frontend | Vercel |

---

## Producao

- Frontend: https://phishradar.vercel.app
- Backend API: https://phishradar-production.up.railway.app

A rota proxy server-side do frontend usa `PHISHRADAR_API_BASE_URL` para apontar para o backend.

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

---

### Frontend

```bash
cd frontend
npm install
cp .env.example .env.local
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

---

## API

### Health Check

```http
GET /health
```

### Analyze

```http
POST /analyze
```

Body:

```json
{
  "content": "Urgent! Verify now"
}
```

Response:

```json
{
  "score": 25,
  "label": "LOW_RISK",
  "reasons": [
    "Message uses urgent language to pressure the recipient."
  ]
}
```

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
|-- frontend/
|   |-- app/
|   |   |-- api/analyze/route.ts
|   |   `-- page.tsx
|   |-- lib/
|   |   `-- phishradar-api.ts
|   `-- types/
|       `-- analysis.ts
|-- tests/
|-- docs/
|-- Procfile
`-- requirements.txt
```

---

## Screenshots

Espaco reservado para prints do projeto:

- tela inicial com formulario de analise
- resultado `LOW_RISK`
- resultado `HIGH_RISK`

---

## Limitacoes

- nao usa machine learning
- nao consulta fontes externas
- nao substitui analise humana em incidentes reais
- heuristicas ainda sao simples e focadas no MVP

---

## Roadmap

| Versao | Foco | Status |
|---|---|---|
| MVP | API, risk engine e UI web | Concluido |
| v1.1 | Mais regras de URL e dominio | Planejado |
| v1.2 | Analise de headers de e-mail | Planejado |
| v1.3 | Testes end-to-end | Planejado |
| v1.4 | Melhorias visuais e screenshots | Planejado |

---

## Objetivo

Demonstrar:

- desenvolvimento full stack com FastAPI e Next.js
- design de motor de risco simples e explicavel
- separacao entre API, regras de negocio e frontend
- deploy desacoplado entre backend e frontend
- boas praticas de testes e configuracao por variavel de ambiente

---

## Desenvolvedor

Jefferson Ferreira

- GitHub: [jeffersonferreira-ti](https://github.com/jeffersonferreira-ti)
- LinkedIn: [Jefferson Ferreira](https://www.linkedin.com/in/jefferson-ferreira-ti)

---

<div align="center">
  <sub>PhishRadar MVP - 2026</sub>
</div>
