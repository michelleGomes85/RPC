import math

class PrimeChecker:
    
    def __init__(self, cache_manager):
        
        """
        Inicializa o verificador de números primos com um gerenciador de cache.

        :param cache_manager: Instância do DiskCacheManager.
        """
        
        self.cache_manager = cache_manager

    def is_prime(self, n):
        
        if n <= 1:
            return False
        elif n == 2:
            return True
        elif n % 2 == 0:
            return False
        
        """
        Verifica se um número é primo, usando o cache para acelerar o processo.

        :param n: Número a ser verificado.
        :return: True se for primo, False caso contrário.
        """
        
        # Verifica no cache
        cached_result = self.cache_manager.get(n)
        if cached_result is not None:
            return bool(cached_result)

        # Calcula a primalidade
        result = all(n % i != 0 for i in range(3, int(math.sqrt(n)) + 1, 2))

        # Armazena no cache
        self.cache_manager.insert(n, int(result))
        
        return result
