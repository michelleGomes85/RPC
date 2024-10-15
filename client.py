import socket
import json

class Client():
    
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
        self.sock.send(json.dumps(request).encode('utf-8'))
        
        # Recebe o resultado do servidor
        response = self.sock.recv(1024).decode('utf-8')
        
        return response  # Retorna a resposta diretamente como string
    
    def sum(self, value1, value2):
        """Solicita uma soma ao servidor"""
        return self.send_operation('sum', value1, value2)
    
    def sumList(self, values):
        return self.send_operation('sum', *values)

    def sub(self, value1, value2):
        """Solicita uma subtração ao servidor"""
        return self.send_operation('sub', value1, value2)

    def mul(self, value1, value2):
        """Solicita uma multiplicação ao servidor"""
        return self.send_operation('mul', value1, value2)

    def div(self, value1, value2):
        """Solicita uma divisão ao servidor"""
        return self.send_operation('div', value1, value2)

    def close(self):
        """Fecha a conexão com o servidor"""
        self.sock.close()
