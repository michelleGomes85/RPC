
from rpc.server import Server
from config.config import ARITH_SERVER2

if __name__ == "__main__":
    Server(ARITH_SERVER2['IP'], ARITH_SERVER2['PORT']).start()
