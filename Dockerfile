# 1. Usar uma imagem base oficial do Python
FROM python:3.10-slim

# 2. Definir o diretório de trabalho dentro do container
WORKDIR /app

# 3. Definir variáveis de ambiente para Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 4. Instalar dependências do sistema (se necessário)
# RUN apt-get update && apt-get install -y ...

# 5. Instalar as dependências do Python
# Copia primeiro o requirements.txt para aproveitar o cache do Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copiar o código da aplicação para o container
COPY ./app /app/app

# 7. Expor a porta que o Uvicorn irá usar
EXPOSE 8000

# 8. Comando para iniciar a aplicação
# O host 0.0.0.0 é essencial para que a aplicação seja acessível de fora do container
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]