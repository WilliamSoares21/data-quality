# pages/perfil.py
import streamlit as st
import pandas as pd
import os
from PIL import Image

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
    
    if st.session_state.role != 'admin':
        try:
            df = pd.read_csv("data/avaliacoes.csv")
            df_user = df[df['Atendente'] == st.session_state.username]
            if not df_user.empty:
                st.subheader("Suas avaliações recentes")
                st.dataframe(df_user.sort_values('Data', ascending=False).head())
            else:
                st.info("Você ainda não tem avaliações registradas.")
        except FileNotFoundError:
            st.info("Nenhuma avaliação registrada ainda.")

if __name__ == "__main__":
    perfil()