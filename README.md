# UrbanXP Backend

Backend para o projeto UrbanXP, um concierge inteligente de experiências e roteiros.

## Como Iniciar (com Docker)

Este projeto é totalmente containerizado, então a única dependência que você precisa na sua máquina é o **Docker** e o **Docker Compose**.

1.  **Clone o repositório:**
    ```bash
    git clone [URL_DO_SEU_REPOSITORIO]
    cd urbanxp_backend
    ```

2.  **Configure as variáveis de ambiente:**
    -   Copie o arquivo `.env.example` para `.env`.
    -   ```bash
        cp .env.example .env
        ```
    -   O arquivo `.env` já vem pré-configurado para o ambiente Docker. Se desejar, altere a `JWT_SECRET_KEY` para um valor mais seguro.

3.  **Construa e suba os containers:**
    -   Este comando irá construir a imagem da sua API, baixar as imagens do Postgres e Redis, e iniciar todos os serviços em background.
    -   ```bash
        docker-compose up -d --build
        ```

4.  **Acesse a documentação da API:**
    -   A API agora está rodando e acessível na sua máquina local.
    -   Abra seu navegador em [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) para ver a documentação interativa (Swagger UI).
    -   Ou acesse [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc) para a documentação ReDoc.

## Comandos Úteis do Docker Compose

-   **Parar os containers:**
    ```bash
    docker-compose down
    ```

-   **Ver os logs da aplicação em tempo real:**
    ```bash
    docker-compose logs -f api
    ```

-   **Acessar o shell dentro do container da API (para debug):**
    ```bash
    docker-compose exec api bash
    ```

## Executando Migrações (Alembic)

(Instruções a serem adicionadas após configurar o Alembic)