import math

class PrimeChecker:
    
    def __init__(self, cache_manager):
        
        """
        Inicializa o verificador de números primos com um gerenciador de cache.

        :param cache_manager: Instância do DiskCacheManager.
        """
        
        self.cache_manager = cache_manager

    def is_prime(self, n):
        
        """
        Verifica se um número é primo, usando o cache para acelerar o processo.

        :param n: Número a ser verificado.
        :return: True se for primo, False caso contrário.
        """
        
        # Verifica no cache
        cached_result = self.cache_manager.get(n)
        if cached_result is not None:
            return cached_result

        # Calcula a primalidade
        if n <= 1:
            result = False
        elif n == 2:
            result = True
        elif n % 2 == 0:
            result = False
        else:
            result = all(n % i != 0 for i in range(3, int(math.sqrt(n)) + 1, 2))

        # Armazena no cache
        self.cache_manager.insert(n, result)
        
        return result
