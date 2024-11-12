import socket
import json
import time
import multiprocessing
import math
import threading
import os

from constants import OPERATIONS, ERROR_MESSAGE, DIV_ZERO_ERROR, SERVER_CONFIG, ENCODING, BUFFER_SIZE, REQUEST_KEYS, INVALID_OPERATION, MESSAGE_DELIMITER, THREAD_PROCESS, ERROR_NUMBER_PROCESS
from multiprocessing import Pool

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
            OPERATIONS['DIV']: self.div,
            OPERATIONS['WAIT']: self.wait_n_seconds,
            OPERATIONS['CHECK_PRIMES']: self.check_primes,
            OPERATIONS['CHECK_PRIMES_PARALLEL']: self.check_primes_parallel 
        }

    def start(self):
        
        self.sock.bind((self.ip, self.port))
        self.sock.listen(1)
        print(f"Servidor escutando em {self.ip}:{self.port}")
        
        while True:
            connection, address = self.sock.accept()
            print(f"Conexão estabelecida com {address}")
            
            worker = threading.Thread if THREAD_PROCESS else multiprocessing.Process
            client_handler = worker(target=self.handle_client, args=(connection,))
            client_handler.start()  

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

                # Processa a mensagem recebida
                response = self.process_request(buffer.decode(ENCODING))

                # Envia o comprimento da resposta seguido pela resposta em si
                response_message = response.encode(ENCODING)
                response_length = len(response_message)

                # Envia o comprimento da resposta e a mensagem
                connection.sendall(f'{response_length}\n'.encode(ENCODING))
                connection.sendall(response_message)

        finally:
            connection.close()


    def process_request(self, data):

        try:
            request = json.loads(data)
            operation = request.get(REQUEST_KEYS['OPERATION'])
            values = request.get(REQUEST_KEYS['VALUES'])

            if operation not in self.operations:
                return INVALID_OPERATION

            result = self.operations[operation](values)

            return str(result)
        
        except ZeroDivisionError:
            return DIV_ZERO_ERROR
        
        except ValueError:
            return ERROR_NUMBER_PROCESS
        
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
    
    def wait_n_seconds(self, values):
        time.sleep(values[0])
        return values[0]
    
    def is_prime(self, n):

        if n <= 1:
            return False
        
        if n == 2: 
            return True
        
        if n % 2 == 0: 
            return False
        
        for i in range(3, int(math.sqrt(n)) + 1, 2):
            if n % i == 0:

                return False
            
        return True

    def check_primes(self, list_numbers):

        """Verifica primalidade de números sem o uso de paralelismo"""

        return [self.is_prime(n) for n in list_numbers]
    
    def check_primes_parallel(self, values):
        
        """Verifica primalidade de números em paralelo, dividindo entre múltiplos processos."""
        
        list_numbers, n_process = values 

        if n_process > os.cpu_count():
            raise ValueError()

        pool = Pool(processes=n_process)
        resp = pool.map(self.is_prime, list_numbers)
        pool.close()
        pool.join()

        return resp