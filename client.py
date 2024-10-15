import socket
import json

class Client:
    
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    def connect(self):
        self.sock.connect((self.ip, self.port))
        
    def send_operation(self, operation, *args):
        """Envia uma operação e seus argumentos ao servidor via JSON"""
        # Cria um dicionário com a operação e os valores
        request = {
            "operation": operation,
            "values": args
        }
        
        # Serializa o dicionário para JSON e envia
        message = json.dumps(request).encode('utf-8')
        message_length = len(message)
        
        # Envia o comprimento da mensagem e a mensagem em si
        self.sock.sendall(f'{message_length}\n'.encode('utf-8'))
        self.sock.sendall(message)
        
        # Recebe o resultado do servidor
        response = self.sock.recv(1024).decode('utf-8')
        return response
    
    def sum(self, value1, value2):
        return self.send_operation('sum', value1, value2)
    
    def sumList(self, values):
        return self.send_operation('sum', *values)

    def sub(self, value1, value2):
        return self.send_operation('sub', value1, value2)

    def mul(self, value1, value2):
        return self.send_operation('mul', value1, value2)

    def div(self, value1, value2):
        return self.send_operation('div', value1, value2)

    def close(self):
        self.sock.close()
