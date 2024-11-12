import socket
import json
from constants import OPERATIONS, SERVER_CONFIG, ENCODING, BUFFER_SIZE, REQUEST_KEYS, MESSAGE_DELIMITER

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

        response = self.receive_message()

        return response

    def receive_message(self):

        """Lê a mensagem do servidor, assim como o servidor lê a requisição"""

        length_buffer = b''
        
        while not length_buffer.endswith(MESSAGE_DELIMITER):
            part = self.sock.recv(1)
            if not part:
                break

            length_buffer += part

        message_length = length_buffer.decode(ENCODING).strip()
        if not message_length:
            return None 
        
        message_length = int(message_length)
        buffer = b''

        while len(buffer) < message_length:
            part = self.sock.recv(BUFFER_SIZE)
            if not part:
                break

            buffer += part

        return buffer.decode(ENCODING)

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

    def check_primes(self, numbers):
        return self.send_operation(OPERATIONS['CHECK_PRIMES'], *numbers)
    
    def check_primes_parallel(self, list_numbers, n_process):
        return self.send_operation(OPERATIONS['CHECK_PRIMES_PARALLEL'], list_numbers, n_process)
    
    def close(self):
        self.sock.close()