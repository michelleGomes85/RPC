
from rpc.server import Server

# Configurações servidor (adição e subtração)
ARITH_SERVER1 = {
    'IP': '127.0.0.1',  # IP do servidor
    'PORT': 5001         # Porta do servidor
}

SERVER_NAME = "server_arith1.txt"

if __name__ == "__main__":
    Server(ARITH_SERVER1['IP'], ARITH_SERVER1['PORT'], SERVER_NAME).start()
