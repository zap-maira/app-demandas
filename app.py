import streamlit as st
import sqlite3
from datetime import datetime

# Conexão com banco SQLite
conn = sqlite3.connect('demandas.db', check_same_thread=False)
cursor = conn.cursor()
  
# Cria tabela se não existir
cursor.execute('''
CREATE TABLE IF NOT EXISTS demandas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    telefone TEXT,
    bairro TEXT,
    localizacao TEXT,
    eixo TEXT,
    descricao TEXT,
    data_envio TEXT
)
''')
conn.commit()

# Estado da sessão para controle de envio
if "enviado" not in st.session_state:
    st.session_state.enviado = False

st.title("📣 Envie sua demanda para o Vereador Fiscalizador")

if not st.session_state.enviado:
    st.markdown("Preencha os dados abaixo. Suas informações serão mantidas em sigilo.")

    nome = st.text_input("Nome completo")
    telefone = st.text_input("WhatsApp (com DDD)")
    bairro = st.text_input("Bairro")
    localizacao = st.text_input("Endereço ou localização aproximada (opcional)")
    eixo = st.selectbox("Área da demanda", ["Mobilidade", "Meio ambiente", "Emprego e renda", "Saúde", "Educação", "Outros"])
    descricao = st.text_area("Descreva a sua demanda")

    if st.button("Enviar demanda"):
        if nome.strip() and telefone.strip() and bairro.strip() and descricao.strip():
            data_envio = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute('''
                INSERT INTO demandas (nome, telefone, bairro, localizacao, eixo, descricao, data_envio)
                VALUES (?, ?, ?, ?, ?, ?, ?)''',
                (nome, telefone, bairro, localizacao, eixo, descricao, data_envio))
            conn.commit()
            st.session_state.enviado = True
            st.rerun()
        else:
            st.warning("Por favor, preencha todos os campos obrigatórios.")

else:
    st.success("✅ Sua demanda foi registrada com sucesso!")
    if st.button("📨 Enviar nova demanda"):
        st.session_state.enviado = False
        st.rerun()


