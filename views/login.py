"""
View: Login de Usuários.
Renderiza o formulário de autenticação e valida credenciais via utils.auth.
"""

import streamlit as st
from utils.auth import login

def render_login_view():
    st.title("🔐 Login no Sistema")
    st.subheader("Dashboard de Qualidade de Dados")
    
    with st.form("login_form", clear_on_submit=False):
        username = st.text_input("Usuário", key="login_username_input").strip()
        password = st.text_input("Senha", type="password", key="login_password_input")
        submit = st.form_submit_button("Entrar", type="primary", width="stretch")
        
        if submit:
            if not username or not password:
                st.error("Por favor, preencha o usuário e a senha.")
            else:
                if login(username, password):
                    st.success(f"Bem-vindo, {username}!")
                    st.rerun()
                else:
                    st.error("Usuário ou senha inválidos.")

render_login_view()
