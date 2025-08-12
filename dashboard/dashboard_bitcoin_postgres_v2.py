import streamlit as st
from sqlalchemy import create_engine
import pandas as pd
import os
from dotenv import load_dotenv
import altair as alt
from datetime import timedelta

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
        
        df_display = df.copy()
        df_display['valor'] = df_display['valor'].map(lambda x: f"${x:,.2f}")
        df_display['timestamp'] = df_display['timestamp'].dt.strftime('%d/%m/%Y %H:%M:%S')
        
        st.dataframe(df_display.style.format({
            'valor': "{:>}",
            'timestamp': "{}"
        }))
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values(by='timestamp')
        
        # Filtro
        st.sidebar.subheader("Filtros")
        data_mais_recente = df['timestamp'].max().date()
        data_inicial_padrao = data_mais_recente - timedelta(days=30)
        
        data_inicial = st.sidebar.date_input("Data Inicial", value=data_inicial_padrao)
        data_final = st.sidebar.date_input("Data Final", value=data_mais_recente)
        df_filtrado = df[(df['timestamp'].dt.date >= data_inicial) & (df['timestamp'].dt.date <= data_final)]
        
        # Botão de atualizar
        st.sidebar.subheader("Atualização")
        refresh = st.sidebar.button("Atualizar dados")
        if refresh:
            st.rerun()
        
        # Formatando os dados para exportar em CSV
        df_export = df.copy()
        df_export['valor'] = "$" + df_export['valor'].apply(lambda x: f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        df_export['timestamp'] = pd.to_datetime(df_export['timestamp']).dt.strftime('%d/%m/%Y %H:%M:%S')
        
        # Botão de exportar em CSV
        csv_data = df_export.to_csv(index=False, sep=";", encoding="utf-8-sig")
        st.download_button("Baixar CSV", data=csv_data, file_name="dados_bitcoin.csv", mime="text/csv")
        
        # Gráfico do Histórico do Preço do Bitcoin
        st.subheader("Evolução do Preço do Bitcoin")
        mostrar_media = st.checkbox("Exibir Média Móvel", value=False)
        
        grafico_preco = alt.Chart(df_filtrado).mark_line(color='steelblue').encode(
            x='timestamp:T',
            y=alt.Y('valor:Q', scale=alt.Scale(zero=False), title='Preço ($)'),
            tooltip=['timestamp:T', 'valor:Q']
        ).properties(
            width='container',
            height=550
        )
        if mostrar_media:
            df_filtrado['media_movel'] = df_filtrado['valor'].rolling(window=5).mean()
            grafico_media = alt.Chart(df_filtrado).mark_line(color='green').encode(
                x='timestamp:T',
                y=alt.Y('media_movel:Q', title='Média Móvel'),
                tooltip=['timestamp:T', 'media_movel:Q']
            ).properties(
                width='container',
                height=550
            )
            st.altair_chart((grafico_preco + grafico_media).interactive(), use_container_width=True)
        else:
            st.altair_chart(grafico_preco.interactive(), use_container_width=True)
        
        # Calculando a porcentagem de variação entre o preço anterior.
        preco_atual = df['valor'].iloc[-1]
        data_atual = df['timestamp'].iloc[-1]
        data_24h = data_atual - timedelta(days=1)
        
        df['diferenca'] = (df['timestamp'] - data_24h).abs()
        indice_mais_proximo = df['diferenca'].idxmin()
        preco_ontem = df.loc[indice_mais_proximo, 'valor']
        
        delta = ((preco_atual - preco_ontem) / preco_ontem) * 100
        legenda_delta = f"{delta:.2f}% (vs 24h atrás)"
        df.drop(columns='diferenca', inplace=True)
        
        # Calculando o intervalo dos dias para comparar o preço médio
        intervalo_7dias = data_atual - timedelta(days=7)
        ultimos_7dias = df[df['timestamp'] >= intervalo_7dias]
        media_7dias = ultimos_7dias['valor'].mean()
        legenda_media = "últimos 7 dias"
        
        # Estatísticas Gerais
        st.subheader("Estatísticas Gerais")
        col1, col2, col3, col4 = st.columns(4)
        
        col1.metric("Preço Atual", f"${preco_atual:,.2f}", legenda_delta)
        col2.metric("Preço Máximo", f"${df['valor'].max():,.2f}")
        col3.metric("Preço Mínimo", f"${df['valor'].min():,.2f}")
        
        col4.metric("Preço Médio", f"${media_7dias:,.2f}", legenda_media)
        
        # Análise de tendência
        tendencia = "em alta" if delta > 0 else "em queda"
        st.info(f"O preço do Bitcoin está {tendencia} nas últimas 24h.")
        
        # Variação percentual diária
        df_daily = df.set_index('timestamp').resample('D').last().reset_index()
        df_daily['pct_change'] = df_daily['valor'].pct_change() * 100
        df_daily['dia'] = df_daily['timestamp'].dt.strftime('%d/%m')
        
        grafico_var_pct = alt.Chart(df_daily).mark_bar(color='purple').encode(
            x=alt.X('dia:N', title='Data', axis=alt.Axis(labelAngle=-45)),
            y=alt.Y('pct_change:Q', title='Variação %', axis=alt.Axis(format='.2f')),
            tooltip=[alt.Tooltip('timestamp:T', title='Data'),
                     alt.Tooltip('pct_change:Q', title='Variação (%)', format='.2f')]
        ).properties(
            title='Variação Percentual Diária',
            width='container',
            height=300
        ).interactive()
        st.altair_chart(grafico_var_pct, use_container_width=True)
        
    else:
        st.warning("Nenhum dado encontrado no banco de dados PostgreSQL.")

if __name__ == "__main__":
    main()
