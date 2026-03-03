import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# Configuração da Página
st.set_page_config(page_title="Motriz Training", page_icon="🏋️‍♀️")

# Conectando ao Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)


# --- FUNÇÕES DE DADOS ---
def carregar_dados():
    try:
        # ttl=0 é vital para ler dados frescos sempre
        return conn.read(worksheet="Historico", ttl=0)
    except:
        return pd.DataFrame(columns=['Data', 'Exercicio', 'Carga', 'Series'])


def carregar_exercicios():
    try:
        df = conn.read(worksheet="ListaExercicios", ttl=0)
        return df['nome'].tolist()
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
            st.cache_data.clear()  # Limpa cache para ler a nova lista
            st.success("Cadastrado!")
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
        st.info(f"Exercício {indice + 1} de {len(lista)}")
        st.header(exercicio_atual)

        # Busca última carga para sugerir
        ultima_vez = df_historico[df_historico['Exercicio'] == exercicio_atual]
        peso_sugerido = ultima_vez.iloc[-1]['Carga'] if not ultima_vez.empty else 0.0

        if peso_sugerido > 0:
            st.caption(f"💡 Carga anterior: {peso_sugerido}kg")

        # FORMULÁRIO DE ENTRADA (O que faltava no seu pedaço de código)
        with st.form(key=f"form_{indice}"):
            col1, col2 = st.columns(2)
            carga = col1.number_input("Carga (kg)", value=float(peso_sugerido), step=0.5)
            series = col2.number_input("Séries", value=3, step=1)

            if st.form_submit_button("✅ Confirmar e Próximo"):
                novo_reg = pd.DataFrame([{
                    'Data': datetime.now().strftime('%d/%m/%Y %H:%M'),
                    'Exercicio': exercicio_atual,
                    'Carga': carga,
                    'Series': series
                }])

                # Atualiza a planilha
                df_atualizado = pd.concat([df_historico, novo_reg], ignore_index=True)
                conn.update(worksheet="Historico", data=df_atualizado)

                # Limpa o cache para a próxima leitura vir atualizada
                st.cache_data.clear()

                st.session_state.indice_atual += 1
                st.rerun()
    else:
        st.success("🎉 Treino concluído e salvo!")
        if st.button("Finalizar e Voltar"):
            st.session_state.treino_iniciado = False
            st.rerun()

# Exibição do Histórico Agrupado
st.divider()
if not df_historico.empty:
    with st.expander("📊 Ver Histórico Completo"):
        st.dataframe(df_historico.sort_values(by='Data', ascending=False))