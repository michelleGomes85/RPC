
from rpc.server import Server

# Configurações servidor outros servidores (isPrimem wait() ...)
UTILITY_SERVER = {
    'IP': '127.0.0.1',  # IP do servidor
    'PORT': 5003         # Porta do servidor
}

if __name__ == "__main__":
    Server(UTILITY_SERVER['IP'], UTILITY_SERVER['PORT']).start()
