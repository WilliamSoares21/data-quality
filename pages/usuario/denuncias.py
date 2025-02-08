# pages/usuario/denuncias.py
import streamlit as st
import pandas as pd
from datetime import datetime

def denuncias():
    st.title("Fazer Denúncia")
    
    denunciado = st.selectbox("Selecione o atendente denunciado", ["Jefferson", "Rallyson", "Leonardo", "William", "Michelle"])
    motivo = st.text_area("Descreva o motivo da denúncia")
    
    if st.button("Enviar Denúncia"):
        data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        denuncia = pd.DataFrame({
            "Denunciante": [st.session_state.username],
            "Denunciado": [denunciado],
            "Motivo": [motivo],
            "Data": [data]
        })
        
        # Salvar em um arquivo CSV
        try:
            df = pd.read_csv("data/denuncias.csv")
            df = pd.concat([df, denuncia], ignore_index=True)
        except FileNotFoundError:
            df = denuncia
        
        df.to_csv("data/denuncias.csv", index=False)
        st.success("Denúncia enviada com sucesso!")

denuncias()