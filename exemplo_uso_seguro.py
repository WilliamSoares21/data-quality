#!/usr/bin/env python3
"""
Exemplo de uso do módulo de segurança safe_nbconvert.

Este script demonstra como converter notebooks Jupyter de forma segura,
protegendo contra a vulnerabilidade CVE-2025-53000.
"""

from utils.safe_nbconvert import safe_convert_to_pdf, safe_convert, NBConvertSecurityError


def exemplo_1_conversao_pdf_basica():
    """Exemplo básico de conversão para PDF."""
    print("Exemplo 1: Conversão básica para PDF")
    print("-" * 50)
    
    try:
        # Substitua 'seu_notebook.ipynb' pelo caminho do seu notebook
        resultado = safe_convert_to_pdf('seu_notebook.ipynb')
        print(f"✓ Conversão concluída: {resultado}")
    except FileNotFoundError:
        print("⊘ Notebook de exemplo não encontrado (esperado)")
    except NBConvertSecurityError as e:
        print(f"✗ ALERTA DE SEGURANÇA: {e}")
    except Exception as e:
        print(f"✗ Erro: {e}")
    
    print()


def exemplo_2_conversao_html_alternativa():
    """Exemplo de conversão para HTML (alternativa mais segura)."""
    print("Exemplo 2: Conversão para HTML (recomendado)")
    print("-" * 50)
    
    try:
        # HTML não é afetado pela vulnerabilidade CVE-2025-53000
        resultado = safe_convert('seu_notebook.ipynb', 'html', 'relatorio.html')
        print(f"✓ Conversão concluída: {resultado}")
    except FileNotFoundError:
        print("⊘ Notebook de exemplo não encontrado (esperado)")
    except Exception as e:
        print(f"✗ Erro: {e}")
    
    print()


def exemplo_3_conversao_com_execucao():
    """Exemplo de conversão executando o notebook antes."""
    print("Exemplo 3: Conversão com execução do notebook")
    print("-" * 50)
    
    try:
        # Executa todas as células antes de converter
        resultado = safe_convert_to_pdf(
            'seu_notebook.ipynb',
            'relatorio_executado.pdf',
            execute=True,
            allow_errors=False
        )
        print(f"✓ Conversão concluída: {resultado}")
    except FileNotFoundError:
        print("⊘ Notebook de exemplo não encontrado (esperado)")
    except NBConvertSecurityError as e:
        print(f"✗ ALERTA DE SEGURANÇA: {e}")
    except Exception as e:
        print(f"✗ Erro: {e}")
    
    print()


def exemplo_4_multiplos_formatos():
    """Exemplo convertendo para múltiplos formatos."""
    print("Exemplo 4: Conversão para múltiplos formatos")
    print("-" * 50)
    
    formatos = ['html', 'markdown', 'pdf']
    
    for formato in formatos:
        try:
            print(f"  Convertendo para {formato.upper()}...", end=" ")
            resultado = safe_convert('seu_notebook.ipynb', formato)
            print(f"✓ {resultado}")
        except FileNotFoundError:
            print("⊘ (notebook não encontrado)")
        except NBConvertSecurityError as e:
            print(f"✗ ALERTA: {str(e).splitlines()[0]}")
        except Exception as e:
            print(f"✗ Erro: {str(e).splitlines()[0]}")
    
    print()


if __name__ == '__main__':
    print("=" * 60)
    print("Exemplos de Uso: Módulo de Segurança safe_nbconvert")
    print("=" * 60)
    print()
    
    exemplo_1_conversao_pdf_basica()
    exemplo_2_conversao_html_alternativa()
    exemplo_3_conversao_com_execucao()
    exemplo_4_multiplos_formatos()
    
    print("=" * 60)
    print("Dicas:")
    print("=" * 60)
    print("• Sempre use safe_convert_to_pdf() ao invés de jupyter nbconvert")
    print("• Prefira HTML para visualização (não tem vulnerabilidade)")
    print("• Execute ./check_security.sh periodicamente")
    print("• Leia utils/SECURITY_README.md para mais informações")
    print()
