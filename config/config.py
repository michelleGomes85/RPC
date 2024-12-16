# constants.py

# Configurações do servidor de nomes
NAME_SERVER = {
    'IP': '127.0.0.1',  # IP do servidor
    'PORT': 5000         # Porta do servidor
}

# Configurações servidor geral
SERVER_CONFIG = {
    'IP': '127.0.0.1',  # IP do servidor
    'PORT': 5001         # Porta do servidor
}

# Configurações servidor (adição e subtração)
ARITH_SERVER1 = {
    'IP': '127.0.0.1',  # IP do servidor
    'PORT': 5001         # Porta do servidor
}

# Configurações servidor (multiplicação e divisão)
ARITH_SERVER2 = {
    'IP': '127.0.0.1',  # IP do servidor
    'PORT': 5002         # Porta do servidor
}

# Configurações servidor outros servidores (multiplicação e divisão)
UTILITY_SERVER = {
    'IP': '127.0.0.1',  # IP do servidor
    'PORT': 5003         # Porta do servidor
}

# Operações suportadas
OPERATIONS = {
    'SUM': 'SUM',
    'SUB': 'SUB',
    'MUL': 'MUL',
    'DIV': 'DIV',
    'WAIT': 'WAIT',
    'CHECK_PRIMES': 'CHECK_PRIMES',
    'CHECK_PRIMES_PARALLEL': 'CHECK_PRIMES_PARALLEL'
}

# Codificação de mensagens
ENCODING = 'utf-8'

# Mensagens de erro
ERROR_MESSAGE = "ERROR"
DIV_ZERO_ERROR = "Divisão por zero."
INVALID_OPERATION = "Operação inválida ou argumentos insuficientes."
INVALID_JSON_FORMAT = "Formato de JSON inválido."
ERROR_NUMBER_PROCESS = "Número de processos acima do esperado"

# Mensagens de Log
LOG_SERVER_START = "Servidor escutando em {ip}:{port}"
LOG_CONNECTION_ESTABLISHED = "\nConexão estabelecida com {address}"
LOG_CONNECTION_CLOSED = "Conexão com o cliente {address} encerrada."
LOG_CLIENT_ERROR = "Erro ao processar o cliente {address}: {error}"


# Definir se servidor vai usar thread ou processo, para fazer o paralelismo
THREAD_PROCESS = True

# Tamanho do buffer de recepção
BUFFER_SIZE = 1024

# Delimitador de mensagem
MESSAGE_DELIMITER = b'\n'

# Estrutura de JSON para requisições
REQUEST_KEYS = {
    'OPERATION': 'operation',
    'VALUES': 'values'
}

# Números de registros máximo do cache em memória
N_CACHE_MEMORY = 2

# Números de registros máximo do cache em disco
N_CACHE_DISK = 100

#Nome do arquivo de cache em disco
NAME_CACHE_DISK = "cache/prime_cache.json"

# Map de operações para IPs e portas dos servidores
SERVER_MAP = {
    "SUM": [{"IP": "127.0.0.1", "PORT": 5001}],
    "SUB": [{"IP": "127.0.0.1", "PORT": 5001}],
    "MUL": [{"IP": "127.0.0.1", "PORT": 5002}],
    "DIV": [{"IP": "127.0.0.1", "PORT": 5002}],
    "WAIT": [{"IP": "127.0.0.1", "PORT": 5003}],
    "CHECK_PRIMES": [{"IP": "127.0.0.1", "PORT": 5003}],
    "CHECK_PRIMES_PARALLEL": [{"IP": "127.0.0.1", "PORT": 5003}]
}