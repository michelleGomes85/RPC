import socket
import json
import random

from config.config import OPERATIONS, SERVER_CONFIG, ENCODING, BUFFER_SIZE, REQUEST_KEYS, MESSAGE_DELIMITER, N_CACHE_MEMORY, NAME_SERVER
from utils.message_handler import MessageHandler
from cache.cache_manager import CacheManager


class Client:
    
    def __init__(self, ip = NAME_SERVER['IP'], port = NAME_SERVER['PORT']):

        self.name_server_ip = ip
        self.name_server_port = port
        self.sock = None
        
        self.cache_sum = CacheManager() # Sem limite
        self.cache_div = CacheManager(max_size=N_CACHE_MEMORY)  # Com limite
        
    def get_server_list(self, operation):
        
        """Obtém a lista de servidores do servidor de nomes."""
        
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_sock:
            
            request = {"operation": operation}
            udp_sock.sendto(json.dumps(request).encode(ENCODING), (self.name_server_ip, self.name_server_port))
            response, _ = udp_sock.recvfrom(BUFFER_SIZE)
            server_list = json.loads(response.decode(ENCODING))
            
            return server_list
    
    def connect_to_server(self, ip, port):
        
        """Conecta ao servidor de operação via TCP."""
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        self.sock.connect((ip, port))
        
    def send_operation(self, operation, *args):
        
        """Envia uma operação e seus argumentos ao servidor via JSON"""
        
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
            return None
    
    def execute_operation(self, operation, *args):
        
        """Obtém o servidor da operação e executa."""
        
        # Passo 1: Obter a lista de servidores do servidor de nomes
        server_list = self.get_server_list(operation)
        if not server_list:
            raise Exception(f"Nenhum servidor disponível para a operação '{operation}'.")

        # Passo 2: Escolher um servidor aleatoriamente
        selected_server = random.choice(server_list)
        print(selected_server)
        ip, port = selected_server["IP"], selected_server["PORT"]

        # Passo 3: Conectar ao servidor escolhido
        self.connect_to_server(ip, port)

        # Passo 4: Enviar operação e retornar resposta
        result = self.send_operation(operation, *args)
        self.close()  
        
        return result

    def sum(self, value1, value2):                                             
        
        """Operação de soma com cache sem limite"""
        
        key = f"{min(value1, value2)}+{max(value1, value2)}"
        cached_result = self.cache_sum.get(key)
        
        if cached_result is not None:
            return cached_result
       
        result = self.execute_operation(OPERATIONS["SUM"], value1, value2)

        self.cache_sum.set(key, result)
        
        return result
    
    def sumList(self, values):
        return self.execute_operation(OPERATIONS['SUM'], *values)

    def sub(self, value1, value2):
        return self.execute_operation(OPERATIONS['SUB'], value1, value2)

    def mul(self, value1, value2):
        return self.execute_operation(OPERATIONS['MUL'], value1, value2)
    
    def div(self, value1, value2):
        
        """Operação de divisão com cache com limite"""
        
        key = f"{value1}/{value2}"
        cached_result = self.cache_div.get(key)
        
        if cached_result is not None:
            return cached_result
        
        result = self.execute_operation(OPERATIONS["DIV"], value1, value2)
        
        self.cache_div.set(key, result)
        
        return result

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