#!/bin/bash
# Script de verificação de segurança para CVE-2025-53000
# Execute este script periodicamente para verificar vulnerabilidades

echo "=========================================="
echo "Verificação de Segurança - nbconvert"
echo "=========================================="
echo ""

# Verifica versão do nbconvert
echo "1. Versão do nbconvert instalada:"
pip show nbconvert | grep "Version"
echo ""

# Verifica arquivos suspeitos no diretório atual (Windows)
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    echo "2. Verificando arquivos suspeitos..."
    if [ -f "inkscape.bat" ] || [ -f "inkscape.cmd" ]; then
        echo "   ⚠️  ALERTA: Arquivo suspeito detectado!"
        ls -la inkscape.* 2>/dev/null
    else
        echo "   ✓ Nenhum arquivo suspeito encontrado"
    fi
    echo ""
fi

# Verifica se o módulo de segurança está disponível
echo "3. Módulo de segurança:"
if [ -f "utils/safe_nbconvert.py" ]; then
    echo "   ✓ utils/safe_nbconvert.py instalado"
else
    echo "   ✗ Módulo de segurança não encontrado!"
fi
echo ""

# Escaneia vulnerabilidades conhecidas (se pip-audit estiver instalado)
echo "4. Escaneando vulnerabilidades conhecidas..."
if command -v pip-audit &> /dev/null; then
    pip-audit --desc 2>/dev/null | grep -A3 "nbconvert" || echo "   ✓ Nenhuma vulnerabilidade adicional detectada"
else
    echo "   ⊘ pip-audit não instalado (execute: pip install pip-audit)"
fi
echo ""

echo "=========================================="
echo "Recomendações:"
echo "=========================================="
echo "• Use utils/safe_nbconvert.py para conversões PDF"
echo "• Prefira HTML ao invés de PDF quando possível"
echo "• Monitore: https://github.com/jupyter/nbconvert/security"
echo ""
