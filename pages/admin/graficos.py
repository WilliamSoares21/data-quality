# pages/admin/graficos.py
import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
from pymongo import MongoClient

def get_database():
    client = MongoClient(st.secrets["mongo"]["uri"])
    return client["cluster-data-quality"]

def graficos():
    st.title("Gráficos de Desempenho")
    
    db = get_database()
    avaliacoes_collection = db["avaliacoes"]
    
    # Carregar os dados de avaliações do MongoDB
    df = pd.DataFrame(list(avaliacoes_collection.find()))
    df['data'] = pd.to_datetime(df['data'])
    
    # Converter as colunas de qualidades para números
    qualidades = ['comunicacao', 'empatia', 'capacidade_resolucao', 'conhecimento', 'trabalho_equipe', 
                  'discricao', 'honestidade', 'paciencia', 'pontualidade', 'aura']
    df[qualidades] = df[qualidades].apply(pd.to_numeric, errors='coerce')
    
    # Selecionar o atendente
    atendente = st.selectbox("Selecione o atendente", df['atendente'].unique(), key="select_atendente")
    
    # Selecionar o tipo de gráfico
    tipo_grafico = st.selectbox("Selecione o tipo de gráfico", ["Semanal", "Mensal"], key="select_tipo_grafico")
    
    # Filtrar os dados por atendente
    df_atendente = df[df['atendente'] == atendente]
    df_atendente = df_atendente.copy()  
    
    if tipo_grafico == "Semanal":
        # Gráfico de desempenho semanal
        df_atendente.loc[:, 'Semana'] = df_atendente['data'].dt.to_period('W').apply(lambda r: r.start_time)
        df_semanal = df_atendente.groupby('Semana')[qualidades].mean().reset_index()
        if df_semanal.empty:
            st.warning("Não há dados suficientes para gerar o gráfico semanal.")
        else:
            # Converter o DataFrame para o formato longo para o Plotly
            df_semanal_long = pd.melt(df_semanal, id_vars=['Semana'], value_vars=qualidades, var_name='Qualidade', value_name='Média')
            fig_semanal = px.bar(df_semanal_long, x='Qualidade', y='Média', color='Qualidade', title=f"Desempenho Semanal de {atendente}")
            st.plotly_chart(fig_semanal)
    else:
        # Gráfico de desempenho mensal
        df_atendente['Mês'] = df_atendente['data'].dt.to_period('M').apply(lambda r: r.start_time)
        df_mensal = df_atendente.groupby('Mês')[qualidades].mean().reset_index()
        if df_mensal.empty:
            st.warning("Não há dados suficientes para gerar o gráfico mensal.")
        else:
            # Converter o DataFrame para o formato longo para o Plotly
            df_mensal_long = pd.melt(df_mensal, id_vars=['Mês'], value_vars=qualidades, var_name='Qualidade', value_name='Média')
            fig_mensal = px.bar(df_mensal_long, x='Qualidade', y='Média', color='Qualidade', title=f"Desempenho Mensal de {atendente}")
            st.plotly_chart(fig_mensal)
    
    # Ranking
    df_ranking = df.groupby('atendente')[qualidades].mean().reset_index()
    df_ranking['Média Geral'] = df_ranking[qualidades].mean(axis=1).round(2)
    df_ranking = df_ranking.sort_values(by='Média Geral', ascending=False).head(5)
    
    # Verificar o ranking calculado
    st.write("Ranking calculado:", df_ranking)
    
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
    graficos()