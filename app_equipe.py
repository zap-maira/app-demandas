
import streamlit as st
import pandas as pd
import sqlite3

# Função para carregar os dados
@st.cache_data
def carregar_demandas():
    conn = sqlite3.connect("demandas.db")
    df = pd.read_sql_query("SELECT * FROM demandas", conn)
    conn.close()
    return df

st.title("📋 Painel da Equipe do Vereador")

df = carregar_demandas()

# Filtro por eixo
eixos = df["eixo"].unique()
eixo_selecionado = st.selectbox("Filtrar por eixo", options=["Todos"] + list(eixos))

if eixo_selecionado != "Todos":
    df = df[df["eixo"] == eixo_selecionado]

st.write("### Demandas encontradas:", df.shape[0])
st.dataframe(df, use_container_width=True)

# Download CSV
csv = df.to_csv(index=False).encode("utf-8")
st.download_button(
     label="\U0001F4E5 Baixar CSV",
    data=csv,
    file_name="demandas_filtradas.csv",
    mime="text/csv",
)
