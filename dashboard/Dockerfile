# Imagem oficial do Python
FROM python:3.13-slim

# Pasta dentro do container

WORKDIR /app

# Copiar o arquivo de dependências 

COPY requirements.txt .

# Instalar as bibliotecas

RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo o projeto para a pasta

COPY . .

# Permissão de execução do script

RUN chmod +x start.sh

# Porta utilizada pelo Flask

EXPOSE 5000

# Comando inicial

CMD ["bash", "./start.sh"]