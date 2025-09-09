# Workout API

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.116.1-009688?style=for-the-badge&logo=fastapi)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-D71F00?style=for-the-badge&logo=sqlalchemy)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-11-336791?style=for-the-badge&logo=postgresql)
![Docker](https://img.shields.io/badge/Docker-blue?style=for-the-badge&logo=docker)

API para gerenciamento de atletas, categorias e centros de treinamento, desenvolvida com FastAPI e SQLAlchemy.

## 📋 Índice

- [Funcionalidades](#-funcionalidades)
- [Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Configuração do Ambiente](#-configuração-do-ambiente)
- [Como Executar](#-como-executar)
- [Comandos Úteis (Makefile)](#-comandos-úteis-makefile)
- [Endpoints da API](#-endpoints-da-api)

## ✨ Funcionalidades

- CRUD completo para Atletas, Categorias e Centros de Treinamento.
- Busca de atletas por `nome` e `CPF` via query parameters.
- Paginação (`limit`/`offset`) em listagens.
- Respostas customizadas para listagem de atletas, retornando apenas campos essenciais.
- Tratamento de exceções de integridade de dados (ex: CPF/CNPJ duplicado).
- Migrações de banco de dados gerenciadas com Alembic.

## 🚀 Tecnologias Utilizadas

- **Python 3.12**
- **FastAPI**: Framework web para construção da API.
- **Pydantic**: Para validação e serialização de dados.
- **SQLAlchemy**: ORM para interação com o banco de dados de forma assíncrona.
- **Alembic**: Para gerenciamento de migrações do schema do banco de dados.
- **PostgreSQL**: Banco de dados relacional.
- **Docker**: Para containerização do banco de dados.
- **Uvicorn**: Servidor ASGI para rodar a aplicação.
- **fastapi-pagination**: Biblioteca para facilitar a implementação de paginação.

## 📁 Estrutura do Projeto

```
workout-api/
├── alembic/                  # Configurações e versões do Alembic
├── workout_api/
│   ├── athlete/              # Módulo de Atletas (controller, model, schema)
│   ├── category/             # Módulo de Categorias
│   ├── training_center/      # Módulo de Centros de Treinamento
│   ├── configs/              # Configurações de banco de dados e settings
│   ├── contrib/              # Componentes compartilhados (BaseModel, BaseSchema, etc.)
│   ├── main.py               # Ponto de entrada da aplicação FastAPI
│   └── routers.py            # Roteador principal da API
├── alembic.ini               # Arquivo de configuração do Alembic
├── docker-compose.yaml       # Arquivo para subir o container do PostgreSQL
├── makefile.mk               # Atalhos para comandos comuns
└── requeriments.txt          # Dependências do projeto
```

## ⚙️ Configuração do Ambiente

Siga os passos abaixo para configurar o ambiente de desenvolvimento.

### 1. Clone o Repositório

```bash
git clone https://github.com/HellenIwata/bootcamp-santander-2025.git
cd workout-api
```

### 2. Crie e Ative um Ambiente Virtual

```bash
# Linux/macOS
python3 -m venv .venv
source .venv/bin/activate

# Windows
python -m venv .venv
.venv\Scripts\activate
```

### 3. Instale as Dependências

```bash
pip install -r requeriments.txt
```

### 4. Inicie o Banco de Dados com Docker

Certifique-se de ter o Docker e o Docker Compose instalados.

```bash
docker-compose up -d
```

### 5. Aplique as Migrações do Banco de Dados

Use o Makefile para aplicar as migrações e criar as tabelas.

```bash
make run-migrations
```

## ▶️ Como Executar

Para iniciar o servidor da API, execute o seguinte comando:

```bash
make run
```

A API estará disponível em `http://127.0.0.1:8000`.

A documentação interativa (Swagger UI) pode ser acessada em `http://127.0.0.1:8000/docs`.

## 🛠️ Comandos Úteis (Makefile)

- `make run`: Inicia o servidor de desenvolvimento com auto-reload.
- `make run-migrations`: Aplica todas as migrações pendentes no banco de dados.
- `make create-migrations d="<sua_mensagem>"`: Gera um novo arquivo de migração com base nas alterações dos models.

## 🌐 Endpoints da API

### Atletas (`/athletes`)

- `POST /`: Cria um novo atleta.
- `GET /`: Lista todos os atletas com filtros (`name`, `document`) e paginação (`page`, `size`).
- `GET /{athlete_id}`: Busca um atleta pelo ID.
- `GET /document/{athlete_document}`: Busca um atleta pelo CPF.
- `PATCH /{athlete_id}`: Atualiza os dados de um atleta.

### Categorias (`/categories`)

- `POST /`: Cria uma nova categoria.
- `GET /`: Lista todas as categorias.
- `GET /{category_id}`: Busca uma categoria pelo ID.

### Centros de Treinamento (`/training-centers`)

- `POST /`: Cria um novo centro de treinamento.
- `GET /`: Lista todos os centros de treinamento.
- `GET /{training_center_id}`: Busca um centro de treinamento pelo ID.