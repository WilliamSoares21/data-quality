"""
View: Perfil do Usuário.
Exibe informações do usuário autenticado, avaliações, denúncias e permite upload seguro de foto de perfil.
"""

import streamlit as st
import pandas as pd
from io import BytesIO
from PIL import Image

from utils.auth import check_permission
from utils.security import validate_uploaded_file
from database.repository import (
    get_all_avaliacoes,
    get_denuncias_by_user,
    get_user_profile_photo,
    save_user_profile_photo
)

def render_perfil_view():
    # 1. Guarda declarativo de permissão
    check_permission()
    
    username = st.session_state.username
    role = st.session_state.role

    st.title("👤 Perfil do Usuário")
    st.write(f"**Usuário:** {username}")
    st.write(f"**Função:** {'Administrador' if role == 'admin' else 'Usuário Comum'}")
    
    # 2. Exibir foto de perfil atual a partir do banco de dados/repository
    photo_bytes = get_user_profile_photo(username)
    if photo_bytes:
        try:
            image = Image.open(BytesIO(photo_bytes))
            st.image(image, caption=f"Foto de {username}", width=180)
        except Exception:
            st.info("Foto de perfil não pôde ser carregada.")
    else:
        st.info("Nenhuma foto de perfil cadastrada.")
    
    # 3. Upload seguro de nova foto de perfil
    uploaded_file = st.file_uploader("Escolha uma nova foto de perfil (PNG, JPG, JPEG)", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        is_valid, err_msg = validate_uploaded_file(uploaded_file, max_size_mb=5)
        if not is_valid:
            st.error(f"Upload rejeitado: {err_msg}")
        else:
            file_bytes = uploaded_file.getvalue()
            if save_user_profile_photo(username, file_bytes):
                st.success("Foto de perfil atualizada com sucesso no banco de dados!")
                st.rerun()

    st.divider()

    # 4. Exibir avaliações recentes do atendente
    df_avaliacoes = get_all_avaliacoes()
    if not df_avaliacoes.empty and "atendente" in df_avaliacoes.columns:
        df_user = df_avaliacoes[df_avaliacoes["atendente"] == username]
        if not df_user.empty:
            st.subheader("Suas Avaliações Recentes")
            st.dataframe(df_user.sort_values("data", ascending=False).head(), width="stretch")
        else:
            st.info("Você ainda não possui avaliações registradas.")
    else:
        st.info("Nenhuma avaliação cadastrada no sistema.")

    # 5. Exibir denúncias feitas pelo usuário
    denuncias = get_denuncias_by_user(username)
    st.subheader("Suas Denúncias Registradas")
    if denuncias:
        for d in denuncias:
            status_emoji = {
                "recusada": "🔴",
                "em_analise": "🟡",
                "aceita": "🟢"
            }.get(d.get("status"), "⚪")
            
            with st.expander(f"{status_emoji} Denúncia contra {d.get('denunciado')} (Data: {d.get('data')})"):
                st.write(f"**Motivo:** {d.get('motivo')}")
                st.write(f"**Status:** {d.get('status')}")
                if d.get("status") == "recusada" and d.get("comentario_admin"):
                    st.write(f"**Comentário do Admin:** {d.get('comentario_admin')}")
    else:
        st.info("Você ainda não registrou nenhuma denúncia.")

render_perfil_view()
