import socket
import json
import time
import multiprocessing
import threading
import os
import signal
import ssl

from multiprocessing import Pool

from config.config_server import OPERATIONS, SERVER_CONFIG, REQUEST_KEYS, THREAD_PROCESS, ERROR_MESSAGE, DIV_ZERO_ERROR, INVALID_OPERATION, ERROR_NUMBER_PROCESS, LOG_SERVER_START, LOG_CONNECTION_ESTABLISHED, LOG_CONNECTION_CLOSED, LOG_CLIENT_ERROR, LOG_SERVER_CLOSED

from config.config_certs import PATH_SERVER_CERTS, PATH_SERVER_KEY
from utils.message_handler import MessageHandler
from utils.prime_check import PrimeChecker
from cache.cache_manager import CacheManager
from cache.disk_cache_manager import DiskCacheManager
from cache.decorators import cached
from log.logger import Logger

class Server:
    
    def __init__(self, ip=SERVER_CONFIG['IP'], port=SERVER_CONFIG['PORT'], log_file="server_log.txt"):

        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Configuração do SSL
        self.context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        self.context.load_cert_chain(certfile=PATH_SERVER_CERTS, keyfile=PATH_SERVER_KEY)
        
        self.running = True

        self.logger = Logger(log_file)
        
        # Operações disponíveis
        self.operations = {
            OPERATIONS['SUM']: self.sum,
            OPERATIONS['SUB']: self.sub,
            OPERATIONS['MUL']: self.mul,
            OPERATIONS['DIV']: self.div,
            OPERATIONS['WAIT']: self.wait_n_seconds,
            OPERATIONS['CHECK_PRIMES']: self.check_primes,
            OPERATIONS['CHECK_PRIMES_PARALLEL']: self.check_primes_parallel,
            OPERATIONS['VALIDA_CPF']: self.valida_CPF
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
                    
                    # Encapsula o socket com SSL
                    secure_connection = self.context.wrap_socket(connection, server_side=True)
                    
                    print(LOG_CONNECTION_ESTABLISHED.format(address=self.address))
                    worker = threading.Thread(target=self.handle_client, args=(secure_connection,))
                    worker.start()

                except socket.timeout:
                    continue  
        finally:
            self.sock.close() 
            
    def handle_sigint(self, signum, frame):
        
        """Manipula o sinal SIGINT (Ctrl + C) para encerrar o servidor."""
        
        print(LOG_SERVER_CLOSED)
        self.running = False

    def handle_client(self, connection):
        
        try:
            while True:
                start_time = time.perf_counter()
                buffer = MessageHandler.receive_message(connection)

                if buffer is None: 
                    break
                
                response = self.process_request(buffer)
                
                if not MessageHandler.send_message(connection, response):
                    break

                end_time = time.perf_counter()
                response_time = end_time - start_time

                self.logger.log(self.address[0], self.get_operation_name(buffer), response_time)

        except Exception as e:
            print(LOG_CLIENT_ERROR.format(address=self.address, error=e))
        finally:
            connection.close()
            print(LOG_CONNECTION_CLOSED.format(address=self.address))

    def get_operation_name(self, data):
        try:
            request = json.loads(data)
            operation = request.get(REQUEST_KEYS['OPERATION'])
            return operation
        except:
            return "UNKNOWN"

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

    @cached(cache_manager=CacheManager())
    def mul(self, values):                                             
        return values[0] * values[1]

    def div(self, values):
        return values[0] / values[1]
    
    def wait_n_seconds(self, values):
        time.sleep(values[0])
        return values[0]

    def check_primes(self, list_numbers):
        
        """Verifica primalidade de números sem o uso de paralelismo"""

        prime_checker = PrimeChecker()

        return [prime_checker.is_prime(n) for n in list_numbers]
    
    def check_primes_parallel(self, values):
        
        """Verifica primalidade de números em paralelo, dividindo entre múltiplos processos."""

        prime_checker = PrimeChecker(self.cache_manager)
        
        list_numbers, n_process = values 

        if n_process > os.cpu_count():
            raise ValueError()

        pool = Pool(processes=n_process)
        resp = pool.map(prime_checker.is_prime, list_numbers)
        pool.close()
        pool.join()

        return resp
    
    def valida_CPF(self, cpf):

        cpf = cpf[0]

        numbers = '0123456789'

        cpf = ''.join([x for x in cpf if x in numbers])
    
        # Verifica se o CPF tem 11 dígitos
        if len(cpf) != 11:
            return False
        
        # Verifica se todos os dígitos são iguais (caso contrário, o CPF é inválido)
        if cpf == cpf[0] * 11:
            return False
        
        # Calcula o primeiro dígito verificador
        soma = 0
        for i in range(9):
            soma += int(cpf[i]) * (10 - i)

        resto = soma % 11

        digito1 = 0 if resto < 2 else 11 - resto
        
        # Calcula o segundo dígito verificador
        soma = 0
        for i in range(10):
            soma += int(cpf[i]) * (11 - i)

        resto = soma % 11
        digito2 = 0 if resto < 2 else 11 - resto
        
        # Verifica se os dígitos calculados são iguais aos dígitos informados
        if int(cpf[9]) == digito1 and int(cpf[10]) == digito2:
            return True
        
        return False