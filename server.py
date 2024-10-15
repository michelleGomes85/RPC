import socket
import json

class Server:
    
    ERROR_MESSAGE = "ERROR"
    DIV_ZERO_ERROR = "Divisão por zero."
    
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # Operações disponíveis
        self.operations = {
            'sum': self.sum,
            'sub': self.sub,
            'mul': self.mul,
            'div': self.div
        }

    def start(self):
        self.sock.bind((self.ip, self.port))
        self.sock.listen(1)
        print(f"Servidor escutando em {self.ip}:{self.port}")
        
        while True:
            connection, address = self.sock.accept()
            print(f"Conexão estabelecida com {address}")
            self.handle_client(connection)

    def handle_client(self, connection):
        try:
            while True:
                # Primeiro, lê o comprimento da mensagem
                length_buffer = b''
                while not length_buffer.endswith(b'\n'):
                    part = connection.recv(1)
                    if not part:
                        break
                    
                    length_buffer += part

                message_length = length_buffer.decode('utf-8').strip()
                if not message_length:
                    break
                
                message_length = int(message_length)
                
                # Agora, lê a mensagem com o comprimento especificado
                buffer = b''
                while len(buffer) < message_length:
                    part = connection.recv(1024)
                    if not part:
                        break
                    buffer += part

                # Processa a requisição e envia a resposta
                response = self.process_request(buffer.decode('utf-8'))
                connection.send(response.encode('utf-8'))

        finally:
            connection.close()


    def process_request(self, data):
        try:
            request = json.loads(data)
            operation = request.get('operation')
            values = request.get('values')

            if operation not in self.operations or len(values) < 2:
                return self.ERROR_MESSAGE

            result = self.operations[operation](values)
            return str(result)
        
        except ZeroDivisionError:
            return self.DIV_ZERO_ERROR
        except Exception:
            return self.ERROR_MESSAGE

    def sum(self, values):
        return sum(values)

    def sub(self, values):
        return values[0] - values[1]

    def mul(self, values):
        return values[0] * values[1]

    def div(self, values):
        return values[0] / values[1]
