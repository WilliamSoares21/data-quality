# Description: Arquivo principal da aplicação, responsável por renderizar a interface gráfica e controlar a navegação entre as páginas.
import streamlit as st
from utils.auth import login, logout
from pages.admin.avaliacao import avaliacao as admin_avaliacao
from pages.admin.graficos import graficos as admin_graficos
from pages.admin.denuncias import visualizar_denuncias as admin_denuncias
from pages.perfil import perfil as user_perfil
from pages.usuario.denuncias import denuncias as user_denuncias

# Inicialização do session_state
if "username" not in st.session_state:
    st.session_state.username = None

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "role" not in st.session_state:
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
    admin_avaliacao()

def show_graficos():
    admin_graficos()

def show_denuncias_admin():
    admin_denuncias()

def show_perfil():
    user_perfil()

def show_denuncias_user():
    user_denuncias()

if __name__ == "__main__":
    main()