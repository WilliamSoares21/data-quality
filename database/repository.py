"""
Camada de Repositório de Dados em Memória (Mock Data & Session State).
Totalmente desacoplada de bancos de dados externos e arquivos locais de gravação.
Garante isolamento estrito por sessão no Streamlit Community Cloud e modo demonstração seguro.
"""

import base64
from datetime import datetime
from typing import Any, Dict, List, Optional
import pandas as pd
import streamlit as st
from utils.security import sanitize_filename

# --- AVATAR PADRÃO EMBUTIDO EM BASE64 (avatar-profile-default1.png) ---
# Fornece a mesma foto de perfil padrão de alta qualidade para todos os colaboradores.
DEFAULT_AVATAR_B64: str = (
    "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"
)

DEFAULT_AVATAR_BYTES: bytes = base64.b64decode(DEFAULT_AVATAR_B64)

# Lista oficial de atendentes do sistema
FUNCIONARIOS: List[str] = ["Kael", "Joao", "Milo", "Dante", "Zephyr"]

# --- DATASETS DE MOCK INICIAIS ---

INITIAL_AVALIACOES_DATA = [
    # Kael
    {"atendente": "Kael", "data": "2026-07-06 09:15:00", "comunicacao": 8.5, "empatia": 9.0, "capacidade_resolucao": 8.0, "conhecimento": 9.0, "trabalho_equipe": 8.5, "discricao": 9.0, "honestidade": 9.5, "paciencia": 8.5, "pontualidade": 9.0, "aura": 9.0},
    {"atendente": "Kael", "data": "2026-07-20 14:30:00", "comunicacao": 9.0, "empatia": 9.5, "capacidade_resolucao": 8.5, "conhecimento": 9.0, "trabalho_equipe": 9.0, "discricao": 9.5, "honestidade": 9.5, "paciencia": 9.0, "pontualidade": 8.5, "aura": 9.0},
    {"atendente": "Kael", "data": "2026-08-10 11:00:00", "comunicacao": 9.0, "empatia": 9.0, "capacidade_resolucao": 9.0, "conhecimento": 9.5, "trabalho_equipe": 9.0, "discricao": 9.0, "honestidade": 10.0, "paciencia": 9.0, "pontualidade": 9.0, "aura": 9.5},
    {"atendente": "Kael", "data": "2026-08-25 16:45:00", "comunicacao": 8.5, "empatia": 8.5, "capacidade_resolucao": 8.5, "conhecimento": 9.0, "trabalho_equipe": 8.5, "discricao": 8.5, "honestidade": 9.0, "paciencia": 8.5, "pontualidade": 9.5, "aura": 8.5},
    {"atendente": "Kael", "data": "2026-09-08 10:20:00", "comunicacao": 9.5, "empatia": 9.5, "capacidade_resolucao": 9.0, "conhecimento": 9.5, "trabalho_equipe": 9.5, "discricao": 9.5, "honestidade": 9.5, "paciencia": 9.5, "pontualidade": 9.0, "aura": 9.5},
    {"atendente": "Kael", "data": "2026-09-21 15:10:00", "comunicacao": 9.0, "empatia": 9.0, "capacidade_resolucao": 9.5, "conhecimento": 9.5, "trabalho_equipe": 9.0, "discricao": 9.0, "honestidade": 9.5, "paciencia": 9.0, "pontualidade": 9.5, "aura": 9.0},

    # Joao
    {"atendente": "Joao", "data": "2026-07-08 10:00:00", "comunicacao": 9.5, "empatia": 10.0, "capacidade_resolucao": 9.0, "conhecimento": 9.0, "trabalho_equipe": 9.5, "discricao": 9.5, "honestidade": 9.5, "paciencia": 9.5, "pontualidade": 9.0, "aura": 9.5},
    {"atendente": "Joao", "data": "2026-07-22 15:40:00", "comunicacao": 9.0, "empatia": 9.5, "capacidade_resolucao": 9.5, "conhecimento": 9.5, "trabalho_equipe": 9.0, "discricao": 9.0, "honestidade": 10.0, "paciencia": 9.0, "pontualidade": 9.5, "aura": 9.5},
    {"atendente": "Joao", "data": "2026-08-12 09:30:00", "comunicacao": 10.0, "empatia": 10.0, "capacidade_resolucao": 9.5, "conhecimento": 9.5, "trabalho_equipe": 10.0, "discricao": 9.5, "honestidade": 10.0, "paciencia": 10.0, "pontualidade": 9.5, "aura": 10.0},
    {"atendente": "Joao", "data": "2026-08-27 14:15:00", "comunicacao": 9.5, "empatia": 9.0, "capacidade_resolucao": 9.0, "conhecimento": 9.0, "trabalho_equipe": 9.5, "discricao": 9.5, "honestidade": 9.5, "paciencia": 9.5, "pontualidade": 9.0, "aura": 9.0},
    {"atendente": "Joao", "data": "2026-09-10 11:20:00", "comunicacao": 9.5, "empatia": 9.5, "capacidade_resolucao": 9.5, "conhecimento": 9.5, "trabalho_equipe": 9.5, "discricao": 9.0, "honestidade": 9.5, "paciencia": 9.0, "pontualidade": 9.5, "aura": 9.5},
    {"atendente": "Joao", "data": "2026-09-23 16:00:00", "comunicacao": 10.0, "empatia": 9.5, "capacidade_resolucao": 9.5, "conhecimento": 9.5, "trabalho_equipe": 9.5, "discricao": 10.0, "honestidade": 10.0, "paciencia": 9.5, "pontualidade": 9.5, "aura": 9.5},

    # Milo
    {"atendente": "Milo", "data": "2026-07-09 11:15:00", "comunicacao": 8.0, "empatia": 8.0, "capacidade_resolucao": 8.5, "conhecimento": 8.5, "trabalho_equipe": 8.0, "discricao": 8.5, "honestidade": 9.0, "paciencia": 8.0, "pontualidade": 8.5, "aura": 8.0},
    {"atendente": "Milo", "data": "2026-07-25 16:10:00", "comunicacao": 8.5, "empatia": 8.5, "capacidade_resolucao": 8.5, "conhecimento": 9.0, "trabalho_equipe": 8.5, "discricao": 8.0, "honestidade": 8.5, "paciencia": 8.5, "pontualidade": 8.0, "aura": 8.5},
    {"atendente": "Milo", "data": "2026-08-15 10:00:00", "comunicacao": 8.5, "empatia": 8.0, "capacidade_resolucao": 9.0, "conhecimento": 9.0, "trabalho_equipe": 8.5, "discricao": 8.5, "honestidade": 9.0, "paciencia": 8.5, "pontualidade": 9.0, "aura": 8.5},
    {"atendente": "Milo", "data": "2026-08-29 13:40:00", "comunicacao": 9.0, "empatia": 8.5, "capacidade_resolucao": 9.0, "conhecimento": 8.5, "trabalho_equipe": 9.0, "discricao": 9.0, "honestidade": 9.0, "paciencia": 8.5, "pontualidade": 8.5, "aura": 8.5},
    {"atendente": "Milo", "data": "2026-09-12 15:30:00", "comunicacao": 8.5, "empatia": 8.5, "capacidade_resolucao": 8.5, "conhecimento": 9.0, "trabalho_equipe": 8.5, "discricao": 8.5, "honestidade": 9.0, "paciencia": 8.5, "pontualidade": 8.5, "aura": 8.5},
    {"atendente": "Milo", "data": "2026-09-22 09:45:00", "comunicacao": 9.0, "empatia": 9.0, "capacidade_resolucao": 9.0, "conhecimento": 9.0, "trabalho_equipe": 9.0, "discricao": 8.5, "honestidade": 9.0, "paciencia": 9.0, "pontualidade": 9.0, "aura": 9.0},

    # Dante
    {"atendente": "Dante", "data": "2026-07-11 14:00:00", "comunicacao": 9.0, "empatia": 8.5, "capacidade_resolucao": 9.0, "conhecimento": 9.0, "trabalho_equipe": 9.0, "discricao": 8.5, "honestidade": 9.0, "paciencia": 8.5, "pontualidade": 9.0, "aura": 8.5},
    {"atendente": "Dante", "data": "2026-07-28 09:20:00", "comunicacao": 9.0, "empatia": 9.0, "capacidade_resolucao": 9.0, "conhecimento": 9.5, "trabalho_equipe": 9.0, "discricao": 9.0, "honestidade": 9.5, "paciencia": 9.0, "pontualidade": 9.5, "aura": 9.0},
    {"atendente": "Dante", "data": "2026-08-18 15:15:00", "comunicacao": 9.5, "empatia": 9.0, "capacidade_resolucao": 9.5, "conhecimento": 9.5, "trabalho_equipe": 9.0, "discricao": 9.0, "honestidade": 9.5, "paciencia": 9.0, "pontualidade": 9.0, "aura": 9.5},
    {"atendente": "Dante", "data": "2026-09-02 11:00:00", "comunicacao": 9.0, "empatia": 9.0, "capacidade_resolucao": 9.0, "conhecimento": 9.0, "trabalho_equipe": 9.5, "discricao": 9.0, "honestidade": 9.0, "paciencia": 9.0, "pontualidade": 9.0, "aura": 9.0},
    {"atendente": "Dante", "data": "2026-09-19 16:50:00", "comunicacao": 9.5, "empatia": 9.5, "capacidade_resolucao": 9.0, "conhecimento": 9.5, "trabalho_equipe": 9.0, "discricao": 9.5, "honestidade": 9.5, "paciencia": 9.0, "pontualidade": 9.5, "aura": 9.5},

    # Zephyr
    {"atendente": "Zephyr", "data": "2026-07-15 10:30:00", "comunicacao": 9.0, "empatia": 9.0, "capacidade_resolucao": 9.5, "conhecimento": 9.5, "trabalho_equipe": 9.0, "discricao": 9.0, "honestidade": 9.5, "paciencia": 9.0, "pontualidade": 9.0, "aura": 9.0},
    {"atendente": "Zephyr", "data": "2026-07-30 14:45:00", "comunicacao": 9.5, "empatia": 9.0, "capacidade_resolucao": 9.5, "conhecimento": 9.5, "trabalho_equipe": 9.5, "discricao": 9.5, "honestidade": 9.5, "paciencia": 9.0, "pontualidade": 9.5, "aura": 9.5},
    {"atendente": "Zephyr", "data": "2026-08-20 11:20:00", "comunicacao": 9.5, "empatia": 9.5, "capacidade_resolucao": 10.0, "conhecimento": 10.0, "trabalho_equipe": 9.5, "discricao": 9.0, "honestidade": 9.5, "paciencia": 9.5, "pontualidade": 9.5, "aura": 9.5},
    {"atendente": "Zephyr", "data": "2026-09-05 16:10:00", "comunicacao": 10.0, "empatia": 9.5, "capacidade_resolucao": 9.5, "conhecimento": 9.5, "trabalho_equipe": 9.5, "discricao": 9.5, "honestidade": 10.0, "paciencia": 9.0, "pontualidade": 10.0, "aura": 9.5},
    {"atendente": "Zephyr", "data": "2026-09-20 13:00:00", "comunicacao": 9.5, "empatia": 9.5, "capacidade_resolucao": 9.5, "conhecimento": 10.0, "trabalho_equipe": 10.0, "discricao": 9.5, "honestidade": 10.0, "paciencia": 9.5, "pontualidade": 9.5, "aura": 9.5},
]

