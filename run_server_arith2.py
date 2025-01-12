
from rpc.server import Server

# Configurações servidor (multiplicação e divisão)
ARITH_SERVER2 = {
    'IP': '127.0.0.1',  # IP do servidor
    'PORT': 5002         # Porta do servidor
}

if __name__ == "__main__":
    Server(ARITH_SERVER2['IP'], ARITH_SERVER2['PORT']).start()
