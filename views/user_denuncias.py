"""
View: Fazer Denúncia (Usuário Comum / Geral).
Permite que o usuário autenticado registre uma denúncia contra um atendente.
"""

import streamlit as st
from utils.auth import check_permission
from database.repository import insert_denuncia, FUNCIONARIOS

def render_user_denuncias_view():
    # Guarda declarativo de usuário autenticado
    check_permission()
    
    st.title("⚠️ Registrar Denúncia")
    st.caption("Suas denúncias serão analisadas sigilosamente pela administração.")

    denunciado = st.selectbox(
        "Selecione o Atendente a ser Denunciado",
        FUNCIONARIOS,
        key="user_select_denunciado"
    )
    
    motivo = st.text_area(
        "Descreva o motivo da denúncia detalhadamente",
        placeholder="Informe os fatos ocorridos...",
        key="user_text_motivo",
        height=150
    )

    if st.button("Enviar Denúncia", type="primary", width="stretch"):
        if not motivo.strip():
            st.error("Por favor, detalhe o motivo da denúncia antes de enviar.")
        else:
            username = st.session_state.username
            if insert_denuncia(username, denunciado, motivo.strip()):
                st.success("Sua denúncia foi registrada com sucesso e enviada para análise!")
                st.info("Você pode acompanhar o status na tela de Perfil.")

render_user_denuncias_view()
