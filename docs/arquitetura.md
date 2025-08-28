## **Documento de Arquitetura de Backend – UrbanXP (MVP)**

### 1. Visão Geral e Objetivos da Arquitetura

O objetivo desta arquitetura é suportar as funcionalidades do MVP do UrbanXP, focando em:
* **Velocidade de Desenvolvimento:** Permitir que o produto seja construído e iterado rapidamente.
* **Baixo Custo Operacional:** Utilizar serviços com camadas gratuitas ou de baixo custo, ideais para um projeto em estágio inicial.
* **Performance:** Garantir que a experiência do usuário seja fluida, especialmente na geração de recomendações (< 2 segundos).
* **Escalabilidade Futura:** Construir uma base sólida que não precise ser totalmente refeita quando o aplicativo crescer para novas cidades e funcionalidades.

### 2. Arquitetura Proposta: Monólito Modular com FastAPI

Para o MVP, a arquitetura ideal é um **Monólito Modular**.

* **Monólito:** Todas as funcionalidades (usuários, grupos, recomendações, etc.) residem em uma única base de código e são implantadas como uma única aplicação. Isso simplifica drasticamente o desenvolvimento, os testes e o deploy na fase inicial.
* **Modular:** O código será organizado em módulos de domínio claros (ex: um módulo para `autenticação`, um para `grupos`, um para `lugares`). Essa organização torna o código mais fácil de manter e, crucialmente, permite que, no futuro, um módulo específico (como o de `recomendações`) possa ser extraído e transformado em um microsserviço sem reescrever tudo.

### 3. Stack de Tecnologia Sugerida

Com base na sua preferência por Python e na necessidade de performance, a seguinte stack é recomendada:

* **Linguagem:** **Python 3.10+**
* **Framework:** **FastAPI**
    * **Justificativa:** É a escolha perfeita para este projeto. É extremamente rápido, seu suporte a operações **assíncronas (`async/await`)** é fundamental para lidar com múltiplas chamadas a APIs externas (Google, Sympla, etc.) sem bloquear o servidor, e ele gera documentação de API interativa (Swagger UI) automaticamente, o que acelera o desenvolvimento do frontend.
* **Banco de Dados:** **PostgreSQL (com a extensão PostGIS)**
    * **Justificativa:** PostgreSQL é um banco de dados relacional robusto e confiável. A extensão **PostGIS é essencial e inegociável** para um aplicativo como o UrbanXP, pois oferece suporte nativo a consultas geoespaciais (ex: "encontrar todos os bares a menos de 2km de um ponto", "lugares dentro de uma área").
* **ORM / Validação:** **SQLAlchemy 2.0** (para suporte assíncrono) com **Alembic** (para migrações de banco de dados) e **Pydantic** (integrado nativamente no FastAPI para validação de dados).
* **Cache:** **Redis**
    * **Justificativa:** Será usado para armazenar em cache os resultados de APIs externas (evitando chamadas repetidas e caras ao Google Maps) e para dados de sessão, melhorando a performance geral.
* **Tarefas em Background (Background Jobs):** **Celery com Redis ou RabbitMQ**
    * **Justificativa:** Essencial para tarefas que não devem bloquear a resposta ao usuário, como:
        * Enviar notificações push após uma votação.
        * Atualizar os dados de um lugar a partir de uma API externa.

### 4. Modelagem de Dados (Schema de Alto Nível)

O banco de dados PostgreSQL terá as seguintes tabelas principais:

* `users`: (id, nome, email, hash_senha, dt_nascimento, cidade, social_provider, social_id)
* `friendships`: (user_id_1, user_id_2, status)
* `groups`: (id, nome, owner_id)
* `group_members`: (group_id, user_id, role)
* `places`: (id, **google_place_id**, nome, endereço, **geom** (campo PostGIS), faixa_preço, fotos, cardapio_url, etc.) -> *Armazena dados dos lugares*.
* `events`: (id, **sympla_event_id**, nome, local, data_hora, link_ingressos, etc.) -> *Armazena dados de eventos*.
* `recommendation_sessions`: (id, group_id, status) -> *Controla uma "rodada" de sugestões*.
* `suggested_routes`: (id, session_id, route_details_json) -> *Armazena um dos 3 roteiros sugeridos*.
* `votes`: (id, route_id, user_id, **guest_identifier**, rank) -> *O campo `guest_identifier` permite que não-usuários votem*.

### 5. Design da API (RESTful)

A comunicação entre o app e o backend será feita via uma API RESTful.

* **Autenticação:** **JWT (JSON Web Tokens)**.
    * **Fluxo:**
        1.  O usuário faz login (via social ou email/senha).
        2.  O backend retorna um `access_token` e um `refresh_token`.
        3.  O app envia o `access_token` no cabeçalho `Authorization: Bearer <token>` em todas as requisições protegidas.
