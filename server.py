import socket
import json

class Server:
    
    ERROR_MESSAGE = "ERROR"
    DIV_ZERO_ERROR = "Divisão por zero."
    
    def __init__(self, ip, port):
        
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Operações disponíveis
        self.operations = {
            'sum': self.sum,
            'sub': self.sub,
            'mul': self.mul,
            'div': self.div
        }

    def start(self):
        
        """Inicia o servidor e aguarda conexões"""
        
        self.sock.bind((self.ip, self.port))
        self.sock.listen(1)
        
        print(f"Servidor escutando em {self.ip}:{self.port}")
        
        while True:
            connection, address = self.sock.accept()
            print(f"Conexão estabelecida com {address}")
            self.handle_client(connection)

    def handle_client(self, connection):
        
        """Gerencia as requisições do cliente"""
        
        try:
            while True:
                data = connection.recv(1024).decode('utf-8')
                if not data:
                    break

                response = self.process_request(data)
                connection.send(response.encode('utf-8'))
        finally:
            connection.close()

    def process_request(self, data):
        
        """Processa a requisição e retorna o resultado"""
        
        try:
            
            # Decodifica o JSON recebido
            
            request = json.loads(data)
            operation = request.get('operation')
            values = request.get('values')

            # Verifica se a operação é valida
            if operation not in self.operations or len(values) < 2:
                return self.ERROR_MESSAGE

            a, b = values

            # Tenta realizar a operação
            result = self.operations[operation](a, b)
            
            return str(result)
        
        except ZeroDivisionError:
            return self.DIV_ZERO_ERROR
        except Exception:
            return self.ERROR_MESSAGE

    # Operações matemáticas
    def sum(self, a, b):
        return a + b

    def sub(self, a, b):
        return a - b

    def mul(self, a, b):
        return a * b

    def div(self, a, b):
        return a / b

