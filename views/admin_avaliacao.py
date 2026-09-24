"""
View: Avaliação de Atendentes (Administrador).
Permite que administradores registrem avaliações de qualidade dos atendentes.
"""

import streamlit as st
from utils.auth import check_permission
from database.repository import insert_avaliacao, FUNCIONARIOS

QUALIDADES = [
    "comunicacao", "empatia", "capacidade_resolucao", "conhecimento", "trabalho_equipe", 
    "discricao", "honestidade", "paciencia", "pontualidade", "aura"
]

def render_admin_avaliacao_view():
    # Guarda declarativo de perfil Admin
    check_permission("admin")
    
    st.title("📝 Avaliação de Atendentes")
    st.caption("Painel do Administrador")

    atendente = st.selectbox(
        "Selecione o Atendente",
        FUNCIONARIOS,
        key="admin_select_atendente"
    )
    
    st.subheader("Notas por Critério (0.0 a 10.0)")
    
    with st.form("avaliacao_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        notas_input = {}
        
        for idx, qualidade in enumerate(QUALIDADES):
            col = col1 if idx % 2 == 0 else col2
            notas_input[qualidade] = col.number_input(
                f"{qualidade.replace('_', ' ').capitalize()}",
                min_value=0.0,
                max_value=10.0,
                value=8.0,
                step=0.5,
                key=f"input_nota_{qualidade}"
            )
            
        submit = st.form_submit_button("Salvar Avaliação", type="primary", width="stretch")
        
        if submit:
            if insert_avaliacao(atendente, notas_input):
                st.success(f"Avaliação para **{atendente}** salva com sucesso no banco de dados!")

render_admin_avaliacao_view()
