# ₿ Pipeline Bitcoin Agente IA ![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)

Sistema de coleta, armazenamento e visualização de dados do preço do Bitcoin, integrando agentes de IA e dashboard interativo.  
Este projeto foi criado para demonstrar automação de ETL (Extract, Transform, Load) com dados financeiros, uso de agentes inteligentes e visualização em tempo real.

## 🚀 Objetivo

Criar uma solução simples e modular que:

- Extraia dados do preço do Bitcoin de APIs públicas.
- Armazene os dados em banco de dados local (TinyDB) ou relacional (PostgreSQL).
- Permita consultas inteligentes via agentes de IA.
- Apresente os dados em dashboard interativo com estatísticas e gráficos.

## 🧩 Funcionalidades

### 🔄 Pipeline ETL
- Scripts para extração dos preços do Bitcoin via API da Coinbase.
- Transformação dos dados para estrutura padronizada.
- Armazenamento em banco local (db.json) ou PostgreSQL.

### 🤖 Agentes Inteligentes
- Consulta e manipulação de dados do banco via agentes IA (Groq, DuckDuckGo).
- Integração com ferramentas de busca e banco de dados.

### 📊 Dashboard Interativo
- Visualização dos dados coletados em tempo real.
- Gráficos de evolução do preço, estatísticas e lista completa dos registros.

### 🌐 Integração com APIs
- Exemplos de consumo de APIs externas (Coinbase, NASA).

## 🏗️ Estrutura do Projeto

```bash
PIPELINE-BITCOIN-AGENT-AI
├── .devcontainer/
│ └── devcontainer.json                         # Configuração para ambientes de desenvolvimento no VS Code com Dev Containers.
├── agents/
│ ├── bitcoin_agent.py                          # Agente IA com Groq e DuckDuckGo.
│ └── bitcoin_agent_postgres.py                 # Agente IA com integração ao PostgreSQL.
├── dashboard/
│ ├── dashboard_bitcoin_postgres_v1.py          # Dashboard Streamlit para visualização dos dados, versão 1.
│ ├── dashboard_bitcoin_postgres_v2.py          # Dashboard Streamlit para visualização dos dados, versão 2. Utilizada para deploy.
│ └── dashboard_bitcoin_postgres_v3.py          # Dashboard Streamlit para visualização dos dados, versão 3. Utilizada para testes local
├── pipeline/
│ ├── get_bitcoin_price.py                      # Extração simples do preço do Bitcoin.
│ ├── nasa_mars_photos.py                       # Consumo de API da NASA.
│ ├── consulta_preco_bitcoin_v1.py              # ETL básico do preço do Bitcoin.
│ ├── consulta_preco_bitcoin_v2_tinydb.py       # ETL com armazenamento em TinyDB.
│ └── consulta_preco_bitcoin_v3_postgres.py     # ETL completo com PostgreSQL e SQLAlchemy.
├── db.json                                     # Banco local TinyDB (você precisa criar um arquivo com esse nome para o tinydb funcionar).
├── .dockerignore                               # Arquivos ignorados no Docker.
├── Dockerfile                                  # Define a imagem Docker do projeto para deploy do agente ETL.
├── .env                                        # Variáveis de ambiente (aqui você coloca as keys, credenciais...).
├── .gitignore                                  # Arquivos ignorados no Git.
└── README.md                                   # Documentação do projeto.
```

## 🛠️ Tecnologias Utilizadas

