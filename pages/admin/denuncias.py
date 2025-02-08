# pages/admin/denuncias.py
import streamlit as st
import pandas as pd

def visualizar_denuncias():
    st.title("Visualização de Denúncias")
    
    try:
        df = pd.read_csv("data/denuncias.csv")
        st.dataframe(df)
    except FileNotFoundError:
        st.info("Nenhuma denúncia registrada ainda.")

visualizar_denuncias()