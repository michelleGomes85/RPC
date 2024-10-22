import socket
import json
from constants import OPERATIONS, SERVER_CONFIG, ENCODING, BUFFER_SIZE, REQUEST_KEYS

class Client:
    
    def __init__(self):
        
        self.ip = SERVER_CONFIG['IP']
        self.port = SERVER_CONFIG['PORT']
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    def connect(self):
        self.sock.connect((self.ip, self.port))
        
    def send_operation(self, operation, *args):
        
        """Envia uma operação e seus argumentos ao servidor via JSON"""
        request = {
            REQUEST_KEYS['OPERATION']: operation,
            REQUEST_KEYS['VALUES']: args
        }
        
        message = json.dumps(request).encode(ENCODING)
        message_length = len(message)
        
        self.sock.sendall(f'{message_length}\n'.encode(ENCODING))
        self.sock.sendall(message)
        
        response = self.sock.recv(BUFFER_SIZE).decode(ENCODING)
        return response
    
    def sum(self, value1, value2):
        return self.send_operation(OPERATIONS['SUM'], value1, value2)
    
    def sumList(self, values):
        return self.send_operation(OPERATIONS['SUM'], *values)

    def sub(self, value1, value2):
        return self.send_operation(OPERATIONS['SUB'], value1, value2)

    def mul(self, value1, value2):
        return self.send_operation(OPERATIONS['MUL'], value1, value2)

    def div(self, value1, value2):
        return self.send_operation(OPERATIONS['DIV'], value1, value2)
    
    def wait_n_seconds(self, n):
        return self.send_operation(OPERATIONS['WAIT'], n)

    def close(self):
        self.sock.close()