- ![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python) – Linguagem principal do projeto.  
- ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white) – Dashboard interativo para visualização dos dados.  
- ![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-FFCA28?logo=python&logoColor=black) – ORM para integração com bancos de dados relacionais.  
- ![TinyDB](https://img.shields.io/badge/TinyDB-00BFFF?logo=python&logoColor=white) – Banco de dados NoSQL local e leve.  
- ![dotenv](https://img.shields.io/badge/dotenv-4E9A06?logo=python&logoColor=white) – Gerenciamento de variáveis de ambiente.  
- ![Requests](https://img.shields.io/badge/Requests-0052CC?logo=python&logoColor=white) – Consumo de APIs HTTP.  
- ![Pandas](https://img.shields.io/badge/Pandas-150458?logo=pandas&logoColor=white) – Manipulação e análise de dados.  
- ![Agno](https://img.shields.io/badge/Agno-000?logo=python&logoColor=white) – Framework para agentes de IA.

## 🧪 Como Rodar Localmente

1. Clone o repositório:

```bash
git clone https://github.com/vmellozk/pipeline-bitcoin-agent-ai.git
cd pipeline-bitcoin-agent-ai
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Configure o arquivo .env com suas credenciais (API keys, banco de dados).

4. Execute os scripts desejados:

- Para coletar dados e salvar no banco NoSQL local:
```bash
python pipeline/consulta_preco_bitcoin_v2.py
```

- Para coletar dados e salvar no PostgreSQL:
```bash
python pipeline/consulta_preco_bitcoin_v3_postgres.py
```

- Para visualizar o dashboard:
```bash
streamlit run dashboard/dashboard_bitcoin_postgres_v2.py
```

## 🧪 Como Fazer o Deploy de todo o Projeto

### Deploy do banco de dados (PostgreSQL) na Render

1. Acesse: [https://dashboard.render.com](https://dashboard.render.com)
2. Clique em **New > PostgreSQL**
3. Dê um nome ao banco e clique em **Create Database**
4. Aguarde alguns minutos até o banco estar disponível
5. Copie a connection string completa no campo **External Database URL**, algo como:  
   `postgresql://user:password@host/dbname`

> ⚠️ **Importante:**  
> O valor de `host` **não** é o que aparece no campo **Host** da Render.  
> Em vez disso, ele está localizado no campo **External Database URL**, a partir do caractere `@` até a primeira barra `/`.

**Exemplo:**  
Se o campo **External Database URL** for:
   `postgresql://dbname_****_user:***********@dpg-*******************-a.oregon-postgres.render.com/dbname_****`

Então o `host` é:
   `dpg-*******************-a.oregon-postgres.render.com`

6. Essa URL completa será usada como valor da variável de ambiente `DATABASE_KEY`

---

### Deploy do dashboard no Streamlit

1. Acesse: [https://share.streamlit.io](https://share.streamlit.io)
2. Crie um novo projeto apontando para o repositório do GitHub
3. No campo **Main file path**, insira o caminho correto do arquivo principal do app:
    `dashboard/dashboard_bitcoin_postgres_v2.py`
4. Depois vá em **Advanced settings** e adicione as variáveis de ambiente:
    `DATABASE_KEY=postgresql://user:password@host/dbname`

    > Exemplo:
    > `DATABASE_KEY=postgresql://dbname_****_user:***********@dpg-*******************-a.oregon-postgres.render.com/dbname_****`
    
5. O app será carregado automaticamente após isso

---

### Criar imagem Docker local (opcional para testes)

Caso deseje testar localmente o backend com Docker antes de fazer o deploy (recomendado):
```bash
docker build -t bitcoin-agent .
```

Se tudo estiver funcionando depois de testar:
```bash
docker ps     # para ver o ID ou nome do container
docker stop <id_ou_nome_do_container>
```

---

###  Deploy do backend com Railway

Instale a CLI do Railway:
```bash
npm install -g @railway/cli
```

Faça login:
```bash
railway login
```

Inicialize o projeto:
```bash
railway init
```

Acesse o projeto criado na [Railway](https://railway.com/dashboard) e vá na aba **Variables** para adicionar sua variável de ambiente:
```bash
DATABASE_KEY=postgresql://user:password@host/dbname
```

> Exemplo:
> `DATABASE_KEY=postgresql://dbname_****_user:***********@dpg-*******************-a.oregon-postgres.render.com/dbname_****`

Faça o deploy:
```bash
railway up
```

Pronto, agora todo o deploy está feito!

## 🤝 Contexto do Projeto
Este projeto foi desenvolvido para fins educacionais e demonstração de automação de coleta de dados financeiros, integração com agentes de IA e visualização interativa.
A proposta é servir como base para aplicações de monitoramento, análise e consulta inteligente de dados.

> ⚠️ Observação: O projeto é um protótipo. Certifique-se de configurar corretamente o banco de dados e as variáveis de ambiente para uso completo das funcionalidades.

## 📸 Prints

## 🔮 Possíveis Expansões

- Integração com mais fontes de dados (outras criptomoedas, APIs financeiras).
- Dashboard administrativo com filtros avançados.
- Notificações automáticas de variações de preço.
- API RESTful para consulta dos dados coletados.
- Sistema de autenticação para agentes e dashboards.

## 🤲 Como Contribuir

Pull requests são bem-vindos!
Sinta-se à vontade para abrir issues, sugerir melhorias ou colaborar com código.

1. Fork este repositório
2. Crie sua branch: git checkout -b minha-feature
3. Commit suas alterações: git commit -m 'feat: nova funcionalidade'
4. Push para a branch: git push origin minha-feature
5. Abra um Pull Request
