import socket
import json
from config.config import NAME_SERVER, BUFFER_SIZE, ENCODING, SERVER_MAP

class NameServer:
    
    def __init__(self, ip = NAME_SERVER['IP'], port = NAME_SERVER['PORT']):
        
        """Inicializa o servidor de nomes."""
        
        self.ip = ip
        self.port = port
        self.buffer_size = BUFFER_SIZE
        self.encoding = ENCODING
        self.server_map = SERVER_MAP
        
        self.udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def start(self):
        
        """Inicia o servidor de nomes para gerenciar endereços dos servidores de operação."""
        
        self.udp_sock.bind((self.ip, self.port))
        
        print(f"Servidor de nomes rodando em {self.ip}:{self.port}")

        try:
            while True:
                self.handle_request()
        except KeyboardInterrupt:
            print("\nEncerrando o servidor de nomes...")
        finally:
            self.udp_sock.close()

    def handle_request(self):
        
        """Trata uma solicitação recebida de um cliente."""
        
        try:
            data, addr = self.udp_sock.recvfrom(self.buffer_size)
            request = json.loads(data.decode(self.encoding))

            if 'operation' not in request:
                self.send_error(addr, 'Chave "operation" ausente na solicitação.')
                return

            operation = request['operation']
            print(f"Solicitação recebida de {addr}: operação = {operation}")

            response = self.server_map.get(operation, {})

            if not response:
                response = {'error': f"Operação '{operation}' não encontrada."}
                print(f"Operação desconhecida solicitada: {operation}")

            self.send_response(addr, response)

        except json.JSONDecodeError:
            self.send_error(addr, 'Solicitação inválida. Esperado formato JSON.')
        except Exception as e:
            print(f"Erro inesperado: {e}")
            self.send_error(addr, 'Erro interno no servidor de nomes.')

    def send_response(self, addr, response):
        
        """Envia uma resposta para o cliente."""
        
        self.udp_sock.sendto(json.dumps(response).encode(self.encoding), addr)

    def send_error(self, addr, message):
        
        """Envia uma mensagem de erro para o cliente."""
        
        error_message = {'error': message}
        self.udp_sock.sendto(json.dumps(error_message).encode(self.encoding), addr)
