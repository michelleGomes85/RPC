import socket
from config.constants import ENCODING, BUFFER_SIZE, MESSAGE_DELIMITER

class MessageHandler:

    @staticmethod
    def receive_message(connection):
        
        """Lê uma mensagem em partes"""
        length_buffer = b''

        while not length_buffer.endswith(MESSAGE_DELIMITER):
            part = connection.recv(1)

            if not part:
                return None
            
            length_buffer += part

        message_length = length_buffer.decode(ENCODING).strip()

        if not message_length:
            return None

        try:
            message_length = int(message_length)
        except ValueError:
            return None

        buffer = b''
        while len(buffer) < message_length:
            part = connection.recv(BUFFER_SIZE)
            if not part: 
                return None
            buffer += part

        return buffer.decode(ENCODING)

    @staticmethod
    def send_message(connection, message):
        
        """Envia uma mensagem informando seu tamanho para leitura"""
        
        message = message.encode(ENCODING)
        message_length = len(message)

        try:
            connection.sendall(f'{message_length}\n'.encode(ENCODING))
            connection.sendall(message)
        except (socket.error, BrokenPipeError) as e:
            print(f"Erro ao enviar a mensagem: {e}")
            return False
        
        return True
