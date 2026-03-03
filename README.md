# 🏋️‍♀️ Motriz Training

Aplicativo web para registro e acompanhamento de treinos na academia, desenvolvido com Python e Streamlit.

## ✨ Funcionalidades

- **Sessão de treino guiada** — selecione os exercícios do dia e registre carga e séries um a um
- **Sugestão de carga** — exibe automaticamente o peso utilizado na última vez que o exercício foi realizado
- **Cadastro de exercícios** — adicione novos exercícios à sua lista pelo menu lateral
- **Histórico por dia** — visualize todos os treinos registrados organizados por data

## 🚀 Como executar

**Pré-requisitos:** Python 3.8+

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/Meu_treino.git
   cd Meu_treino
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Inicie o app:
   ```bash
   streamlit run academia.py
   ```

4. Acesse no navegador em `http://localhost:8501`

## 🗂️ Estrutura do projeto

```
Meu_treino/
├── academia.py              # Aplicação principal
├── requirements.txt         # Dependências do projeto
├── historico_treinos.csv    # Gerado automaticamente ao registrar treinos
└── meus_exercicios.csv      # Gerado automaticamente ao cadastrar exercícios
```

> Os arquivos `.csv` são ignorados pelo Git (ver `.gitignore`) e ficam apenas na sua máquina.

## 🛠️ Tecnologias

- [Python](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- [Pandas](https://pandas.pydata.org/)

## 📄 Licença

Distribuído sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.