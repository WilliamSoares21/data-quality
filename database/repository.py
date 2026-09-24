"""
Camada de Repositório de Dados.
Isola as operações de leitura e escrita das telas da interface do Streamlit.
Aplica @st.cache_data para otimização de consultas e agregação de relatórios.
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from typing import List, Dict, Any, Optional
import base64
import os
import sqlite3

from database.connection import get_database
from utils.security import sanitize_filename

# Inicialização de esquemas SQLite se fallback for utilizado
def init_sqlite_tables(conn: sqlite3.Connection):
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS avaliacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            atendente TEXT NOT NULL,
            data TEXT NOT NULL,
            comunicacao REAL, empatia REAL, capacidade_resolucao REAL,
            conhecimento REAL, trabalho_equipe REAL, discricao REAL,
            honestidade REAL, paciencia REAL, pontualidade REAL, aura REAL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS denuncias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            denunciante TEXT NOT NULL,
            denunciado TEXT NOT NULL,
            motivo TEXT NOT NULL,
            data TEXT NOT NULL,
            status TEXT NOT NULL,
            comentario_admin TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            foto_base64 TEXT
        )
    """)
    conn.commit()

# --- REPOSITÓRIO DE AVALIAÇÕES ---

@st.cache_data(ttl=30)
def get_all_avaliacoes() -> pd.DataFrame:
    """Carrega todas as avaliações cadastradas em um DataFrame do Pandas."""
    db_ctx = get_database()
    
    if db_ctx["type"] == "mongo":
        collection = db_ctx["db"]["avaliacoes"]
        records = list(collection.find({}, {"_id": 0}))
        return pd.DataFrame(records)
    else:
        conn = db_ctx["db"]
        init_sqlite_tables(conn)
        df = pd.read_sql_query("SELECT * FROM avaliacoes", conn)
        if "id" in df.columns:
            df = df.drop(columns=["id"])
        return df

def insert_avaliacao(atendente: str, notas: Dict[str, float]) -> bool:
    """Insere uma nova avaliação no banco de dados e limpa a cache de dados."""
    db_ctx = get_database()
    data_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    record = {
        "atendente": atendente,
        "data": data_str,
        **notas
    }
    
    if db_ctx["type"] == "mongo":
        db_ctx["db"]["avaliacoes"].insert_one(record)
    else:
        conn = db_ctx["db"]
        init_sqlite_tables(conn)
        qualidades = ["comunicacao", "empatia", "capacidade_resolucao", "conhecimento", "trabalho_equipe", 
                      "discricao", "honestidade", "paciencia", "pontualidade", "aura"]
        cols = ["atendente", "data"] + qualidades
        vals = [atendente, data_str] + [notas.get(q, 0.0) for q in qualidades]
        placeholders = ", ".join(["?"] * len(vals))
        sql = f"INSERT INTO avaliacoes ({', '.join(cols)}) VALUES ({placeholders})"
        conn.cursor().execute(sql, vals)
        conn.commit()
        
    st.cache_data.clear()
    return True

# --- REPOSITÓRIO DE DENÚNCIAS ---

@st.cache_data(ttl=10)
def get_all_denuncias() -> List[Dict[str, Any]]:
    """Obtém todas as denúncias para visualização e gestão do administrador."""
    db_ctx = get_database()
    
    if db_ctx["type"] == "mongo":
        records = list(db_ctx["db"]["denuncias"].find())
        for r in records:
            r["id"] = str(r["_id"])
        return records
    else:
        conn = db_ctx["db"]
        init_sqlite_tables(conn)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM denuncias ORDER BY id DESC")
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

@st.cache_data(ttl=10)
def get_denuncias_by_user(username: str) -> List[Dict[str, Any]]:
    """Obtém denúncias criadas por um usuário específico."""
    db_ctx = get_database()
    
    if db_ctx["type"] == "mongo":
        records = list(db_ctx["db"]["denuncias"].find({"denunciante": username}))
        for r in records:
            r["id"] = str(r["_id"])
        return records
    else:
        conn = db_ctx["db"]
        init_sqlite_tables(conn)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM denuncias WHERE denunciante = ? ORDER BY id DESC", (username,))
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

