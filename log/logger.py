import os
import time
from datetime import datetime

class Logger:

    PATH_LOG_FILES = "log/files"

    def __init__(self, log_file):

        self.log_folder = Logger.PATH_LOG_FILES
        self.log_file = os.path.join(self.log_folder, log_file)
        
        os.makedirs(self.log_folder, exist_ok=True)

    def log(self, client_ip, operation, response_time):

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Converte o tempo de resposta para milissegundos
        response_time_ms = response_time * 1000
        log_entry = f"{timestamp}, {client_ip}, {operation}, {response_time_ms:.6f} ms\n"
        
        # Escreve no arquivo de log
        with open(self.log_file, "a") as file:
            file.write(log_entry)