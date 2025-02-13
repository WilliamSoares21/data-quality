# pages/admin/avaliacao.py
import streamlit as st
import pandas as pd
from datetime import datetime

def avaliacao():
    st.title("Avaliação de Atendentes")
    
    atendente = st.selectbox("Selecione o atendente", ["Jefferson", "Rallyson", "Leonardo", "William", "Michelle"])
    
    qualidades = ["Comunicação", "Empatia", "Capacidade de resolução", "Conhecimento", "Trabalho em equipe", 
                  "Discrição", "Honestidade", "Paciência", "Pontualidade", "AURA"]
    
    notas = {}
    for qualidade in qualidades:
        notas[qualidade] = st.slider(f"{qualidade}", 0, 10, 5)
    
    if st.button("Salvar Avaliação"):
        data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        avaliacao = pd.DataFrame({
            "Atendente": [atendente],
            "Data": [data],
            **{q: [notas[q]] for q in qualidades}
        })
        
        # Salvar em um arquivo CSV
        try:
            df = pd.read_csv("data/avaliacoes.csv")
            df = pd.concat([df, avaliacao], ignore_index=True)
        except FileNotFoundError:
            df = avaliacao
        
        df.to_csv("data/avaliacoes.csv", index=False)
        st.success("Avaliação salva com sucesso!")

avaliacao()