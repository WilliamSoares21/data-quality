"""
Módulo de Conexão e Gerenciamento de Estado de Demonstração em Memória.
Substitui completamente bancos de dados externos por persistência volátil em st.session_state,
garantindo isolamento por sessão de usuário, conformidade AppSec e zero custos de infraestrutura.
"""

import streamlit as st
from typing import Any


def init_demo_data(force: bool = False) -> None:
    """
    Inicializa o st.session_state com os datasets simulados de demonstração (Mock Data),
    caso ainda não tenham sido carregados na sessão do usuário.
    
    Args:
        force: Se True, reinicializa todos os dados para o estado padrão original.
    """
    from database.repository import init_demo_state
    init_demo_state(force=force)


def get_database() -> dict[str, Any]:
    """
    Provedor de contexto de dados em memória.
    Mantido para compatibilidade arquitetural com a camada de serviços.
    """
    init_demo_data()
    return {
        "type": "memory",
        "session": st.session_state
    }
