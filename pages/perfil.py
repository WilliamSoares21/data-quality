# pages/perfil.py
import streamlit as st
import pandas as pd
import os
from PIL import Image
from pymongo import MongoClient

def get_database():
    client = MongoClient(st.secrets["mongo"]["uri"])
    return client["cluster-data-quality"]

def perfil():
    st.title("Perfil do Usuário")
    
    # Inicializar as chaves 'username' e 'role' se não estiverem presentes
    if 'username' not in st.session_state:
        st.session_state.username = "Usuário Desconhecido"
    if 'role' not in st.session_state:
        st.session_state.role = "user"  # ou "admin" dependendo do contexto

    st.write(f"Nome de usuário: {st.session_state.username}")
    st.write(f"Função: {'Administrador' if st.session_state.role == 'admin' else 'Usuário comum'}")
    
    # Exibir a foto de perfil atual, se existir
    foto_path = f"data/fotos/{st.session_state.username}.jpg"
    if os.path.exists(foto_path):
        image = Image.open(foto_path)
        st.image(image, caption=st.session_state.username, use_container_width=True)
    else:
        st.write("Nenhuma foto de perfil encontrada.")
    
    # Upload de nova foto de perfil
    uploaded_file = st.file_uploader("Escolha uma nova foto de perfil", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        # Salvar a nova foto de perfil
        with open(foto_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success("Foto de perfil atualizada com sucesso!")
        st.image(uploaded_file, caption=st.session_state.username, use_container_width=True)
    
    db = get_database()
    
    # Exibir avaliações recentes
    avaliacoes_collection = db["avaliacoes"]
    df_user = pd.DataFrame(list(avaliacoes_collection.find({"atendente": st.session_state.username})))
    if not df_user.empty:
        st.subheader("Suas avaliações recentes")
        st.dataframe(df_user.sort_values('data', ascending=False).head())
    else:
        st.info("Você ainda não tem avaliações registradas.")
    
    # Exibir denúncias feitas pelo usuário
    denuncias_collection = db["denuncias"]
    df_denuncias = pd.DataFrame(list(denuncias_collection.find({"denunciante": st.session_state.username})))
    if not df_denuncias.empty:
        st.subheader("Suas denúncias")
        denunciados = df_denuncias['denunciado'].unique()
        for denunciado in denunciados:
            denuncias_denunciado = df_denuncias[df_denuncias['denunciado'] == denunciado]
            for _, denuncia in denuncias_denunciado.iterrows():
                status_emoji = {
                    "recusada": "🔴",
                    "em_analise": "🟡",
                    "aceita": "🟢"
                }.get(denuncia['status'], "⚪")
                with st.expander(f"{status_emoji} Denúncia contra {denunciado}"):
                    st.write(f"**Motivo:** {denuncia['motivo']}")
                    st.write(f"**Data:** {denuncia['data']}")
                    st.write(f"**Status:** {denuncia['status']}")
                    if denuncia['status'] == 'recusada':
                        st.write(f"**Comentário do Admin:** {denuncia['comentario_admin']}")
    else:
        st.info("Você ainda não fez nenhuma denúncia.")

if __name__ == "__main__":
    perfil()