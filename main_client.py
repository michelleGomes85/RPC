import time
import matplotlib.pyplot as plt
from client import Client

def test_performance():
    
    client = Client()  
    client.connect()
    
    # Lista de tamanhos para teste
    sizes = [1_000, 10_000, 50_000, 100_000, 500_000, 1_000_000]
    
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

if __name__ == "__main__":
    results = test_performance()
    plot_results(results)
