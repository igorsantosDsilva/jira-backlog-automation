# Jira Backlog Automation – AI Task Creation

Sistema inteligente de automação que transforma ideias (áudio ou texto) em tarefas estruturadas no Jira, sem necessidade de preenchimento manual.

---

## 🚀 Overview

Este projeto implementa um **bot inteligente no Telegram com IA Generativa**, responsável por capturar ideias em tempo real e convertê-las automaticamente em issues estruturadas no Jira.

O sistema foi projetado para eliminar etapas manuais de organização, seguindo boas práticas modernas de automação:

* Interface conversacional via **Telegram**
* Processamento inteligente com **Google Gemini AI**
* Integração automática com **Jira REST API**
* Padronização inteligente de tarefas (Desenvolvimento vs. Estudo)
* Suporte a áudio e texto como entrada

---

## 🧠 Problem Statement

Profissionais criativos frequentemente têm muitas ideias durante o dia de trabalho, mas enfrentam desafios significativos:

* **Dispersão de ideias**: Anotações em papéis, whatsapp, múltiplos places que se perdem
* **Falta de padronização**: Descrições inconsistentes que prejudicam a organização do backlog
* **Desperdício de tempo**: Horas gastas formatando e reorganizando tarefas manualmente ao invés de desenvolver
* **Baixa rastreabilidade**: Atividades não chegam até o Jira ou ficam incompletas

Este projeto resolve esses problemas através de:

* Captura rápida de ideias via **Telegram** (áudio ou texto)
* **Transformação automática** em tarefas estruturadas com IA
* **Padronização inteligente** seguindo modelos de Desenvolvimento ou Estudo
* **Integração direta** com o Jira, sem etapas intermediárias

Principais benefícios:

* ⏱️ Economia de tempo na organização de ideias
* 📋 Padronização automática de descrições
* 🎯 Melhor rastreabilidade de atividades
* 🧠 Foco em desenvolvimento, não em administração

---

## ⚙️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     TELEGRAM USER                           │
│                  (Audio or Text Input)                      │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
        ┌─────────────────────┐
        │   TELEGRAM BOT      │
        │   Webhook Receiver  │
        └────────┬────────────┘
                 │
                 ▼
        ┌──────────────────────────┐
        │   FASTAPI SERVER         │
        │   (app.py - Port 8000)   │
        └────────┬─────────────────┘
                 │
        ┌────────▼────────────────────┐
        │   REQUEST PROCESSING        │
        ├─────────────────────────────┤
        │ • Audio Download (if any)   │
        │ • Gemini Upload (if audio)  │
        └────────┬────────────────────┘
                 │
                 ▼
        ┌──────────────────────────────────┐
        │   GOOGLE GEMINI AI               │
        │   (ia_description.py)            │
        ├──────────────────────────────────┤
        │ • Smart Task Classification      │
        │ • Development vs. Study Model    │
        │ • JSON Structure Generation      │
        └────────┬───────────────────────┘
                 │
                 ▼
        ┌──────────────────────────┐
        │   JIRA API INTEGRATION   │
        │   (jira_issue.py)        │
        ├──────────────────────────┤
        │ • Issue Creation         │
        │ • Description Formatting │
        │ • Priority Assignment    │
        └────────┬──────────────────┘
                 │
                 ▼
        ┌─────────────────────┐
        │   JIRA BACKLOG      │
        │ (Structured Issues) │
        └─────────────────────┘
                 │
                 └──────────────────────┐
                                        ▼
                               ┌─────────────────────┐
                               │  TELEGRAM RESPONSE  │
                               │   (response_bot.py) │
                               │  (Success Feedback) │
                               └─────────────────────┘
