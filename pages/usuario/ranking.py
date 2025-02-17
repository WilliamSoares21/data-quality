import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image

def ranking():
    st.title("Ranking de Atendentes")
    
    # Carregar os dados de avaliações
    df = pd.read_csv("data/avaliacoes.csv")
    
    # Verificar se o DataFrame está vazio
    if df.empty:
        st.warning("O DataFrame está vazio. Nenhum dado foi adicionado ainda.")
        return
    
    # Selecionar apenas as colunas numéricas
    numeric_cols = df.select_dtypes(include='number').columns
    
    # Verificar se a coluna 'AURA' existe
    if 'AURA' not in numeric_cols:
        st.error("A coluna 'AURA' não foi encontrada no DataFrame.")
        return
    
    # Gráfico geral de desempenho dos atendentes
    st.subheader("Desempenho Geral dos Atendentes")
    df_mean = df.groupby('Atendente')[numeric_cols].mean().reset_index()
    df_mean_long = pd.melt(df_mean, id_vars=['Atendente'], value_vars=numeric_cols, var_name='Qualidade', value_name='Média')
    fig = px.bar(df_mean_long, x='Atendente', y='Média', color='Qualidade', barmode='group', title="Desempenho Geral dos Atendentes")
    st.plotly_chart(fig)
    
    # Calcular o ranking
    df_ranking = df.groupby('Atendente')[numeric_cols].mean().sort_values(by='AURA', ascending=False).head(5)
    
    # Exibir o ranking com fotos
    for i, atendente in enumerate(df_ranking.index, start=1):
        col1, col2 = st.columns([1, 3])
        with col1:
            st.markdown(f"<h2>{i}º Lugar</h2>", unsafe_allow_html=True)
        with col2:
            st.write(f"{atendente}: {df_ranking.loc[atendente, 'AURA']}")
            # Exibir a foto do atendente 
            try:
                image = Image.open(f"data/fotos/{atendente.lower()}.jpg")
                st.image(image, caption=atendente, use_container_width=True, width=150)
            except FileNotFoundError:
                st.write("Foto não disponível")

if __name__ == "__main__":
    ranking()
