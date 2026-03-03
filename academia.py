import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# Configuração da Página
st.set_page_config(page_title="Motriz Training", page_icon="🏋️‍♀️")

# Conectando ao Google Sheets
# (As credenciais serão configuradas no painel do Streamlit Cloud depois)
conn = st.connection("gsheets", type=GSheetsConnection)


# --- FUNÇÕES DE DADOS ---
def carregar_dados():
    try:
        # Tenta ler a aba 'Historico'
        return conn.read(worksheet="Historico", ttl=0)
    except:
        # Se não existir, retorna um DataFrame com as colunas corretas
        return pd.DataFrame(columns=['Data', 'Exercicio', 'Carga', 'Series', 'Reps'])


def carregar_exercicios():
    try:
        return conn.read(worksheet="ListaExercicios", ttl=0)['nome'].tolist()
    except:
        return ["Mesa flexora", "Elevação pélvica", "Remada baixa", "Bíceps direto"]


# --- INICIALIZAÇÃO ---
df_historico = carregar_dados()
lista_oficial = carregar_exercicios()

if 'treino_iniciado' not in st.session_state:
    st.session_state.treino_iniciado = False

# --- INTERFACE: MENU LATERAL ---
with st.sidebar:
    st.header("⚙️ Configurações")
    novo_ex = st.text_input("Adicionar novo exercício:")
    if st.button("➕ Cadastrar"):
        if novo_ex and novo_ex not in lista_oficial:
            nova_lista = pd.DataFrame(lista_oficial + [novo_ex], columns=['nome'])
            conn.update(worksheet="ListaExercicios", data=nova_lista)
            st.success("Cadastrado no Google Sheets!")
            st.rerun()

# --- INTERFACE PRINCIPAL ---
st.title("🏃‍♀️ Sessão de Treino")

if not st.session_state.treino_iniciado:
    st.subheader("O que vamos treinar hoje?")
    exercicios_selecionados = st.multiselect("Selecione os exercícios:", options=lista_oficial)

    if st.button("🚀 Iniciar Treino") and exercicios_selecionados:
        st.session_state.lista_treino = exercicios_selecionados
        st.session_state.indice_atual = 0
        st.session_state.treino_iniciado = True
        st.rerun()

else:
    lista = st.session_state.lista_treino
    indice = st.session_state.indice_atual

    if indice < len(lista):
        exercicio_atual = lista[indice]