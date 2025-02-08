# pages/admin/graficos.py
import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image

def graficos():
    st.title("Gráficos de Desempenho")
    
    df = pd.read_csv("data/avaliacoes.csv")
    df['Data'] = pd.to_datetime(df['Data'])
    
    atendente = st.selectbox("Selecione o atendente", df['Atendente'].unique())
    periodo = st.selectbox("Selecione o período", ["Semanal", "Mensal"])
    
    if periodo == "Semanal":
        df_filtrado = df[df['Data'] >= pd.Timestamp.now() - pd.Timedelta(weeks=1)]
    else:
        df_filtrado = df[df['Data'] >= pd.Timestamp.now() - pd.Timedelta(days=30)]
    
    df_atendente = df_filtrado[df_filtrado['Atendente'] == atendente]
    
    qualidades = ["Comunicação", "Empatia", "Capacidade de resolução", "Conhecimento", "Trabalho em equipe", 
                  "Discrição", "Honestidade", "Paciência", "Pontualidade", "AURA"]
    
    fig = px.line(df_atendente, x='Data', y=qualidades, title=f"Desempenho {periodo} de {atendente}")
    st.plotly_chart(fig)
    
    # Ranking
    df_ranking = df_filtrado.groupby('Atendente')[qualidades].mean().sum(axis=1).sort_values(ascending=False)
    st.subheader("Ranking de Atendentes")
    st.bar_chart(df_ranking)

graficos()

# Ranking com fotos
st.subheader("Ranking de Atendentes")
for atendente in df_ranking.index:
    col1, col2 = st.columns([1, 4])
    try:
        img = Image.open(f"images/atendentes/{atendente.lower()}.jpg")
        col1.image(img, width=100)
    except FileNotFoundError:
        col1.write("Sem foto")
    col2.write(f"{atendente}: {df_ranking[atendente]:.2f}")