INITIAL_DENUNCIAS_DATA = [
    {
        "id": 1,
        "denunciante": "user",
        "denunciado": "Milo",
        "motivo": "Demora excessiva para responder solicitações no canal de suporte e ausência de retorno no prazo estipulado.",
        "data": "2026-09-18 14:20:10",
        "status": "em_analise",
        "comentario_admin": ""
    },
    {
        "id": 2,
        "denunciante": "user",
        "denunciado": "Dante",
        "motivo": "Uso de linguagem informal inadequada durante atendimento a cliente corporativo.",
        "data": "2026-09-12 10:15:33",
        "status": "aceita",
        "comentario_admin": "Ocorrência verificada nas gravações de atendimento. Medidas de orientação foram aplicadas."
    },
    {
        "id": 3,
        "denunciante": "Kael",
        "denunciado": "Zephyr",
        "motivo": "Divergência de horário no registro da escala de plantão compartilhado.",
        "data": "2026-09-05 08:45:00",
        "status": "recusada",
        "comentario_admin": "Ajuste de escala foi pré-aprovado pela supervisão. Registro regularizado sem infração."
    }
]


# --- INICIALIZAÇÃO E CONTROLE DE ESTADO EM MEMÓRIA ---

def init_demo_state(force: bool = False) -> None:
    """
    Inicializa ou restaura o estado de demonstração no st.session_state.
    
    Args:
        force: Quando True, força a substituição dos dados atuais pelos dados padrão de demonstração.
    """
    if force or "avaliacoes" not in st.session_state:
        st.session_state["avaliacoes"] = [dict(item) for item in INITIAL_AVALIACOES_DATA]

    if force or "denuncias" not in st.session_state:
        st.session_state["denuncias"] = [dict(item) for item in INITIAL_DENUNCIAS_DATA]

    if force or "user_photos" not in st.session_state:
        # Todos os usuários e atendentes iniciam compartilhando o avatar de perfil padrão
        photos_dict: Dict[str, bytes] = {}
        for func in FUNCIONARIOS + ["admin", "user"]:
            photos_dict[func.lower()] = DEFAULT_AVATAR_BYTES
            photos_dict[func] = DEFAULT_AVATAR_BYTES
        st.session_state["user_photos"] = photos_dict

    st.session_state["demo_initialized"] = True


