#!/bin/bash
# =============================================================================
# lab_setup_check.sh — Verificação do Ambiente de Laboratório
# Uso: Execute no Kali Linux antes de iniciar os cenários de teste.
# =============================================================================

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

TARGET=${1:-"192.168.56.102"}

echo ""
echo "============================================="
echo "  🔐 Verificação do Ambiente de Laboratório"
echo "============================================="
echo "  Alvo: $TARGET"
echo "============================================="
echo ""

# --- 1. Verificar ferramentas necessárias ---
echo "📦 [1/4] Verificando ferramentas instaladas..."

tools=("medusa" "nmap" "enum4linux" "smbclient" "ftp" "curl")
all_ok=true

for tool in "${tools[@]}"; do
    if command -v "$tool" &>/dev/null; then
        echo -e "  ${GREEN}✔${NC} $tool encontrado: $(which $tool)"
    else
        echo -e "  ${RED}✘${NC} $tool NÃO encontrado"
        all_ok=false
    fi
done

if $all_ok; then
    echo -e "\n  ${GREEN}Todas as ferramentas estão disponíveis.${NC}"
else
    echo -e "\n  ${YELLOW}Instale as ferramentas faltantes:${NC}"
    echo "  sudo apt update && sudo apt install -y medusa nmap enum4linux smbclient"
fi

echo ""

# --- 2. Verificar conectividade com o alvo ---
echo "🌐 [2/4] Verificando conectividade com $TARGET..."

if ping -c 2 -W 2 "$TARGET" &>/dev/null; then
    echo -e "  ${GREEN}✔${NC} Alvo $TARGET está alcançável (ping OK)"
else
    echo -e "  ${RED}✘${NC} Alvo $TARGET NÃO responde ao ping"
    echo "  Verifique se a VM Metasploitable está ligada e na rede host-only."
fi

echo ""

# --- 3. Verificar serviços no alvo com Nmap ---
echo "🔍 [3/4] Escaneando serviços no alvo com Nmap..."

if command -v nmap &>/dev/null; then
    echo "  Executando: nmap -sV -p 21,80,139,445 $TARGET"
    echo "  (Aguarde...)"
    echo ""
    nmap -sV -p 21,80,139,445 "$TARGET" 2>/dev/null | grep -E "PORT|open|closed|filtered"
else
    echo -e "  ${RED}✘${NC} Nmap não instalado. Pulando esta etapa."
fi

echo ""

# --- 4. Verificar wordlists ---
echo "📄 [4/4] Verificando wordlists..."

wordlists=(
    "../wordlists/usuarios.txt"
    "../wordlists/senhas.txt"
    "/usr/share/wordlists/rockyou.txt"
)

for wl in "${wordlists[@]}"; do
    if [ -f "$wl" ]; then
        count=$(wc -l < "$wl")
        echo -e "  ${GREEN}✔${NC} $wl ($count entradas)"
    else
        echo -e "  ${YELLOW}⚠${NC} $wl não encontrada"
    fi
done

echo ""
echo "============================================="
echo "  ✅ Verificação concluída!"
echo "  Siga os cenários documentados no README.md"
echo "============================================="
echo ""