* **Endpoints Principais do MVP:**
    * `POST /v1/auth/register`
    * `POST /v1/auth/login`
    * `POST /v1/auth/google`
    * `GET /v1/users/me`
    * `GET, POST /v1/groups`
    * `POST /v1/groups/{group_id}/invite`
    * `POST /v1/recommendations/` (Corpo da requisição: `{ "group_id": 123, "filters": {...} }`)
    * `GET /v1/recommendations/{session_id}`
    * `POST /v1/votes/` (Corpo: `{ "session_id": 456, "ranked_routes": [...] }`)
    * `GET /v1/places/search?lat=...&lon=...&radius=...`

### 6. Estratégia de Coleta e Gerenciamento de Dados

Esta é a parte mais complexa e crucial para o modelo de negócios.

1.  **Ingestão Híbrida:**
    * Quando o usuário busca por lugares, o backend primeiro consulta o **banco de dados local (PostgreSQL)**.
    * Se o dado não existe ou está desatualizado (ex: a última verificação foi há mais de 7 dias), uma **tarefa em background (Celery)** é disparada para buscar os dados mais recentes da API do Google Places e/ou outra fonte.
    * O resultado da API externa é usado para **criar ou atualizar** o registro no nosso banco de dados.
    * **Benefício:** Isso cria um cache persistente, reduzindo drasticamente os custos com APIs e a latência para buscas futuras na mesma região.

2.  **Enriquecimento de Dados por Parceiros:**
    * O modelo da tabela `places` terá campos que podem ser gerenciados por parceiros premium (ex: `promotions`, `is_highlighted`, `custom_photos`).
    * O algoritmo de recomendação dará um **peso maior** a lugares que são de parceiros premium, implementando o modelo de negócio diretamente na lógica.

### 7. Infraestrutura e Deploy (Foco em Custo Zero/Baixo no Início)

Para começar sem custos elevados, a melhor abordagem é usar uma **PaaS (Platform as a Service)**.

* **Plataforma Sugerida:** **Railway** ou **Render**.
    * **Justificativa:** Ambas são plataformas modernas, mais fáceis de usar que o Heroku e com planos gratuitos generosos que incluem o deploy da aplicação FastAPI, um banco de dados PostgreSQL e um cache Redis. Elas se integram diretamente ao seu repositório no GitHub para deploy contínuo (CI/CD).
* **Processo de Deploy:**
    1.  Crie o projeto no Railway/Render.
    2.  Conecte ao seu repositório do GitHub.
    3.  Adicione os serviços: "Python App", "PostgreSQL", "Redis".
    4.  Configure as variáveis de ambiente (chaves de API, segredos do banco de dados).
    5.  A cada `git push` na branch principal, a plataforma automaticamente faz o build e o deploy da nova versão.

### 8. Próximos Passos e Escalabilidade

Esta arquitetura foi projetada para crescer:

* **Novas Cidades:** O uso do PostGIS e uma boa modelagem de dados permitem a expansão para outras cidades simplesmente adicionando novos dados geográficos, sem alteração na arquitetura.
* **IA e NLP:** Quando a funcionalidade de busca por linguagem natural for implementada, o módulo de `recomendações` pode ser refatorado para chamar um serviço externo de IA (como a API da OpenAI) ou se tornar um microsserviço dedicado com modelos de ML próprios.
* **Aumento de Carga:** A plataforma PaaS (Railway/Render) permite escalar os recursos (CPU, RAM) com apenas alguns cliques. Quando o faturamento justificar, a migração para uma infraestrutura mais robusta como **AWS (ECS/Fargate)** ou **Google Cloud (Cloud Run)** será um passo natural e facilitado pela arquitetura modular.

### 9. Esqueleto sugerido

```
urbanxp_backend/
├── app/
│   ├── __init__.py
│   ├── main.py                   # Ponto de entrada da aplicação FastAPI
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── api.py            # Agregador de rotas da v1
│   │       └── endpoints/
│   │           ├── __init__.py
│   │           ├── auth.py       # Endpoints de autenticação
│   │           ├── groups.py     # Endpoints de grupos
│   │           └── places.py     # Endpoints de lugares/eventos
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py             # Gerenciamento de configurações e variáveis de ambiente
│   ├── db/
│   │   ├── __init__.py
│   │   ├── base.py               # Base para os modelos SQLAlchemy
│   │   └── session.py            # Configuração da sessão do banco de dados
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── group.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── token.py              # Schemas para JWT
│   │   └── user.py
│   └── services/
│       ├── __init__.py
│       └── recommendation_service.py # Lógica de negócio para recomendações
├── tests/
│   └── __init__.py
├── .env.example                  # Arquivo de exemplo para variáveis de ambiente
├── .gitignore
├── README.md
└── requirements.txt
```