def reset_demo_data() -> None:
    """
    Restaura todos os dados fictícios simulados da sessão para o estado original.
    Permite ao visitante redefinir a demonstração a qualquer momento.
    """
    init_demo_state(force=True)
    st.cache_data.clear()


# --- REPOSITÓRIO DE AVALIAÇÕES ---

def get_all_avaliacoes() -> pd.DataFrame:
    """
    Carrega todas as avaliações cadastradas na sessão em um DataFrame do Pandas.
    """
    init_demo_state()
    records = st.session_state.get("avaliacoes", [])
    if not records:
        return pd.DataFrame()
    return pd.DataFrame(records)


def insert_avaliacao(atendente: str, notas: Dict[str, float]) -> bool:
    """
    Insere uma nova avaliação no st.session_state da sessão atual.
    """
    init_demo_state()
    data_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    record = {
        "atendente": atendente,
        "data": data_str,
        **notas
    }
    
    st.session_state["avaliacoes"].append(record)
    st.cache_data.clear()
    return True


salvar_avaliacao = insert_avaliacao


# --- REPOSITÓRIO DE DENÚNCIAS ---

def get_all_denuncias() -> List[Dict[str, Any]]:
    """
    Obtém todas as denúncias para visualização e moderação administrativa.
    """
    init_demo_state()
    denuncias = st.session_state.get("denuncias", [])
    return sorted(denuncias, key=lambda x: x.get("id", 0), reverse=True)


