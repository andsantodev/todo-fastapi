# API de Gerenciamento de Tarefas (FastAPI)

Este projeto é uma API RESTful desenvolvida com **Python + FastAPI** para gerenciar tarefas (to-do list).  
Inclui autenticação simples via token e persistência de dados com PostgreSQL.

---

## 🚀 Como executar

### Pré-requisitos:
- Docker + Docker Compose instalados

### Passos:

1. Clone o repositório e entre na pasta:
  bash
  git clone <repo-url>
  cd todo-fast

2. Crie o arquivo .env com o seguinte conteúdo:
  DATABASE_URL=postgresql://user:password@db:5432/todo_db
  TOKEN=meu-token-secreto

3. Suba o ambiente com Docker:
  docker compose up --build

4. Acesse:
  • Swagger: http://localhost:8000/docs
  • Adminer: http://localhost:8080

---

## 🔐 Autenticação

- Todas as rotas exigem autenticação via header:
  Authorization: Bearer meu-token-secreto

- No Swagger, clique em Authorize e insira:
  Bearer meu-token-secreto

---

## 📌 Endpoints
  • POST /tarefas – Criar nova tarefa
  • GET /tarefas – Listar tarefas (opcional: ?concluida=true|false)
  • PUT /tarefas/{id} – Atualizar título e descrição
  • PATCH /tarefas/{id}/concluir – Marcar como concluída
  • DELETE /tarefas/{id} – Deletar tarefa

---

## 🛠️ Tecnologias utilizadas
  • FastAPI
  • Pydantic
  • SQLAlchemy
  • PostgreSQL
  • Docker & Docker Compose
