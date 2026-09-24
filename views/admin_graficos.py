"""
View: Gráficos de Desempenho (Administrador).
Exibe gráficos interativos semanais e mensais com Plotly e ranking detalhado de atendentes.
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

def render_admin_graficos_view():
    # Guarda declarativo de perfil Admin
    check_permission("admin")
    
    st.title("📈 Gráficos de Desempenho e Métricas")
    st.caption("Visão Consolidada de Atendimento")

    df = get_all_avaliacoes()
    
    if df.empty:
        st.warning("Nenhuma avaliação cadastrada no banco de dados para gerar gráficos.")
        return

    df['data'] = pd.to_datetime(df['data'])
    df[QUALIDADES] = df[QUALIDADES].apply(pd.to_numeric, errors='coerce')
    
    col_filters1, col_filters2 = st.columns(2)
    with col_filters1:
        atendentes_unicos = df['atendente'].unique()
        atendente_sel = st.selectbox("Selecione o Atendente", atendentes_unicos, key="graficos_select_atendente")
    with col_filters2:
        tipo_grafico = st.selectbox("Período de Agrupamento", ["Semanal", "Mensal"], key="graficos_select_periodo")

    df_atendente = df[df['atendente'] == atendente_sel].copy()

    if tipo_grafico == "Semanal":
        df_atendente['Semana'] = df_atendente['data'].dt.to_period('W').apply(lambda r: r.start_time)
        df_agrupado = df_atendente.groupby('Semana')[QUALIDADES].mean().reset_index()
        periodo_col = 'Semana'
    else:
        df_atendente['Mês'] = df_atendente['data'].dt.to_period('M').apply(lambda r: r.start_time)
        df_agrupado = df_atendente.groupby('Mês')[QUALIDADES].mean().reset_index()
        periodo_col = 'Mês'

    if df_agrupado.empty:
        st.info("Dados insuficientes para o atendente selecionado no período.")
    else:
        df_long = pd.melt(df_agrupado, id_vars=[periodo_col], value_vars=QUALIDADES, var_name='Qualidade', value_name='Média')
        fig = px.bar(
            df_long,
            x='Qualidade',
            y='Média',
            color='Qualidade',
            title=f"Desempenho {tipo_grafico} - {atendente_sel}",
            labels={'Média': 'Nota Média'},
            barmode='group'
        )
        st.plotly_chart(fig, width="stretch")

    st.divider()

    # Ranking Geral
    st.subheader("🏆 Ranking Geral de Atendentes")
    df_ranking = df.groupby('atendente')[QUALIDADES].mean().reset_index()
    df_ranking['Média Geral'] = df_ranking[QUALIDADES].mean(axis=1).round(2)
    df_ranking = df_ranking.sort_values(by='Média Geral', ascending=False).reset_index(drop=True)

    for i, row in enumerate(df_ranking.itertuples(), start=1):
        c1, c2, c3 = st.columns([1, 2, 3])
        with c1:
            st.markdown(f"### {i}º Lugar")
        with c2:
            st.markdown(f"**{row.atendente}**")
            st.write(f"Média Geral: **{row._12:.2f}**")
        with c3:
            photo_bytes = get_user_profile_photo(row.atendente)
            if photo_bytes:
                try:
                    img = Image.open(BytesIO(photo_bytes))
                    st.image(img, caption=row.atendente, width=100)
                except Exception:
                    st.caption("Sem foto disponível")
            else:
                st.caption("Sem foto disponível")

render_admin_graficos_view()
