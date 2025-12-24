"""
Módulo de segurança para mitigar CVE-2025-53000 (CWE-427) no nbconvert.

Este módulo fornece uma camada de proteção contra a vulnerabilidade de execução
de código não autorizado ao converter notebooks contendo SVG para PDF no Windows.

Uso:
    from utils.safe_nbconvert import safe_convert_to_pdf
    
    safe_convert_to_pdf('notebook.ipynb', 'output.pdf')
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
from typing import Optional, List
import warnings


class NBConvertSecurityError(Exception):
    """Exceção levantada quando uma ameaça de segurança é detectada."""
    pass


def _check_malicious_files(directory: str) -> None:
    """
    Verifica se há arquivos suspeitos (inkscape.bat) no diretório.
    
    Args:
        directory: Diretório a ser verificado
        
    Raises:
        NBConvertSecurityError: Se arquivos maliciosos forem detectados
    """
    if os.name != 'nt':
        return
    
    suspicious_files = ['inkscape.bat', 'inkscape.cmd']
    dir_path = Path(directory)
    
    for sus_file in suspicious_files:
        file_path = dir_path / sus_file
        if file_path.exists():
            raise NBConvertSecurityError(
                f"ALERTA DE SEGURANÇA: Arquivo suspeito detectado: {file_path}\n"
                f"Este arquivo pode ser uma tentativa de exploração da CVE-2025-53000.\n"
                f"Remova o arquivo antes de prosseguir."
            )


def _get_safe_inkscape_path() -> Optional[str]:
    """
    Retorna o caminho completo e seguro do executável inkscape.
    
    Returns:
        Caminho completo para o inkscape ou None se não encontrado
    """
    if os.name != 'nt':
        return shutil.which('inkscape')
    
    # Caminhos padrão do Inkscape no Windows
    common_paths = [
        r"C:\Program Files\Inkscape\bin\inkscape.exe",
        r"C:\Program Files (x86)\Inkscape\bin\inkscape.exe",
        os.path.expandvars(r"%PROGRAMFILES%\Inkscape\bin\inkscape.exe"),
        os.path.expandvars(r"%PROGRAMFILES(X86)%\Inkscape\bin\inkscape.exe"),
    ]
    
    for path in common_paths:
        if os.path.isfile(path):
            return path
    
    # Tenta encontrar via PATH, mas apenas em caminhos absolutos seguros
    inkscape_path = shutil.which('inkscape')
    if inkscape_path and os.path.isabs(inkscape_path):
        return inkscape_path
    
    return None


def safe_convert_to_pdf(
    input_notebook: str,
    output_pdf: Optional[str] = None,
    execute: bool = False,
    allow_errors: bool = False,
    extra_args: Optional[List[str]] = None
) -> str:
    """
    Converte um notebook Jupyter para PDF de forma segura.
    
    Esta função mitiga a CVE-2025-53000 verificando arquivos maliciosos
    e usando caminhos absolutos para o executável inkscape.
    
    Args:
        input_notebook: Caminho para o notebook .ipynb
        output_pdf: Caminho para o PDF de saída (opcional)
        execute: Se True, executa o notebook antes da conversão
        allow_errors: Se True, permite erros durante a execução
        extra_args: Argumentos adicionais para nbconvert
        
    Returns:
        Caminho para o arquivo PDF gerado
        
    Raises:
        NBConvertSecurityError: Se uma ameaça de segurança for detectada
        FileNotFoundError: Se o notebook de entrada não existir
        subprocess.CalledProcessError: Se a conversão falhar
    """
    input_path = Path(input_notebook).resolve()
    
    if not input_path.exists():
        raise FileNotFoundError(f"Notebook não encontrado: {input_path}")
    
    # Verifica segurança no diretório de trabalho
    _check_malicious_files(input_path.parent)
    _check_malicious_files(os.getcwd())
    
    # Prepara ambiente seguro
    env = os.environ.copy()
    
    if os.name == 'nt':
        inkscape_path = _get_safe_inkscape_path()
        if inkscape_path:
            env['INKSCAPE'] = inkscape_path
            warnings.warn(
                f"Usando Inkscape seguro: {inkscape_path}",
                UserWarning
            )
        else:
            warnings.warn(
                "Inkscape não encontrado. A conversão de SVG pode falhar.",
                UserWarning
            )
    
    # Monta comando de conversão
    cmd = ['jupyter', 'nbconvert', '--to', 'pdf']
    
    if execute:
        cmd.append('--execute')
    
    if allow_errors:
        cmd.append('--allow-errors')
    
    if output_pdf:
        cmd.extend(['--output', str(Path(output_pdf).resolve())])
    
    if extra_args:
        cmd.extend(extra_args)
    
    cmd.append(str(input_path))
    
    # Executa conversão
    try:
        result = subprocess.run(
            cmd,
            env=env,
            capture_output=True,
            text=True,
            check=True,
            cwd=str(input_path.parent)
        )
        
        if output_pdf:
            output_path = Path(output_pdf).resolve()
        else:
            output_path = input_path.with_suffix('.pdf')
        
        return str(output_path)
        
    except subprocess.CalledProcessError as e:
        raise subprocess.CalledProcessError(
            e.returncode,
            e.cmd,
            output=e.stdout,
            stderr=f"Erro na conversão:\n{e.stderr}"
        )


def safe_convert(
    input_notebook: str,
    output_format: str = 'html',
    output_file: Optional[str] = None,
    execute: bool = False,
    extra_args: Optional[List[str]] = None
) -> str:
    """
    Converte um notebook Jupyter para qualquer formato de forma segura.
    
    Para formato PDF, usa proteção adicional contra CVE-2025-53000.
    
    Args:
        input_notebook: Caminho para o notebook .ipynb
        output_format: Formato de saída (html, pdf, markdown, etc.)
        output_file: Caminho para o arquivo de saída (opcional)
        execute: Se True, executa o notebook antes da conversão
        extra_args: Argumentos adicionais para nbconvert
        
    Returns:
        Caminho para o arquivo gerado
    """
    if output_format.lower() == 'pdf':
        return safe_convert_to_pdf(
            input_notebook,
            output_file,
            execute=execute,
            extra_args=extra_args
        )
    
    input_path = Path(input_notebook).resolve()
    
    if not input_path.exists():
        raise FileNotFoundError(f"Notebook não encontrado: {input_path}")
    
    cmd = ['jupyter', 'nbconvert', '--to', output_format]
    
    if execute:
        cmd.append('--execute')
    
    if output_file:
        cmd.extend(['--output', str(Path(output_file).resolve())])
    
    if extra_args:
        cmd.extend(extra_args)
    
    cmd.append(str(input_path))
    
    subprocess.run(cmd, check=True, cwd=str(input_path.parent))
    
    if output_file:
        return str(Path(output_file).resolve())
    else:
        return str(input_path.with_suffix(f'.{output_format}'))


if __name__ == '__main__':
    # Exemplo de uso via linha de comando
    if len(sys.argv) < 2:
        print("Uso: python safe_nbconvert.py <notebook.ipynb> [formato] [saida]")
        sys.exit(1)
    
    notebook = sys.argv[1]
    fmt = sys.argv[2] if len(sys.argv) > 2 else 'html'
    output = sys.argv[3] if len(sys.argv) > 3 else None
    
    try:
        result = safe_convert(notebook, fmt, output)
        print(f"✓ Conversão concluída: {result}")
    except Exception as e:
        print(f"✗ Erro: {e}", file=sys.stderr)
        sys.exit(1)
