# pages/usuario/denuncias.py
import streamlit as st
from pymongo import MongoClient
from datetime import datetime

def get_database():
    client = MongoClient(st.secrets["mongo"]["uri"])
    return client["cluster-data-quality"]

def denuncias():
    st.title("Fazer Denúncia")
    
    denunciado = st.selectbox("Selecione o atendente denunciado", ["Jefferson", "Rallyson", "Leonardo", "William", "Michelle"])
    motivo = st.text_area("Descreva o motivo da denúncia")
    
    if st.button("Enviar Denúncia"):
        data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        denuncia = {
            "Denunciante": st.session_state.username,
            "Denunciado": denunciado,
            "Motivo": motivo,
            "Data": data
        }
        
        db = get_database()
        db.denuncias.insert_one(denuncia)
        st.success("Denúncia enviada com sucesso!")

denuncias()