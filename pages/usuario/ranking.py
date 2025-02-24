import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
from pymongo import MongoClient

def get_database():
    client = MongoClient(st.secrets["mongo"]["uri"])
    return client["cluster-data-quality"]

def ranking():
    st.title("Ranking de Atendentes")
    
    db = get_database()
    avaliacoes_collection = db["avaliacoes"]
    
    # Carregar os dados de avaliações do MongoDB
    df = pd.DataFrame(list(avaliacoes_collection.find()))
    df['data'] = pd.to_datetime(df['data'])
    
    # Converter as colunas de qualidades para números
    qualidades = ['comunicacao', 'empatia', 'capacidade_resolucao', 'conhecimento', 'trabalho_equipe', 
                  'discricao', 'honestidade', 'paciencia', 'pontualidade', 'aura']
    df[qualidades] = df[qualidades].apply(pd.to_numeric, errors='coerce')
    
    # Verificar se o DataFrame está vazio
    if df.empty:
        st.warning("O DataFrame está vazio. Nenhum dado foi adicionado ainda.")
        return
    
    # Calcular a média das notas por atendente
    df_mean = df.groupby('atendente')[qualidades].mean().reset_index()
    
    # Calcular a média geral de todas as qualidades para cada atendente
    df_mean['Média Geral'] = df_mean[qualidades].mean(axis=1).round(2)
    
    # Gráfico geral de desempenho dos atendentes
    st.subheader("Desempenho Geral dos Atendentes")
    df_mean_long = pd.melt(df_mean, id_vars=['atendente'], value_vars=qualidades, var_name='Qualidade', value_name='Média')
    fig = px.bar(df_mean_long, x='atendente', y='Média', color='Qualidade', barmode='group', title="Desempenho Geral dos Atendentes")
    st.plotly_chart(fig)
    
    # Calcular o ranking com base na média geral
    df_ranking = df_mean.sort_values(by='Média Geral', ascending=False).reset_index(drop=True)
    
    # Exibir o ranking com fotos
    st.subheader("Ranking de Atendentes")
    for i, row in enumerate(df_ranking.itertuples(), start=1):
        col1, col2 = st.columns([1, 3])
        with col1:
            st.markdown(f"<h2>{i}º Lugar</h2>", unsafe_allow_html=True)
        with col2:
            st.write(f"{row.atendente}: {row._12:.2f}")  # _12 corresponde à coluna 'Média Geral'
            # Exibir a foto do atendente 
            try:
                image = Image.open(f"data/fotos/{row.atendente.lower()}.jpg")
                st.image(image, caption=row.atendente, use_container_width=True, width=150)
            except FileNotFoundError:
                st.write("Foto não disponível")

if __name__ == "__main__":
    ranking()
