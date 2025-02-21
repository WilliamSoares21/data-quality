import streamlit as st
from pymongo import MongoClient
from datetime import datetime

def get_database():
    client = MongoClient(st.secrets["mongo"]["uri"])
    return client["cluster-data-quality"]

def avaliacao():
    st.title("Avaliação de Atendentes")
    
    db = get_database()
    avaliacoes_collection = db["avaliacoes"]
    
    atendente = st.selectbox("Selecione o atendente", ["Jefferson", "Rallyson", "Leonardo", "William", "Michelle"], key="select_atendente_avaliacao")
    
    qualidades = ["comunicacao", "empatia", "capacidade_resolucao", "conhecimento", "trabalho_equipe", 
                  "discricao", "honestidade", "paciencia", "pontualidade", "aura"]
    
    notas = {}
    for qualidade in qualidades:
        notas[qualidade] = st.text_input(f"{qualidade.capitalize()} (0 a 10)", key=f"text_input_{qualidade}_avaliacao")
    
    if st.button("Salvar Avaliação", key="save_button_avaliacao"):
        data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Converter as notas para float
        try:
            notas = {q: float(notas[q]) for q in qualidades}
        except ValueError:
            st.error("Por favor, insira valores numéricos válidos para todas as qualidades.")
            return
        
        avaliacao = {
            "atendente": atendente,
            "data": data,
            **notas
        }
        
        avaliacoes_collection.insert_one(avaliacao)
        st.success("Avaliação salva com sucesso!")

avaliacao()