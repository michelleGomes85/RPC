# constants.py

# Configurações servidor geral
SERVER_CONFIG = {
    'IP': '127.0.0.1',  # IP do servidor
    'PORT': 5000         # Porta do servidor
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

# Definir se servidor vai usar thread ou processo, para fazer o paralelismo
THREAD_PROCESS = True

# Estrutura de JSON para requisições
REQUEST_KEYS = {
    'OPERATION': 'operation',
    'VALUES': 'values'
}

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

LOG_SERVER_CLOSED = "\nServidor encerrado."

