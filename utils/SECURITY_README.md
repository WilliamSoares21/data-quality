# Guia de Uso: Mitigação CVE-2025-53000

## Visão Geral

Este módulo protege contra a vulnerabilidade **CVE-2025-53000** (CWE-427: Uncontrolled Search Path) no `nbconvert`, que permite execução de código não autorizado no Windows.

## Instalação

O módulo já está instalado em `utils/safe_nbconvert.py`

## Uso Básico

### 1. Conversão para PDF (Protegido)

```python
from utils.safe_nbconvert import safe_convert_to_pdf

# Conversão simples
safe_convert_to_pdf('meu_notebook.ipynb')

# Com arquivo de saída customizado
safe_convert_to_pdf('meu_notebook.ipynb', 'relatorio.pdf')

# Executar notebook antes de converter
safe_convert_to_pdf('meu_notebook.ipynb', execute=True)
```

### 2. Conversão para Outros Formatos

```python
from utils.safe_nbconvert import safe_convert

# HTML (recomendado como alternativa ao PDF)
safe_convert('meu_notebook.ipynb', 'html')

# Markdown
safe_convert('meu_notebook.ipynb', 'markdown', 'README.md')

# Slides
safe_convert('meu_notebook.ipynb', 'slides')
```

### 3. Linha de Comando

```bash
# Conversão para HTML
python utils/safe_nbconvert.py notebook.ipynb html

# Conversão para PDF
python utils/safe_nbconvert.py notebook.ipynb pdf output.pdf
```

## Proteções Implementadas

1. **Verificação de Arquivos Maliciosos**: Detecta `inkscape.bat` suspeito
2. **Caminho Absoluto**: Usa caminho completo para executáveis
3. **Isolamento de Ambiente**: Variáveis de ambiente controladas
4. **Validação de Entrada**: Verifica existência de arquivos

## Tratamento de Erros

```python
from utils.safe_nbconvert import safe_convert_to_pdf, NBConvertSecurityError

try:
    safe_convert_to_pdf('notebook.ipynb')
except NBConvertSecurityError as e:
    print(f"Ameaça de segurança detectada: {e}")
except FileNotFoundError as e:
    print(f"Arquivo não encontrado: {e}")
```

## Recomendações

- ✅ Use `safe_convert_to_pdf()` ao invés de `jupyter nbconvert --to pdf`
- ✅ Prefira conversão HTML quando possível (não afetado pela vulnerabilidade)
- ✅ Mantenha nbconvert atualizado: `pip install --upgrade nbconvert`
- ⚠️ Monitore: https://github.com/jupyter/nbconvert/security/advisories

## Status da Vulnerabilidade

- **CVE**: CVE-2025-53000
- **Afetado**: nbconvert <= 7.16.6 (versão atual)
- **Plataforma**: Apenas Windows
- **Status**: Patch oficial ainda não disponível
- **Mitigação**: Este módulo implementa workaround recomendado
