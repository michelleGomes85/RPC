from collections import deque

class CacheManager:
    
    def __init__(self, max_size=None):
        
        """
        Inicializa o gerenciador de cache.
        :param max_size: Tamanho máximo do cache (None para ilimitado).
        """
        
        self.cache = {}
        self.queue = deque()
        self.max_size = max_size

    def get(self, key):
        
        """Recupera um valor do cache, se existir."""
        
        return self.cache.get(key)

    def set(self, key, value):
        
        """Adiciona um novo valor ao cache, respeitando o limite de tamanho."""
        
        if key in self.cache:
            return  # Já está no cache, não é necessário adicionar novamente.

        if self.max_size is not None and len(self.cache) >= self.max_size:
            
            # Remove o item mais antigo, se o limite for alcançado
            
            oldest_key = self.queue.popleft()
            del self.cache[oldest_key]

        self.queue.append(key)
        self.cache[key] = value

    def __len__(self):
        
        """Retorna o número de itens no cache."""
        
        return len(self.cache)
