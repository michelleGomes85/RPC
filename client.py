import socket
import json

from config import OPERATIONS, SERVER_CONFIG, ENCODING, BUFFER_SIZE, REQUEST_KEYS, MESSAGE_DELIMITER, N_CACHE_MEMORY
from utils import MessageHandler
from cache_manager import CacheManager

class Client:
    
    def __init__(self):

        self.ip = SERVER_CONFIG['IP']
        self.port = SERVER_CONFIG['PORT']
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        
        self.cache_sum = CacheManager() # Sem limite
        self.cache_div = CacheManager(max_size=N_CACHE_MEMORY)  # Com limite
        
    def connect(self):
        self.sock.connect((self.ip, self.port))
        
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

    def sum(self, value1, value2):                                             
        
        key = f"{min(value1, value2)}+{max(value1, value2)}"
        cached_result = self.cache_sum.get(key)
        
        if cached_result is not None:
            return cached_result
       
        result = self.send_operation(OPERATIONS['SUM'], value1, value2)
        self.cache_sum.set(key, result)
        
        return result
    
    def sumList(self, values):
        return self.send_operation(OPERATIONS['SUM'], *values)

    def sub(self, value1, value2):
        return self.send_operation(OPERATIONS['SUB'], value1, value2)

    def mul(self, value1, value2):
        return self.send_operation(OPERATIONS['MUL'], value1, value2)
    
    def div(self, value1, value2):
        
        key = f"{value1}/{value2}"
        cached_result = self.cache_div.get(key)
        
        if cached_result is not None:
            return cached_result
        
        result = self.send_operation(OPERATIONS['DIV'], value1, value2)
        
        self.cache_div.set(key, result)
        
        return result

    def wait_n_seconds(self, n):
        return self.send_operation(OPERATIONS['WAIT'], n)

    def check_primes(self, numbers):
        return self.send_operation(OPERATIONS['CHECK_PRIMES'], *numbers)
    
    def check_primes_parallel(self, list_numbers, n_process):
        return self.send_operation(OPERATIONS['CHECK_PRIMES_PARALLEL'], list_numbers, n_process)
    
    def close(self):
        self.sock.close()