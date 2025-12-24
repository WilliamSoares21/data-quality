"""
Testes básicos para o módulo safe_nbconvert.
"""

import os
import sys
import tempfile
from pathlib import Path

# Adiciona o diretório pai ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.safe_nbconvert import (
    _check_malicious_files,
    _get_safe_inkscape_path,
    NBConvertSecurityError
)


def test_malicious_file_detection():
    """Testa a detecção de arquivos maliciosos."""
    print("Testando detecção de arquivos maliciosos...")
    
    if os.name != 'nt':
        print("  ⊘ Teste pulado (não é Windows)")
        return
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Cria arquivo suspeito
        malicious_file = Path(tmpdir) / "inkscape.bat"
        malicious_file.write_text("@echo You've been hacked!")
        
        try:
            _check_malicious_files(tmpdir)
            print("  ✗ FALHOU: Deveria ter detectado arquivo malicioso")
        except NBConvertSecurityError as e:
            print(f"  ✓ PASSOU: {str(e).splitlines()[0]}")


def test_inkscape_path():
    """Testa a detecção do caminho do Inkscape."""
    print("Testando detecção do Inkscape...")
    
    inkscape_path = _get_safe_inkscape_path()
    
    if inkscape_path:
        print(f"  ✓ Inkscape encontrado: {inkscape_path}")
    else:
        print("  ⊘ Inkscape não encontrado (OK se não estiver instalado)")


def test_import():
    """Testa se o módulo pode ser importado."""
    print("Testando importação do módulo...")
    
    try:
        from utils.safe_nbconvert import safe_convert_to_pdf, safe_convert
        print("  ✓ Módulo importado com sucesso")
        return True
    except Exception as e:
        print(f"  ✗ Erro na importação: {e}")
        return False


def main():
    """Executa todos os testes."""
    print("=" * 60)
    print("Testes do Módulo de Segurança safe_nbconvert")
    print("=" * 60)
    print()
    
    if not test_import():
        sys.exit(1)
    
    test_malicious_file_detection()
    test_inkscape_path()
    
    print()
    print("=" * 60)
    print("✓ Testes básicos concluídos")
    print("=" * 60)


if __name__ == '__main__':
    main()
