

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

# Configurações do servidor de nomes
NAME_SERVER = {
    'IP': '127.0.0.1', 
    'PORT': 5000       
}

LOG_SERVER_NAME_CLOSED = "\nEncerrando o servidor de nomes..."
LOG_SERVER_NAME_START = "Servidor de nomes rodando em {ip}:{port}"
KEY_OPERATION = "operation"
ERROR_KEY_OPERATION_MISSING = "Chave \"operation\" ausente na solicitação."
LOG_REQUEST_RECEIVED = "Solicitação recebida de {addr}: operação = {operation}"
LOG_OPERATION_NOT_FOUND = "Operação '{operation}' não encontrada."

ERROR = "error"
ERROR_UNKNOWN_OPERATION = "Operação desconhecida solicitada: {operation}"
ERROR_FORMAT_WRONG = "Solicitação inválida. Esperado formato JSON."
ERROR_INTERNAL = "Erro interno no servidor de nomes."
