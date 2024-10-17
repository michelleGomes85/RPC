import socket
import json
from constants import OPERATIONS, ERROR_MESSAGE, DIV_ZERO_ERROR, SERVER_CONFIG, ENCODING, BUFFER_SIZE, REQUEST_KEYS, INVALID_OPERATION, MESSAGE_DELIMITER

class Server:
    
    def __init__(self):
        self.ip = SERVER_CONFIG['IP']
        self.port = SERVER_CONFIG['PORT']
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # Operações disponíveis
        self.operations = {
            OPERATIONS['SUM']: self.sum,
            OPERATIONS['SUB']: self.sub,
            OPERATIONS['MUL']: self.mul,
            OPERATIONS['DIV']: self.div
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
                length_buffer = b''
                while not length_buffer.endswith(MESSAGE_DELIMITER):
                    part = connection.recv(1)
                    if not part:
                        break
                    length_buffer += part

                message_length = length_buffer.decode(ENCODING).strip()
                if not message_length:
                    break
                
                message_length = int(message_length)
                buffer = b''
                while len(buffer) < message_length:
                    part = connection.recv(BUFFER_SIZE)
                    if not part:
                        break
                    buffer += part

                response = self.process_request(buffer.decode(ENCODING))
                connection.send(response.encode(ENCODING))

        finally:
            connection.close()

    def process_request(self, data):
        try:
            request = json.loads(data)
            operation = request.get(REQUEST_KEYS['OPERATION'])
            values = request.get(REQUEST_KEYS['VALUES'])

            if operation not in self.operations or len(values) < 2:
                return INVALID_OPERATION

            result = self.operations[operation](values)
            return str(result)
        
        except ZeroDivisionError:
            return DIV_ZERO_ERROR
        except Exception:
            return ERROR_MESSAGE

    def sum(self, values):
        return sum(values)

    def sub(self, values):
        return values[0] - values[1]

    def mul(self, values):
        return values[0] * values[1]

    def div(self, values):
        return values[0] / values[1]
