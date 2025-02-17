import streamlit as st
import pandas as pd
from datetime import datetime

def avaliacao():
    st.title("Avaliação de Atendentes")
    
    atendente = st.selectbox("Selecione o atendente", ["Jefferson", "Rallyson", "Leonardo", "William", "Michelle"], key="select_atendente_avaliacao")
    
    qualidades = ["Comunicação", "Empatia", "Capacidade de resolução", "Conhecimento", "Trabalho em equipe", 
                  "Discrição", "Honestidade", "Paciência", "Pontualidade", "AURA"]
    
    notas = {}
    for qualidade in qualidades:
        notas[qualidade] = st.text_input(f"{qualidade} (0 a 10)", key=f"text_input_{qualidade}_avaliacao")
    
    if st.button("Salvar Avaliação", key="save_button_avaliacao"):
        data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Converter as notas para float
        try:
            notas = {q: float(notas[q]) for q in qualidades}
        except ValueError:
            st.error("Por favor, insira valores numéricos válidos para todas as qualidades.")
            return
        
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