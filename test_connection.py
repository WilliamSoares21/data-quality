import streamlit as st
from pymongo import MongoClient

def get_database():
    client = MongoClient(st.secrets["mongo"]["uri"])
    return client["cluster-data-quality"]

def test_connection():
    db = get_database()
    collections = db.list_collection_names()
    st.write("Conexão bem-sucedida!")
    st.write("Coleções no banco de dados:", collections)

if __name__ == "__main__":
    test_connection()