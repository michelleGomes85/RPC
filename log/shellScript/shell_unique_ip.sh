#!/bin/bash

# Verifica se o arquivo de log foi fornecido como argumento
if [ $# -ne 1 ]; then
    echo "Uso: $0 <arquivo_de_log>"
    exit 1
fi

# Extrai os IPs únicos do arquivo de log
awk -F', ' '{print $2}' "$1" | sort | uniq
