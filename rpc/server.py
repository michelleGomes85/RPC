import socket
import json
import time
import multiprocessing
import threading
import os
import signal

from multiprocessing import Pool

from config.config import OPERATIONS, ERROR_MESSAGE, DIV_ZERO_ERROR, SERVER_CONFIG, REQUEST_KEYS, INVALID_OPERATION, THREAD_PROCESS, ERROR_NUMBER_PROCESS, LOG_CLIENT_ERROR, LOG_CONNECTION_CLOSED, LOG_CONNECTION_ESTABLISHED, LOG_SERVER_START

from utils.message_handler import MessageHandler
from utils.prime_check import PrimeChecker
from cache.cache_manager import CacheManager
from cache.disk_cache_manager import DiskCacheManager

class Server:
    
    def __init__(self):

        self.ip = SERVER_CONFIG['IP']
        self.port = SERVER_CONFIG['PORT']
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        self.cache_mul = CacheManager() 
        self.cache_manager = DiskCacheManager()
        
        self.running = True
        
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
        
        signal.signal(signal.SIGINT, self.handle_sigint)
        
        self.sock.bind((self.ip, self.port))
        self.sock.listen(1)
        
        print(LOG_SERVER_START.format(ip=self.ip, port=self.port))
        
        try:
            while self.running:
                self.sock.settimeout(1)
                try:
                    connection, self.address = self.sock.accept()
                except socket.timeout:
                    continue  
                
                print(LOG_CONNECTION_ESTABLISHED.format(address=self.address))
                worker = threading.Thread if THREAD_PROCESS else multiprocessing.Process
                client_handler = worker(target=self.handle_client, args=(connection,))
                client_handler.start()
        finally:
            self.sock.close() 
            
    def handle_sigint(self, signum, frame):
        
        """Manipula o sinal SIGINT (Ctrl + C) para encerrar o servidor."""
        
        print("\nServidor encerrado.")
        self.running = False

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
        
        key = f"{min(values[0], values[1])}*{max(values[0], values[1])}"
        cached_result = self.cache_mul.get(key)
        
        if cached_result is not None:
            return cached_result
       
        result = values[0] * values[1]
        self.cache_mul.set(key, result)
        
        return result

    def div(self, values):
        return values[0] / values[1]
    
    def wait_n_seconds(self, values):
        time.sleep(values[0])
        return values[0]

    def check_primes(self, list_numbers):
        
        prime_checker = PrimeChecker(self.cache_manager)

        """Verifica primalidade de números sem o uso de paralelismo"""

        return [prime_checker.is_prime(n) for n in list_numbers]
    
    def check_primes_parallel(self, values):
        
        prime_checker = PrimeChecker(self.cache_manager)
        
        """Verifica primalidade de números em paralelo, dividindo entre múltiplos processos."""
        
        list_numbers, n_process = values 

        if n_process > os.cpu_count():
            raise ValueError()

        pool = Pool(processes=n_process)
        resp = pool.map(self.is_prime, list_numbers)
        pool.close()
        pool.join()

        return resp