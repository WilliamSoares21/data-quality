import streamlit as st
from utils.auth import login, logout

if "username" not in st.session_state:
    st.session_state.username = None

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.role = None

def main():
    if not st.session_state.logged_in:
        st.title("Login")
        username = st.text_input("Usuário")
        password = st.text_input("Senha", type="password")
        if st.button("Login"):
            if login(username, password):
                st.success(f"Bem-vindo, {username}!")
                st.rerun()
            else:
                st.error("Usuário ou senha inválidos")
    else:
        show_navigation()

def show_navigation():
    st.sidebar.title(f"Bem-vindo, {st.session_state.username}")
    st.sidebar.button("Logout", on_click=logout)

    if st.session_state.role == "admin":
        page = st.sidebar.radio("Navegação", ["Avaliação", "Gráficos", "Denúncias"])
        if page == "Avaliação":
            show_avaliacao()
        elif page == "Gráficos":
            show_graficos()
        elif page == "Denúncias":
            show_denuncias_admin()
    else:
        page = st.sidebar.radio("Navegação", ["Perfil", "Denúncias"])
        if page == "Perfil":
            show_perfil()
        elif page == "Denúncias":
            show_denuncias_user()

def show_avaliacao():
    st.title("Avaliação de Atendentes")
    atendente = st.selectbox("Selecione o atendente", ["Jefferson", "Rallyson", "Leonardo", "William", "Michelle"])
    # Implemente a lógica de avaliação aqui

def show_graficos():
    st.title("Gráficos de Desempenho")
    # Implemente a lógica de exibição de gráficos aqui

def show_denuncias_admin():
    st.title("Visualização de Denúncias")
    # Implemente a lógica de visualização de denúncias para o admin aqui

def show_perfil():
    st.title("Perfil do Usuário")
    # Implemente a lógica de exibição do perfil aqui

def show_denuncias_user():
    st.title("Fazer Denúncia")
    # Implemente a lógica de criação de denúncias para usuários comuns aqui

if __name__ == "__main__":
    main()