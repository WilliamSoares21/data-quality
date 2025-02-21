import pandas as pd
from pymongo import MongoClient
import streamlit as st

def get_database():
    client = MongoClient(
        st.secrets["mongo"]["uri"],
        tls=True,
        tlsAllowInvalidCertificates=True
    )
    return client["cluster-data-quality"]

def import_csv_to_mongo():
    db = get_database()

    # Importar dados do arquivo CSV de avaliações
    avaliacoes_df = pd.read_csv("data/avaliacoes.csv")
    avaliacoes_collection = db["avaliacoes"]
    avaliacoes_collection.insert_many(avaliacoes_df.to_dict("records"))
    st.write("Dados de avaliações importados com sucesso!")

    # Importar dados do arquivo CSV de denúncias
    denuncias_df = pd.read_csv("data/denuncias.csv")
    denuncias_collection = db["denuncias"]
    denuncias_collection.insert_many(denuncias_df.to_dict("records"))
    st.write("Dados de denúncias importados com sucesso!")

    # Importar dados do arquivo CSV de usuários
    usuarios_df = pd.read_csv("data/usuarios.csv")
    usuarios_collection = db["usuarios"]
    usuarios_collection.insert_many(usuarios_df.to_dict("records"))
    st.write("Dados de usuários importados com sucesso!")

if __name__ == "__main__":
    import_csv_to_mongo()