# Usa uma imagem leve do Python
FROM python:3.11-slim

# Define diretório de trabalho
WORKDIR /app

# Copia arquivos
COPY . .

# Instala dependências
RUN pip install --no-cache-dir -r requirements.txt

# Expõe porta (não necessário aqui, mas é padrão)
EXPOSE 8080

# Comando para rodar o script
CMD ["python", "pipeline/consulta_preco_bitcoin_v3_postgres.py"]
