# test_client.py
from client import Client

def test_operations():
    
    client = Client('127.0.0.1', 5000)
    client.connect()

    # Teste de operações
    print("Soma (10 + 20):", client.sum(10, 20)) 
    print("Subtração (15 - 10):", client.sub(15, 10))
    print("Subtração (15 - 'b'):", client.sub(15, 'b')) 
    print("Multiplicação (5 * 5):", client.mul(5, 5))
    print("Divisão (10 / 2):", client.div(10, 2))
    print("Divisão (10 / 0):", client.div(10, 0))  # Testando divisão por zero
    print("Multiplicação (10 * 'a'):", client.mul(10, 'a'))  # Testando mandar string
    
    # Testando somar uma lista de números
    print("Somando Lista: ", client.sumList([1,2,3]))

    client.close()

if __name__ == "__main__":
    test_operations()
