"""
Dashboard de Qualidade de Dados - Arquivo Principal da Aplicação.
Gerencia inicialização de estado da sessão, autorização global, mock data e roteamento moderno via st.Page e st.navigation.
"""

import streamlit as st
from utils.auth import logout
from database.connection import init_demo_data
from database.repository import reset_demo_data

# 1. Configuração Global da Página
st.set_page_config(
    page_title="Dashboard de Qualidade de Dados",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Inicialização Centralizada e Segura do Session State e Mock Data
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = None

if "role" not in st.session_state:
    st.session_state.role = None

if "user_id" not in st.session_state:
    st.session_state.user_id = None

# Inicializa datasets simulados em memória para isolamento de sessão
init_demo_data()

# 3. Definição de Páginas Nativas via st.Page
login_page = st.Page("views/login.py", title="Login", icon="🔒")

# Páginas de Usuário Comum
perfil_page = st.Page("views/perfil.py", title="Meu Perfil", icon="👤")
user_denuncias_page = st.Page("views/user_denuncias.py", title="Fazer Denúncia", icon="⚠️")
user_ranking_page = st.Page("views/user_ranking.py", title="Ranking de Atendentes", icon="🏆")

# Páginas de Administrador
admin_avaliacao_page = st.Page("views/admin_avaliacao.py", title="Avaliação de Atendentes", icon="📝")
admin_graficos_page = st.Page("views/admin_graficos.py", title="Gráficos de Desempenho", icon="📈")
admin_denuncias_page = st.Page("views/admin_denuncias.py", title="Gerenciar Denúncias", icon="🛡️")

# 4. Roteamento Dinâmico por Perfil
if not st.session_state.logged_in:
    pg = st.navigation([login_page])
else:
    # Sidebar personalizada para usuário autenticado
    st.sidebar.markdown(f"### 👋 Olá, **{st.session_state.username}**")
    st.sidebar.caption(f"Perfil: **{st.session_state.role.upper() if st.session_state.role else 'USER'}**")
    
    if st.sidebar.button("🚪 Sair (Logout)", type="secondary", width="stretch"):
        logout()
        st.rerun()

    st.sidebar.divider()
    if st.sidebar.button("🔄 Restaurar Dados Demo", help="Restaura os dados mockados originais da sessão", width="stretch"):
        reset_demo_data()
        st.sidebar.success("Dados restaurados!")
        st.rerun()

    # Montagem da estrutura de menu dinâmico
    if st.session_state.role == "admin":
        nav_dict = {
            "Painel Administrativo": [admin_avaliacao_page, admin_graficos_page, admin_denuncias_page],
            "Área do Usuário": [perfil_page, user_denuncias_page, user_ranking_page]
        }
    else:
        nav_dict = {
            "Navegação": [perfil_page, user_denuncias_page, user_ranking_page]
        }
    
    pg = st.navigation(nav_dict)

# 5. Execução da Página Roteada
pg.run()