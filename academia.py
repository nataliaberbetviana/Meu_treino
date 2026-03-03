import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Configuração e Estilo
st.set_page_config(page_title="Motriz Training", page_icon="🏋️‍♀️", layout="wide")
arquivo_dados = 'historico_treinos.csv'
arquivo_exercicios = 'meus_exercicios.csv'


# --- FUNÇÕES DE DADOS ---
def carregar_exercicios():
    if os.path.exists(arquivo_exercicios):
        return pd.read_csv(arquivo_exercicios)['nome'].tolist()
    # Lista inicial caso o arquivo não exista
    return ["Mesa flexora", "Elevação pélvica", "Remada baixa", "Bíceps direto"]


def salvar_novo_exercicio(nome):
    exs = carregar_exercicios()
    if nome not in exs:
        exs.append(nome)
        pd.DataFrame(exs, columns=['nome']).to_csv(arquivo_exercicios, index=False)


def carregar_historico():
    if os.path.exists(arquivo_dados):
        df = pd.read_csv(arquivo_dados)
        df['Data'] = pd.to_datetime(df['Data'])
        return df
    return pd.DataFrame(columns=['Data', 'Exercicio', 'Carga', 'Series', 'Reps'])


# --- INICIALIZAÇÃO ---
df_historico = carregar_historico()
lista_oficial = carregar_exercicios()

if 'treino_iniciado' not in st.session_state:
    st.session_state.treino_iniciado = False

# --- INTERFACE: MENU LATERAL (SIDEBAR) ---
with st.sidebar:
    st.header("⚙️ Configurações")
    novo_ex = st.text_input("Adicionar novo exercício:")
    if st.button("➕ Cadastrar"):
        if novo_ex:
            salvar_novo_exercicio(novo_ex)
            st.success("Exercício adicionado!")
            st.rerun()

# --- INTERFACE PRINCIPAL ---
st.title("🏃‍♀️ Sessão de Treino")

if not st.session_state.treino_iniciado:
    st.subheader("O que vamos treinar hoje?")

    exercicios_selecionados = st.multiselect(
        "Selecione os exercícios:",
        options=lista_oficial,
        default=lista_oficial[:4] if len(lista_oficial) > 4 else lista_oficial
    )

    if st.button("🚀 Iniciar Treino"):
        if exercicios_selecionados:
            st.session_state.lista_treino = exercicios_selecionados
            st.session_state.indice_atual = 0
            st.session_state.treino_iniciado = True
            st.rerun()

else:
    # Lógica de Execução (igual à anterior, mas salvando no novo formato)
    lista = st.session_state.lista_treino
    indice = st.session_state.indice_atual

    if indice < len(lista):
        exercicio_atual = lista[indice]
        st.info(f"Exercício {indice + 1} de {len(lista)}")
        st.header(exercicio_atual)

        # Busca última carga
        ultima_vez = df_historico[df_historico['Exercicio'] == exercicio_atual]
        peso_sugerido = ultima_vez.iloc[-1]['Carga'] if not ultima_vez.empty else 0.0

        if peso_sugerido > 0:
            st.caption(f"💡 Carga anterior: {peso_sugerido}kg")

        with st.form(key=f"exec_{indice}"):
            col1, col2 = st.columns(2)
            carga = col1.number_input("Carga (kg)", value=float(peso_sugerido))
            series = col2.number_input("Séries", value=3)
            proximo = st.form_submit_button("✅ Confirmar e Próximo")

            if proximo:
                novo_reg = pd.DataFrame([{
                    'Data': datetime.now(),
                    'Exercicio': exercicio_atual,
                    'Carga': carga,
                    'Series': series
                }])
                df_historico = pd.concat([df_historico, novo_reg], ignore_index=True)
                df_historico.to_csv(arquivo_dados, index=False)
                st.session_state.indice_atual += 1
                st.rerun()
    else:
        st.success("🎉 Treino concluído!")
        if st.button("Finalizar e Voltar"):
            st.session_state.treino_iniciado = False
            st.rerun()

# --- HISTÓRICO AGRUPADO ---
st.divider()
st.subheader("📊 Histórico por Dia")

if not df_historico.empty:
    # Agrupando por data (apenas dia/mês/ano)
    df_historico['Data_Simples'] = df_historico['Data'].dt.strftime('%d/%m/%Y')
    datas = df_historico['Data_Simples'].unique()[::-1]  # Mais recentes primeiro

    for d in datas:
        with st.expander(f"📅 Treino do dia {d}"):
            dados_do_dia = df_historico[df_historico['Data_Simples'] == d]
            st.table(dados_do_dia[['Exercicio', 'Carga', 'Series']])
else:
    st.info("Nenhum treino registrado.")