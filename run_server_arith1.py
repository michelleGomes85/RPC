
from rpc.server import Server
from config.config_server import ARITH_SERVER1

if __name__ == "__main__":
    Server(ARITH_SERVER1['IP'], ARITH_SERVER1['PORT']).start()
