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
    'DIV': 'div',
    'WAIT': 'wait',
    'CHECK_PRIMES': 'check_primes',
    'CHECK_PRIMES_PARALLEL': 'check_primes_parallel'
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
N_CACHE_DISK = 2