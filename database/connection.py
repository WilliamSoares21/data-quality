"""
Módulo de Conexão com Banco de Dados.
Gerencia instâncias de banco de dados reutilizando pools de conexão via @st.cache_resource.
"""

import streamlit as st
import sqlite3
import os
from pathlib import Path
from pymongo import MongoClient

@st.cache_resource
def get_mongo_client() -> MongoClient:
    """
    Retorna uma instância de MongoClient otimizada e em cache.
    Reaproveita o pool de conexões entre execuções reativas do Streamlit.
    """
    if "mongo" in st.secrets and "uri" in st.secrets["mongo"]:
        uri = st.secrets["mongo"]["uri"]
        client = MongoClient(uri, tls=True, serverSelectionTimeoutMS=5000)
        return client
    return None

@st.cache_resource
def get_sqlite_connection(db_path: str = "data/database.sqlite"):
    """
    Retorna conexão com banco SQLite local como fallback de persistência estruturada.
    """
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def get_database():
    """
    Obtém o cliente de banco de dados ativo (MongoDB se configurado em secrets, caso contrário SQLite/Memory).
    """
    mongo_client = get_mongo_client()
    if mongo_client:
        try:
            # Tenta realizar ping rápido no MongoDB
            mongo_client.admin.command('ping')
            return {"type": "mongo", "db": mongo_client["cluster-data-quality"]}
        except Exception:
            pass
            
    # Fallback para SQLite local
    sqlite_conn = get_sqlite_connection()
    return {"type": "sqlite", "db": sqlite_conn}
