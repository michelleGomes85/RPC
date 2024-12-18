
from rpc.name_server import NameServer
from config.config_server_name import NAME_SERVER

if __name__ == "__main__":
    name_server = NameServer(NAME_SERVER['IP'], NAME_SERVER['PORT'])
    name_server.start()
