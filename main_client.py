import time
import matplotlib.pyplot as plt
from rpc.client import Client

def test_performance():
    
    client = Client()  
    client.connect()
    
    # Lista de tamanhos para teste
    sizes = [1_000, 10_000, 50_000, 100_000, 1_000_000]
    
    results = {"size": [], "sequential": [], "parallel": []}
    
    for size in sizes:
        
        numbers = list(range(size))
        
        start_time = time.time()
        client.check_primes(numbers)
        end_time = time.time()
        sequential_time = end_time - start_time
        
        start_time = time.time()
        client.check_primes_parallel(numbers, 4)
        end_time = time.time()
        parallel_time = end_time - start_time
        
        results["size"].append(size)
        results["sequential"].append(sequential_time)
        results["parallel"].append(parallel_time)
    
    client.close()
    
    return results

def plot_results(results):

    sizes = results["size"]
    sequential_times = results["sequential"]
    parallel_times = results["parallel"]
    
    bar_width = 0.35
    index = range(len(sizes))
    
    plt.figure(figsize=(10, 6))
    
    plt.bar(index, sequential_times, bar_width, label='Sequencial', color='b')
    plt.bar([i + bar_width for i in index], parallel_times, bar_width, label='Paralelo', color='g')
    
    plt.xlabel('Tamanho da Lista')
    plt.ylabel('Tempo de Execução (segundos)')
    plt.title('Comparação de Tempos de Execução entre Métodos Sequenciais e Paralelos')
    plt.xticks([i + bar_width / 2 for i in index], sizes)
    plt.legend()
    
    plt.tight_layout()
    plt.show()

# Função para testar outras operações (sem gerar gráfico)
def test_operations():
    
    try:
        client = Client()  
    
    # print("Soma (11 + 20):", client.sum(11, 20)) 
    # print("Soma (5 + 20):", client.sum(5, 20)) 
    # print("Soma (11 + 20):", client.sum(20, 11)) 
    # print("Soma (5 + 20):", client.sum(5, 20)) 
    # print("Soma (5 + 20):", client.sum(5, 20)) 

    # print("Multiplicação (11 * 20):", client.mul(11, 20)) 
    # print("Multiplicação (20 * 11):", client.mul(20, 11)) 
    # print("Multiplicação (10 * 100):", client.mul(10, 100)) 
    # print("Multiplicação (5 * 4):", client.mul(5, 4)) 

    # print("\n-- Divisão (20 / 10):", client.div(20, 10)) # cache
    # print("\n-- Divisão (20 / 5):", client.div(20, 5)) #cache
    # print("Divisão (20 / 10):", client.div(20, 10)) #não chama
    # print("\n-- Divisão (30 / 10):", client.div(30, 10)) #cache
    # print("Divisão (20 / 10):", client.div(20, 10)) #não chama
    # print("\n-- Divisão (80 / 20):", client.div(80, 20)) #cache tira 20/10
    # print("Divisão (20 / 10):", client.div(20, 10)) #chama tira 20,5
    # print("\n-- Divisão (100 / 20):", client.div(20, 5)) #chama 

    # print("Subtração (15 - 10):", client.sub(15, 10))
    # print("Subtração (15 - 'b'):", client.sub(15, 'b')) 
    # print("Multiplicação (5 * 5):", client.mul(5, 5))
    # print("Divisão (10 / 2):", client.div(10, 2))
    # print("Divisão (10 / 0):", client.div(10, 0))  
    # print("Multiplicação (10 * 'a'):", client.mul(10, 'a')) 
    
    # # Testando somar uma lista de números
    # print("Somando Lista de 10.000 números:", client.sumList(list(range(10_000))))

    # print("Aguardar 1 segundos:", client.wait_n_seconds(1))
    
        # numbers = list(range(1, 10))
        # print(client.check_primes(numbers))

        print(client.valida_CPF("371.587.380-94"))

        client.close()
    except Exception as e:
        print(f"\nErro de conexão: {e}")


if __name__ == "__main__":
    #results = test_performance()
    #plot_results(results)

    # Testando as operações matemáticas
    test_operations()