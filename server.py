import socket
import json
import time
import multiprocessing
import math
import threading
import os

from config import OPERATIONS, ERROR_MESSAGE, DIV_ZERO_ERROR, SERVER_CONFIG, ENCODING, BUFFER_SIZE, REQUEST_KEYS, INVALID_OPERATION, THREAD_PROCESS, ERROR_NUMBER_PROCESS, LOG_CLIENT_ERROR, LOG_CONNECTION_CLOSED, LOG_CONNECTION_ESTABLISHED, LOG_SERVER_START
from multiprocessing import Pool
from utils import MessageHandler

class Server:
    
    def __init__(self):

        self.ip = SERVER_CONFIG['IP']
        self.port = SERVER_CONFIG['PORT']
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.cacheMul = {}
        
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
        
        print(LOG_SERVER_START.format(ip=self.ip, port=self.port))
        
        while True:
            connection, self.address = self.sock.accept()
            
            print(LOG_CONNECTION_ESTABLISHED.format(address=self.address))
            
            worker = threading.Thread if THREAD_PROCESS else multiprocessing.Process
            client_handler = worker(target=self.handle_client, args=(connection,))
            client_handler.start()  

    def handle_client(self, connection):
        
        try:
            while True:
                buffer = MessageHandler.receive_message(connection)

                if buffer is None: 
                    break
                
                response = self.process_request(buffer)
                
                if not MessageHandler.send_message(connection, response):
                    break

        except Exception as e:
            print(LOG_CLIENT_ERROR.format(address=self.address, error=e))
        finally:
            connection.close()
            print(LOG_CONNECTION_CLOSED.format(address=self.address))

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

        key = str(values[0]) + '*' + str(values[1])
       
        if key in self.cacheMul:
            return self.cacheMul[key]
        else:
            self.cacheMul[key] = values[0] * values[1]

        return self.cacheMul[key]

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