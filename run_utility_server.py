
from rpc.server import Server
from config.config import UTILITY_SERVER

if __name__ == "__main__":
    Server(UTILITY_SERVER['IP'], UTILITY_SERVER['PORT']).start()
