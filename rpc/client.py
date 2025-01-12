import socket
import json
import random

from config.constants import ENCODING, BUFFER_SIZE, N_CACHE_MEMORY
from config.config_server import OPERATIONS, REQUEST_KEYS
from config.config_server_name import NAME_SERVER
from utils.message_handler import MessageHandler
from cache.cache_manager import CacheManager
from cache.decorators import cached

class Client:

    # Constantes para mensagens de erro
    LOG_ERROR_CONNECT_SERVER_NAME = "\nErro ao conectar ao servidor de nomes: {e}\n"
    LOG_ERROR_CONNECT_SERVER = "\nErro ao conectar ao servidor {ip}:{port}: {e}\n"
    LOG_ERROR_SEND_RECEIVE_MESSAGE = "\nErro ao enviar/receber mensagem: {e}\n"
    LOG_NO_SERVER_AVAILABLE = "\nNenhum servidor disponível para a operação '{operation}'.\n"
    LOG_CONNECT_SERVER_FAILED = "\nNão foi possível conectar ao servidor {ip}:{port}.\n"
    LOG_EXECUTE_OPERATION_FAILED = "\nErro ao executar a operação '{operation}': {e}\n"
    
    def __init__(self, ip=NAME_SERVER['IP'], port=NAME_SERVER['PORT']):
        self.name_server_ip = ip
        self.name_server_port = port
        self.sock = None
                
    def get_server_list(self, operation):

        """Obtém a lista de servidores do servidor de nomes."""
        
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_sock:
                request = {"operation": operation}
                udp_sock.sendto(json.dumps(request).encode(ENCODING), (self.name_server_ip, self.name_server_port))
                response, _ = udp_sock.recvfrom(BUFFER_SIZE)
                server_list = json.loads(response.decode(ENCODING))
                return server_list
        except (socket.error, json.JSONDecodeError) as e:
            raise Exception(self.LOG_ERROR_CONNECT_SERVER_NAME.format(e=e))
    
    def connect_to_server(self, ip, port):

        """Conecta ao servidor de operação via TCP."""

        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((ip, port))
            return True
        except socket.error as e:
            raise Exception(self.LOG_ERROR_CONNECT_SERVER.format(ip=ip, port=port, e=e))
        
    def send_operation(self, operation, *args):

        """Envia uma operação e seus argumentos ao servidor via JSON."""

        request = {
            REQUEST_KEYS['OPERATION']: operation,
            REQUEST_KEYS['VALUES']: args
        }
        
        try:
            if not MessageHandler.send_message(self.sock, json.dumps(request)):
                return None

            response = MessageHandler.receive_message(self.sock)
            if response is None:
                return None

            return response

        except (socket.error, json.JSONDecodeError) as e:
            raise Exception(self.LOG_ERROR_SEND_RECEIVE_MESSAGE.format(e=e))
    
    def execute_operation(self, operation, *args):

        """Obtém o servidor da operação e executa."""

        try:
            # Passo 1: Obter a lista de servidores do servidor de nomes
            server_list = self.get_server_list(operation)
            if not server_list:
                raise Exception(self.LOG_NO_SERVER_AVAILABLE.format(operation=operation))

            # Passo 2: Escolher um servidor aleatoriamente
            selected_server = random.choice(server_list)
            ip, port = selected_server["IP"], selected_server["PORT"]
            
            print(f"\nServidor escolhido para operação {ip}:{port}\n")
            
            # Passo 3: Conectar ao servidor escolhido
            if not self.connect_to_server(ip, port):
                raise Exception(self.LOG_CONNECT_SERVER_FAILED.format(ip=ip, port=port))

            # Passo 4: Enviar operação e retornar resposta
            result = self.send_operation(operation, *args)
            self.close()  
            
            return result

        except Exception as e:
            raise Exception(self.LOG_EXECUTE_OPERATION_FAILED.format(operation=operation, e=e))

    @cached(cache_manager=CacheManager())
    def sum(self, value1, value2):

        """Operação de soma com cache sem limite."""

        return self.execute_operation(OPERATIONS["SUM"], value1, value2)
    
    def sumList(self, values):
        return self.execute_operation(OPERATIONS['SUM'], *values)

    def sub(self, value1, value2):
        return self.execute_operation(OPERATIONS['SUB'], value1, value2)

    def mul(self, value1, value2):
        return self.execute_operation(OPERATIONS['MUL'], value1, value2)
    
    @cached(cache_manager=CacheManager(max_size=N_CACHE_MEMORY))
    def div(self, value1, value2):

        """Operação de divisão com cache com limite."""

        return self.execute_operation(OPERATIONS["DIV"], value1, value2)

    def wait_n_seconds(self, n):
        return self.execute_operation(OPERATIONS['WAIT'], n)

    def check_primes(self, numbers):
        return self.execute_operation(OPERATIONS['CHECK_PRIMES'], *numbers)
    
    def check_primes_parallel(self, list_numbers, n_process):
        return self.execute_operation(OPERATIONS['CHECK_PRIMES_PARALLEL'], list_numbers, n_process)
    
    def close(self):
        """Fecha o socket do cliente."""
        if self.sock:
            self.sock.close()
            self.sock = None