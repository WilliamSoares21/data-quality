"""
Módulo de Autenticação e Controle de Acesso Baseado em Papéis (RBAC).
Implementa hashing seguro de senhas (Argon2id/Bcrypt) e guardas declarativos de acesso com st.stop().
"""

import hmac
import streamlit as st
from passlib.context import CryptContext

# Configuração do contexto de criptografia (suporta Argon2id e Bcrypt)
pwd_context = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Gera um hash seguro de senha utilizando Argon2id/Bcrypt com salt automático."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, stored_credential: str) -> bool:
    """
    Verifica a senha informada contra a credencial armazenada.
    Suporta hashes de senhas e fallback seguro com hmac.compare_digest se for plaintext.
    """
    if not plain_password or not stored_credential:
        return False
        
    try:
        # Tenta verificar se a credencial armazenada é um hash seguro válido
        if stored_credential.startswith(("$argon2", "$2b$", "$2a$", "$2y$")):
            return pwd_context.verify(plain_password, stored_credential)
    except Exception:
        pass

    # Fallback seguro para comparação em tempo constante contra plaintext (compatibilidade temporária)
    return hmac.compare_digest(stored_credential.encode("utf-8"), plain_password.encode("utf-8"))

def check_permission(required_role: str = None) -> None:
    """
    Guarda declarativo de autorização RBAC.
    Interrompe a execução imediatamente com st.stop() se o usuário não estiver autenticado
    ou se não possuir o perfil necessário.
    """
    if not st.session_state.get("logged_in", False):
        st.error("⛔ **Acesso Negado**: Você precisa estar autenticado para acessar esta funcionalidade.")
        st.info("Por favor, faça login através da tela inicial.")
        st.stop()
        
    if required_role and st.session_state.get("role") != required_role:
        st.error(f"⛔ **Acesso Negado**: Esta página requer nível de permissão '{required_role}'.")
        st.warning(f"Seu perfil atual ('{st.session_state.get('role')}') não possui privilégios suficientes.")
        st.stop()

def get_user_credentials_from_secrets(username: str):
    """Recupera credenciais do st.secrets de forma segura."""
    if "passwords" not in st.secrets or "roles" not in st.secrets:
        return None, None
        
    passwords_dict = st.secrets["passwords"]
    roles_dict = st.secrets["roles"]
    
    if username in passwords_dict and username in roles_dict:
        return passwords_dict[username], roles_dict[username]
        
    return None, None

def login(username: str, password: str, repo_get_user_fn=None) -> bool:
    """
    Autentica o usuário validando as credenciais no repositório de dados ou secrets.toml.
    Define o estado da sessão centralizado.
    """
    if not username or not password:
        return False

    stored_pass = None
    role = None

    # 1. Tentar buscar do banco de dados se a função de repositório for fornecida
    if repo_get_user_fn:
        user_data = repo_get_user_fn(username)
        if user_data:
            stored_pass = user_data.get("password")
            role = user_data.get("role", "user")

    # 2. Fallback para st.secrets caso não esteja no DB
    if not stored_pass:
        stored_pass, role = get_user_credentials_from_secrets(username)

    if stored_pass and verify_password(password, stored_pass):
        st.session_state.logged_in = True
        st.session_state.username = username
        st.session_state.role = role or "user"
        st.session_state.user_id = username
        return True

    return False

def logout() -> None:
    """Encerra a sessão do usuário de forma limpa."""
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.role = None
    st.session_state.user_id = None