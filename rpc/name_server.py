import socket
import json
import signal
from threading import Thread

from config.config_server_name import SERVER_MAP, NAME_SERVER, LOG_SERVER_NAME_CLOSED, LOG_SERVER_NAME_START, KEY_OPERATION, ERROR_KEY_OPERATION_MISSING, LOG_REQUEST_RECEIVED, ERROR_UNKNOWN_OPERATION, ERROR, LOG_OPERATION_NOT_FOUND, ERROR_FORMAT_WRONG, ERROR_INTERNAL
from config.constants import ENCODING, BUFFER_SIZE

class NameServer:
    
    def __init__(self, ip = NAME_SERVER['IP'], port = NAME_SERVER['PORT']):
        
        """Inicializa o servidor de nomes."""
        
        self.ip = ip
        self.port = port
        self.buffer_size = BUFFER_SIZE
        self.encoding = ENCODING
        self.server_map = SERVER_MAP
        
        self.udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        self.running = True

    def start(self):
        
        """Inicia o servidor de nomes para gerenciar endereços dos servidores de operação."""

        signal.signal(signal.SIGINT, self.handle_sigint)
        
        self.udp_sock.bind((self.ip, self.port))
        
        print(LOG_SERVER_NAME_START.format(ip=self.ip, port=self.port))

        try:
            while self.running:
                self.udp_sock.settimeout(1)
                try:
                    data, addr = self.udp_sock.recvfrom(self.buffer_size)

                    # Cria uma nova thread para processar a requisição
                    client_thread = Thread(target=self.handle_request, args=(data, addr))
                    client_thread.start()
                except socket.timeout:
                    continue
        finally:
            self.udp_sock.close()
        
    def handle_sigint(self, signum, frame):
        
        """Manipula o sinal SIGINT (Ctrl + C) para encerrar o servidor."""
        
        print(LOG_SERVER_NAME_CLOSED)
        self.running = False

    def handle_request(self, data, addr):
        
        """Trata uma solicitação recebida de um cliente."""
        
        try:
            request = json.loads(data.decode(self.encoding))

            if KEY_OPERATION not in request:
                self.send_error(addr, ERROR_KEY_OPERATION_MISSING)
                return

            operation = request[KEY_OPERATION]
            print(LOG_REQUEST_RECEIVED.format(addr=addr, operation=operation))

            response = self.server_map.get(operation, {})

            if not response:
                response = {ERROR: LOG_OPERATION_NOT_FOUND}

                raise Exception(ERROR_UNKNOWN_OPERATION)

            self.send_response(addr, response)

        except json.JSONDecodeError:
            self.send_error(addr, ERROR_FORMAT_WRONG)
        except Exception as e:
            self.send_error(addr, ERROR_INTERNAL)

    def send_response(self, addr, response):
        
        """Envia uma resposta para o cliente."""
        
        self.udp_sock.sendto(json.dumps(response).encode(self.encoding), addr)

    def send_error(self, addr, message):
        
        """Envia uma mensagem de erro para o cliente."""
        
        error_message = {ERROR: message}
        self.udp_sock.sendto(json.dumps(error_message).encode(self.encoding), addr)
