"""
View: Ranking de Atendentes (Usuário Comum / Geral).
Exibe o ranking público de desempenho dos atendentes e gráfico comparativo.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
from io import BytesIO

from utils.auth import check_permission
from database.repository import get_all_avaliacoes, get_user_profile_photo

QUALIDADES = [
    'comunicacao', 'empatia', 'capacidade_resolucao', 'conhecimento', 'trabalho_equipe', 
    'discricao', 'honestidade', 'paciencia', 'pontualidade', 'aura'
]

def render_user_ranking_view():
    # Guarda declarativo de usuário autenticado
    check_permission()
    
    st.title("🏆 Ranking de Atendentes")
    st.caption("Visão Geral do Desempenho da Equipe")

    df = get_all_avaliacoes()
    
    if df.empty:
        st.warning("Nenhuma avaliação cadastrada ainda.")
        return

    df[QUALIDADES] = df[QUALIDADES].apply(pd.to_numeric, errors='coerce')
    df_mean = df.groupby('atendente')[QUALIDADES].mean().reset_index()
    df_mean['Média Geral'] = df_mean[QUALIDADES].mean(axis=1).round(2)
    
    st.subheader("📊 Gráfico Comparativo Geral")
    df_mean_long = pd.melt(df_mean, id_vars=['atendente'], value_vars=QUALIDADES, var_name='Qualidade', value_name='Média')
    fig = px.bar(
        df_mean_long,
        x='atendente',
        y='Média',
        color='Qualidade',
        barmode='group',
        title="Desempenho Geral por Atendente e Critério"
    )
    st.plotly_chart(fig, width="stretch")

    st.divider()

    st.subheader("🥇 Classificação Geral")
    df_ranking = df_mean.sort_values(by='Média Geral', ascending=False).reset_index(drop=True)

    for i, row in enumerate(df_ranking.itertuples(), start=1):
        col1, col2, col3 = st.columns([1, 2, 3])
        with col1:
            st.markdown(f"### {i}º Lugar")
        with col2:
            st.markdown(f"**{row.atendente}**")
            st.write(f"Pontuação Média: **{row._12:.2f}**")
        with col3:
            photo_bytes = get_user_profile_photo(row.atendente)
            if photo_bytes:
                try:
                    img = Image.open(BytesIO(photo_bytes))
                    st.image(img, caption=row.atendente, width=120)
                except Exception:
                    st.caption("Foto indisponível")
            else:
                st.caption("Foto indisponível")

render_user_ranking_view()