def insert_denuncia(denunciante: str, denunciado: str, motivo: str) -> bool:
    """Cria um novo registro de denúncia."""
    db_ctx = get_database()
    data_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    record = {
        "denunciante": denunciante,
        "denunciado": denunciado,
        "motivo": motivo,
        "data": data_str,
        "status": "em_analise",
        "comentario_admin": ""
    }
    
    if db_ctx["type"] == "mongo":
        db_ctx["db"]["denuncias"].insert_one(record)
    else:
        conn = db_ctx["db"]
        init_sqlite_tables(conn)
        conn.cursor().execute(
            "INSERT INTO denuncias (denunciante, denunciado, motivo, data, status, comentario_admin) VALUES (?, ?, ?, ?, ?, ?)",
            (denunciante, denunciado, motivo, data_str, "em_analise", "")
        )
        conn.commit()
        
    st.cache_data.clear()
    return True

def update_denuncia_status(denuncia_id: Any, status: str, comentario_admin: str = "") -> bool:
    """Atualiza o status e comentário de uma denúncia existente."""
    db_ctx = get_database()
    
    if db_ctx["type"] == "mongo":
        from bson.objectid import ObjectId
        query = {"_id": ObjectId(denuncia_id)} if isinstance(denuncia_id, str) and len(denuncia_id) == 24 else {"_id": denuncia_id}
        db_ctx["db"]["denuncias"].update_one(query, {"$set": {"status": status, "comentario_admin": comentario_admin}})
    else:
        conn = db_ctx["db"]
        init_sqlite_tables(conn)
        conn.cursor().execute(
            "UPDATE denuncias SET status = ?, comentario_admin = ? WHERE id = ?",
            (status, comentario_admin, denuncia_id)
        )
        conn.commit()
        
    st.cache_data.clear()
    return True

# --- REPOSITÓRIO DE PERFIL E FOTOS (BASE64 NO DB / BLOB) ---

def save_user_profile_photo(username: str, file_bytes: bytes) -> bool:
    """
    Armazena a foto de perfil do usuário como string Base64 no banco de dados.
    Evita gravação em disco local na pasta data/fotos.
    """
    safe_user = sanitize_filename(username)
    encoded = base64.b64encode(file_bytes).decode("utf-8")
    db_ctx = get_database()
    
    if db_ctx["type"] == "mongo":
        db_ctx["db"]["usuarios"].update_one(
            {"username": safe_user},
            {"$set": {"foto_base64": encoded}},
            upsert=True
        )
    else:
        conn = db_ctx["db"]
        init_sqlite_tables(conn)
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM usuarios WHERE username = ?", (safe_user,))
        if cursor.fetchone():
            cursor.execute("UPDATE usuarios SET foto_base64 = ? WHERE username = ?", (encoded, safe_user))
        else:
            cursor.execute("INSERT INTO usuarios (username, password, role, foto_base64) VALUES (?, ?, ?, ?)", (safe_user, "", "user", encoded))
        conn.commit()
        
    st.cache_data.clear()
    return True

@st.cache_data(ttl=60)
def get_user_profile_photo(username: str) -> Optional[bytes]:
    """Recupera os bytes da foto de perfil do banco de dados ou do fallback seguro de assets."""
    safe_user = sanitize_filename(username)
    db_ctx = get_database()
    
    foto_b64 = None
    if db_ctx["type"] == "mongo":
        user_doc = db_ctx["db"]["usuarios"].find_one({"username": safe_user})
        if user_doc and "foto_base64" in user_doc:
            foto_b64 = user_doc["foto_base64"]
    else:
        conn = db_ctx["db"]
        init_sqlite_tables(conn)
        cursor = conn.cursor()
        cursor.execute("SELECT foto_base64 FROM usuarios WHERE username = ?", (safe_user,))
        row = cursor.fetchone()
        if row and row["foto_base64"]:
            foto_b64 = row["foto_base64"]
            
    if foto_b64:
        try:
            return base64.b64decode(foto_b64)
        except Exception:
            pass

    # Verificação de fallback seguro na pasta data/fotos se existir localmente (apenas leitura)
    local_photo_path = os.path.join("data", "fotos", f"{safe_user.lower()}.jpg")
    if os.path.exists(local_photo_path):
        try:
            with open(local_photo_path, "rb") as f:
                return f.read()
        except Exception:
            pass

    return None
