import math
from cache.disk_cache_manager import DiskCacheManager
from cache.decorators import cached


class PrimeChecker:
    
    def __init__(self):
        pass

    @cached(cache_manager=DiskCacheManager(cache_file="cache/files/prime_cache.json"))
    def is_prime(self, n):

        """
        Verifica se um número é primo.

        :param n: Número a ser verificado.
        :return: True se for primo, False caso contrário.
        """
        
        if n <= 1:
            return False
        elif n == 2:
            return True
        elif n % 2 == 0:
            return False

        # Calcula a primalidade
        return all(n % i != 0 for i in range(3, int(math.sqrt(n)) + 1, 2))
