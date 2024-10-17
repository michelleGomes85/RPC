# constants.py

# Configurações do servidor
SERVER_CONFIG = {
    'IP': '127.0.0.1',  # IP do servidor
    'PORT': 5000         # Porta do servidor
}

# Operações suportadas
OPERATIONS = {
    'SUM': 'sum',
    'SUB': 'sub',
    'MUL': 'mul',
    'DIV': 'div'
}

# Codificação de mensagens
ENCODING = 'utf-8'

# Mensagens de erro
ERROR_MESSAGE = "ERROR"
DIV_ZERO_ERROR = "Divisão por zero."
INVALID_OPERATION = "Operação inválida ou argumentos insuficientes."
INVALID_JSON_FORMAT = "Formato de JSON inválido."

# Tamanho do buffer de recepção
BUFFER_SIZE = 1024

# Estrutura de JSON para requisições
REQUEST_KEYS = {
    'OPERATION': 'operation',
    'VALUES': 'values'
}
