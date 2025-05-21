import streamlit as st
import pandas as pd
from supabase import create_client, Client

# Configurações do Supabase
url = "https://hxnhfrzhfsaykuvicpbc.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imh4bmhmcnpoZnNheWt1dmljcGJjIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0Nzc5MzM3MCwiZXhwIjoyMDYzMzY5MzcwfQ.Wh2vVRlsV8QcTueMKzlCFqDdDtz7ohQqODXXnYLfukg"

supabase: Client = create_client(url, key)

# Título do app
st.title("📋 Painel da Equipe do Vereador")

# Carregar dados da Supabase
def carregar_demandas():
    try:
        response = supabase.table("demandas").select("*").order("data_envio", desc=True).execute()
        if hasattr(response, "error") and response.error:
            st.error(f"Erro ao carregar dados: {response.error}")
            return pd.DataFrame()
        return pd.DataFrame(response.data)
    except Exception as e:
        st.error(f"Erro ao acessar a Supabase: {e}")
        return pd.DataFrame()

df = carregar_demandas()

if not df.empty:
    eixos = df["eixo"].dropna().unique().tolist()
    eixo_selecionado = st.selectbox("Filtrar por eixo", options=["Todos"] + eixos)

    if eixo_selecionado != "Todos":
        df = df[df["eixo"] == eixo_selecionado]

    st.write(f"### Demandas encontradas: {len(df)}")
    st.dataframe(df, use_container_width=True)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Baixar CSV",
        data=csv,
        file_name="demandas_filtradas.csv",
        mime="text/csv"
    )
else:
    st.warning("Nenhuma demanda encontrada.")

if st.button("🔄 Atualizar dados"):
    st.rerun()