```

---

## 🔄 Workflow & Stages

### 🔹 1. Message Capture (Telegram)

* Usuário envia **áudio** ou **texto** via Telegram Bot
* Webhook FastAPI recebe a requisição
* Sistema identifica tipo de entrada (voz ou mensagem)
* Se áudio: download automático do Telegram, upload para Gemini

---

### 🔹 2. AI Processing (Google Gemini)

Sistema inteligente com duplo modelo de classificação:

**Modelo A – Desenvolvimento**
* Implementação de código, pipelines, correção de bugs
* Estrutura: User Story + Acceptance Criteria + Definition of Done

**Modelo B – Estudo e Aprendizado**
* Aprendizagem de tecnologias, documentação, cursos
* Estrutura: Objective + Learning Plan + Acceptance Criteria

Saída estruturada em **JSON**:
```json
{
  "title": "Título da tarefa",
  "description": "Descrição formatada com os critérios",
  "type": "Tarefa",
  "priority": "High | Medium | Low"
}
```

---

### 🔹 3. Jira Integration

* Validação do JSON gerado pela IA
* Criação automática de **Issue** no Jira via REST API
* Mapeamento de campos:
  * `title` → Summary (campo principal)
  * `description` → Description (com formatação ADF)
  * `type` → Issue Type
  * `priority` → Priority

---

### 🔹 4. User Feedback

* Resposta automática no Telegram informando sucesso/erro
* Título da tarefa criada é retornado ao usuário
* Tratamento de exceções com mensagens amigáveis

---

## 🗂 Project Structure

```bash
jira-backlog-automation/
│
├── app.py                          # FastAPI Server & Webhook Handler
│
├── src/
│   ├── ia_description.py          # Google Gemini Integration
│   ├── jira_issue.py              # Jira REST API Integration
│   └── response_bot.py            # Telegram Response Handler
│
├── config/
│   └── .env                       # Environment Variables (git-ignored)
│
├── requirements.txt               # Python Dependencies
├── .gitignore
└── README.md
```

---

## 🛠 Tech Stack

* **Backend**: Python, FastAPI
* **AI/LLM**: Google Gemini 3.1 Flash Lite
* **Messaging**: Telegram Bot API
* **Project Management**: Jira REST API v3
* **HTTP Client**: requests, uvicorn

---

## 📊 Key Engineering Concepts

Este projeto demonstra na prática:

* **Webhook Architecture**: Integração com APIs externas assíncronas
* **Multi-API Integration**: Coordenação de 3+ serviços (Telegram, Gemini, Jira)
* **Prompt Engineering**: Design de prompts sofisticados para classificação de tarefas
* **Error Handling**: Tratamento robusto de exceções em fluxos distribuídos
* **JSON Processing**: Parsing e validação de dados estruturados
* **Authentication**: HTTPBasicAuth para APIs seguras
* **Logging**: Rastreamento detalhado de fluxos

---

## ⚙️ Setup & Configuration

### Pré-requisitos

```bash
Python 3.9+
Conta Telegram Bot (via @BotFather)
API Key Google Gemini
Conta Jira com acesso à API
```

### Instalação

1. **Clone o repositório**
   ```bash
   git clone https://github.com/seu-usuario/jira-backlog-automation.git
   cd jira-backlog-automation
   ```

2. **Crie ambiente virtual**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   # ou
   .venv\Scripts\activate     # Windows
   ```

3. **Instale dependências**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure variáveis de ambiente** (.env)
   ```env
   # Telegram
   TELEGRAM_TOKEN=seu_token_aqui
   
   # Google Gemini
   GEMINI_KEY=sua_chave_aqui
   
   # Jira
   JIRA_URL=https://seu-dominio.atlassian.net
   JIRA_EMAIL=seu_email@empresa.com
   JIRA_API_TOKEN=seu_token_aqui
   JIRA_PROJECT_KEY=PROJ
   ```

5. **Inicie o servidor**
   ```bash
   uvicorn app:app --host 0.0.0.0 --port 8000
   ```

6. **Configure webhook do Telegram**
   ```bash
   curl -X POST https://api.telegram.org/botSEU_TOKEN/setWebhook \
     -H "Content-Type: application/json" \
     -d '{"url": "https://seu-dominio.com/webhook"}'
   ```

---

## 📈 Usage Flow

1. **Enviar áudio ou mensagem** via Telegram Bot
2. **Aguardar processamento** (geralmente <5 segundos)
3. **Receber confirmação** no Telegram com título da tarefa criada
4. **Acessar Jira** para revisar e organizar na sprint

### Exemplo de Entrada

**Áudio**: *"Preciso criar um pipeline de integração com a API de produtos. Deve fazer GET dos dados, transformar em JSON e salvar no banco de dados..."*

**Resultado no Jira**:
```
Título: Implementar Pipeline de Integração com API de Produtos
Descrição: [Estruturada com User Story, Critérios de Aceitação, Definition of Done]
Tipo: Tarefa
Prioridade: High
```

---

## 🚀 Output & Impact

* ✅ Tarefas criadas automaticamente no Jira
* ✅ Descrições padronizadas e bem estruturadas
* ✅ Zero perda de ideias durante o dia
* ✅ Economia de 2-4 horas/semana em organização manual
* ✅ Backlog sempre atualizado e pronto para sprint planning

---

## 🔐 Security Notes

* ✅ Credenciais armazenadas em `.env` (git-ignored)
* ✅ HTTPBasicAuth para autenticação Jira
* ✅ Validação de estrutura JSON antes de enviar à Jira
* ✅ Logging detalhado para debugging

---

<div align="center">

**Desenvolvido por [@Igor Santos](https://www.linkedin.com/in/igor-santos-50791a227) 😁**

</div>