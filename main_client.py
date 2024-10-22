from client import Client
from constants import SERVER_CONFIG

def test_operations():
    
    while True:
        client = Client()
        client.connect()

        # # Teste de operações
        # print("Soma (10 + 20):", client.sum(10, 20)) 
        # print("Subtração (15 - 10):", client.sub(15, 10))
        # print("Subtração (15 - 'b'):", client.sub(15, 'b')) 
        # print("Multiplicação (5 * 5):", client.mul(5, 5))
        # print("Divisão (10 / 2):", client.div(10, 2))
        # print("Divisão (10 / 0):", client.div(10, 0))  # Testando divisão por zero
        # print("Multiplicação (10 * 'a'):", client.mul(10, 'a'))  # Testando mandar string
        
        # # Testando somar uma lista de números
        # print("Somando Lista: ", client.sumList(list(range(10000))))

        print("Wait: ", client.wait_n_seconds(2))

        client.close()

if __name__ == "__main__":
    test_operations()