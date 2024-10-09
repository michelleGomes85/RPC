
from server import Server

if __name__ == "__main__":
    
    ip = "127.0.0.1"
    port = 5000 

    server = Server(ip, port)
    
    server.start()
