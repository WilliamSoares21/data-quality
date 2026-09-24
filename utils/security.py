"""
Módulo de Utilidades de Segurança (AppSec)
Fornece funções para sanitização de arquivos, prevenção de Path Traversal e validação de uploads.
"""

import os
from pathlib import Path
from typing import Tuple, Optional
from werkzeug.utils import secure_filename
import streamlit as st

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}
MAX_FILE_SIZE_MB = 5

def sanitize_filename(filename: str) -> str:
    """
    Sanitiza um nome de arquivo para prevenir Path Traversal e Injeção de Comandos.
    Remove sequências perigosas como '../', slashes e caracteres de controle.
    """
    if not filename:
        return ""
    # Utiliza secure_filename do Werkzeug para limpar o nome do arquivo
    clean_name = secure_filename(os.path.basename(filename))
    return clean_name

def validate_uploaded_file(uploaded_file, max_size_mb: int = MAX_FILE_SIZE_MB) -> Tuple[bool, Optional[str]]:
    """
    Valida a extensão, o tipo MIME e o tamanho de um arquivo enviado.
    Retorna (is_valid, error_message).
    """
    if uploaded_file is None:
        return False, "Nenhum arquivo enviado."
    
    # 1. Sanitizar nome do arquivo
    clean_name = sanitize_filename(uploaded_file.name)
    if not clean_name:
        return False, "Nome de arquivo inválido."
    
    # 2. Validar extensão
    ext = Path(clean_name).suffix.lstrip(".").lower()
    if ext not in ALLOWED_EXTENSIONS:
        return False, f"Extensão de arquivo não permitida ('.{ext}'). Extensões permitidas: {', '.join(ALLOWED_EXTENSIONS)}"
    
    # 3. Validar tamanho do arquivo
    file_bytes = uploaded_file.getvalue()
    size_mb = len(file_bytes) / (1024 * 1024)
    if size_mb > max_size_mb:
        return False, f"Tamanho do arquivo ({size_mb:.2f} MB) excede o limite máximo de {max_size_mb} MB."
    
    return True, None

def get_safe_filepath(base_dir: str, filename: str) -> str:
    """
    Garante que o caminho final do arquivo esteja estritamente restrito ao base_dir.
    Evita Path Traversal mesmo que o sistema de arquivos receba caminhos relativos.
    """
    base_path = Path(base_dir).resolve()
    clean_name = sanitize_filename(filename)
    target_path = (base_path / clean_name).resolve()
    
    # Verificar se o target_path ainda está dentro do base_path
    if not str(target_path).startswith(str(base_path)):
        raise ValueError("Tentativa de Path Traversal detectada!")
        
    return str(target_path)
