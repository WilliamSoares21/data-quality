"""
View: Gerenciamento de Denúncias (Administrador).
Painel de análise e moderação de denúncias submetidas pelos usuários.
"""

import streamlit as st
from utils.auth import check_permission
from database.repository import get_all_denuncias, update_denuncia_status

def render_admin_denuncias_view():
    # Guarda declarativo de perfil Admin
    check_permission("admin")
    
    st.title("🛡️ Gerenciamento de Denúncias")
    st.caption("Painel de Moderação do Administrador")

    denuncias = get_all_denuncias()
    
    if not denuncias:
        st.info("Nenhuma denúncia registrada até o momento.")
        return

    st.write(f"Total de denúncias no sistema: **{len(denuncias)}**")

    for denuncia in denuncias:
        denuncia_id = denuncia.get("id") or denuncia.get("_id")
        status = denuncia.get("status", "em_analise")
        status_emoji = {
            "recusada": "🔴",
            "em_analise": "🟡",
            "aceita": "🟢"
        }.get(status, "⚪")

        with st.expander(f"{status_emoji} Denúncia de **{denuncia.get('denunciante')}** contra **{denuncia.get('denunciado')}** ({denuncia.get('data')})"):
            st.write(f"**Motivo:** {denuncia.get('motivo')}")
            st.write(f"**Status Atual:** {status}")

            if status == "recusada" and denuncia.get("comentario_admin"):
                st.write(f"**Justificativa de Rejeição:** {denuncia.get('comentario_admin')}")

            if status == "em_analise":
                st.divider()
                col_btn1, col_btn2 = st.columns(2)
                
                with col_btn1:
                    if st.button("✅ Aceitar Denúncia", key=f"btn_aceitar_{denuncia_id}", type="primary"):
                        if update_denuncia_status(denuncia_id, "aceita"):
                            st.success("Denúncia aceita com sucesso.")
                            st.rerun()

                with col_btn2:
                    with st.popover("🔴 Rejeitar Denúncia"):
                        comentario = st.text_area("Motivo da rejeição", key=f"txt_comentario_{denuncia_id}")
                        if st.button("Confirmar Rejeição", key=f"btn_confirmar_rejeitar_{denuncia_id}"):
                            if comentario.strip():
                                if update_denuncia_status(denuncia_id, "recusada", comentario.strip()):
                                    st.warning("Denúncia rejeitada.")
                                    st.rerun()
                            else:
                                st.error("Insira um comentário justificando a rejeição.")

render_admin_denuncias_view()