def get_denuncias_by_user(username: str) -> List[Dict[str, Any]]:
    """
    Obtém as denúncias criadas por um usuário específico na sessão atual.
    """
    init_demo_state()
    user_clean = (username or "").strip().lower()
    denuncias = st.session_state.get("denuncias", [])
    user_denuncias = [
        d for d in denuncias 
        if str(d.get("denunciante", "")).strip().lower() == user_clean
    ]
    return sorted(user_denuncias, key=lambda x: x.get("id", 0), reverse=True)


def insert_denuncia(denunciante: str, denunciado: str, motivo: str) -> bool:
    """
    Cria um novo registro de denúncia no st.session_state.
    """
    init_demo_state()
    denuncias = st.session_state.get("denuncias", [])
    next_id = max([d.get("id", 0) for d in denuncias] or [0]) + 1
    data_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    record = {
        "id": next_id,
        "denunciante": denunciante,
        "denunciado": denunciado,
        "motivo": motivo,
        "data": data_str,
        "status": "em_analise",
        "comentario_admin": ""
    }

    denuncias.append(record)
    st.cache_data.clear()
    return True


salvar_denuncia = insert_denuncia


def update_denuncia_status(denuncia_id: Any, status: str, comentario_admin: str = "") -> bool:
    """
    Atualiza o status e comentário administrativo de uma denúncia existente no session_state.
    """
    init_demo_state()
    denuncias = st.session_state.get("denuncias", [])
    
    for d in denuncias:
        if str(d.get("id")) == str(denuncia_id):
            d["status"] = status
            d["comentario_admin"] = comentario_admin
            st.cache_data.clear()
            return True
            
    return False


atualizar_status_denuncia = update_denuncia_status


# --- REPOSITÓRIO DE PERFIL E FOTOS (MEMÓRIA / BASE64) ---

def save_user_profile_photo(username: str, file_bytes: bytes) -> bool:
    """
    Armazena a foto de perfil do usuário diretamente na memória de sessão (st.session_state).
    Permite atualização personalizada pelo usuário, mantendo total isolamento.
    """
    init_demo_state()
    safe_user = sanitize_filename(username).lower()
    st.session_state["user_photos"][safe_user] = file_bytes
    st.session_state["user_photos"][username] = file_bytes
    st.cache_data.clear()
    return True


salvar_foto_perfil = save_user_profile_photo


def get_user_profile_photo(username: str) -> Optional[bytes]:
    """
    Recupera os bytes da foto de perfil a partir do st.session_state.
    Retorna a foto personalizada do usuário se houver, ou a foto de perfil padrão para todos.
    """
    init_demo_state()
    safe_user = sanitize_filename(username).lower()
    photos = st.session_state.get("user_photos", {})
    
    # 1. Busca por nome sanitizado ou exato no session_state
    if safe_user in photos and photos[safe_user]:
        return photos[safe_user]
    if username in photos and photos[username]:
        return photos[username]
        
    # 2. Retorna a mesma foto de perfil padrão para todos
    return DEFAULT_AVATAR_BYTES
