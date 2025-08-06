import streamlit as st
from sqlalchemy import create_engine
import pandas as pd
import os
from dotenv import load_dotenv
import altair as alt

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Lê a variável DATABASE_URL
DATABASE_URL = os.getenv("DATABASE_KEY")

# Crie o engine SQLAlchemy
engine = create_engine(DATABASE_URL)

# Lê os dados do banco PostgreSQL e retorna como DataFrame
def ler_dados_postgres():
    try:
        query = "SELECT * FROM bitcoin_dados ORDER BY timestamp DESC"
        df = pd.read_sql(query, engine)
        return df
    except Exception as e:
        st.error(f"Erro ao conectar no PostgreSQL: {e}")
        return pd.DataFrame()
    
# Função principal do dashboard
def main():
    st.set_page_config(page_title="Dashboard de Preços do Bitcoin", layout="wide")
    st.title("Dashboard de Preços do Bitcoin")
    st.write("Este dashboard exibe os dados do preço do Bitcoin coletados periodicamente em um banco PostgreSQL.")
    
    df = ler_dados_postgres()
    
    if not df.empty:
        st.subheader("Dados Recentes")
        st.dataframe(df)
        
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values(by='timestamp')
        
        # Gráfico
        st.subheader("Evolução do Preço do Bitcoin")
        
        chart = alt.Chart(df).mark_line().encode(
            x='timestamp:T',
            y=alt.Y('valor:Q', scale=alt.Scale(zero=False)),
            tooltip=['timestamp:T', 'valor:Q']
        ).properties(
            width='container',
            height=400
        ).interactive()
        
        st.altair_chart(chart, use_container_width=True)
        
        # Estatísticas Gerais
        st.subheader("Estatísticas Gerais")
        col1, col2, col3 = st.columns(3)
        col1.metric("Preço Atual", f"${df['valor'].iloc[-1]:,.2f}")
        col2.metric("Preço Máximo", f"${df['valor'].max():,.2f}")
        col3.metric("Preço Mínimo", f"${df['valor'].min():,.2f}")
    else:
        st.warning("Nenhum dado encontrado no banco de dados PostgreSQL.")

if __name__ == "__main__":
    main()
