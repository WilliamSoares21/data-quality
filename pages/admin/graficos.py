# pages/admin/graficos.py
import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image

def graficos():
    st.title("Gráficos de Desempenho")
    
    # Carregar os dados de avaliações
    df = pd.read_csv("data/avaliacoes.csv")
    df['Data'] = pd.to_datetime(df['Data'])
    
    # Selecionar o atendente
    atendente = st.selectbox("Selecione o atendente", df['Atendente'].unique())
    
    # Selecionar o tipo de gráfico
    tipo_grafico = st.selectbox("Selecione o tipo de gráfico", ["Semanal", "Mensal"])
    
    # Filtrar os dados por atendente
    df_atendente = df[df['Atendente'] == atendente]
    
    qualidades = ["Comunicação", "Empatia", "Capacidade de resolução", "Conhecimento", "Trabalho em equipe", 
                  "Discrição", "Honestidade", "Paciência", "Pontualidade", "AURA"]
    
    if tipo_grafico == "Semanal":
        # Gráfico de desempenho semanal
        df_atendente['Semana'] = df_atendente['Data'].dt.to_period('W').apply(lambda r: r.start_time)
        df_semanal = df_atendente.groupby('Semana')[qualidades].mean().reset_index()
        if df_semanal.empty:
            st.warning("Não há dados suficientes para gerar o gráfico semanal.")
        else:
            fig_semanal = px.bar(df_semanal, y='Semana', x=qualidades, orientation='h', title=f"Desempenho Semanal de {atendente}")
            st.plotly_chart(fig_semanal)
    else:
        # Gráfico de desempenho mensal
        df_atendente['Mês'] = df_atendente['Data'].dt.to_period('M').apply(lambda r: r.start_time)
        df_mensal = df_atendente.groupby('Mês')[qualidades].mean().reset_index()
        if df_mensal.empty:
            st.warning("Não há dados suficientes para gerar o gráfico mensal.")
        else:
            fig_mensal = px.bar(df_mensal, y='Mês', x=qualidades, orientation='h', title=f"Desempenho Mensal de {atendente}")
            st.plotly_chart(fig_mensal)
    
    # Ranking
    df_ranking = df.groupby('Atendente').mean().sort_values(by='AURA', ascending=False).head(5)
    
    # Exibir o ranking com fotos
    st.subheader("Ranking de Atendentes")
    for i, atendente in enumerate(df_ranking.index, start=1):
        col1, col2 = st.columns([1, 3])
        with col1:
            st.markdown(f"<h2>{i}º Lugar</h2>", unsafe_allow_html=True)
        with col2:
            st.write(f"{atendente}: {df_ranking.loc[atendente, 'AURA']}")
            # Exibir a foto do atendente (supondo que as fotos estejam em 'data/fotos/')
            try:
                image = Image.open(f"data/fotos/{atendente}.jpg")
                st.image(image, caption=atendente, use_container_width=True, width=150)
            except FileNotFoundError:
                st.write("Foto não disponível")

if __name__ == "__main__":
    graficos()