# pages/perfil.py
import streamlit as st
import pandas as pd

def perfil():
    st.title("Perfil do Usuário")
    
    st.write(f"Nome de usuário: {st.session_state.username}")
    st.write(f"Função: {'Administrador' if st.session_state.role == 'admin' else 'Usuário comum'}")
    
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

perfil()