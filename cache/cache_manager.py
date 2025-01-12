from collections import deque

class CacheManager:

    LOG_SEARCHING_FOR_KEY = "\n[DEBUG - CacheManager] Buscando chave: {key}\n"
    LOG_KEY_ALREADY_EXISTS = "\n[DEBUG - CacheManager] Chave já existe no cache: {key}\n"
    LOG_REMOVING_OLD_KEY = "\n[DEBUG - CacheManager] Removendo chave antiga: {oldest_key}\n"
    LOG_ADDING_KEY = "\n[DEBUG - CacheManager] Adicionando chave: {key}, Valor: {value}\n"
    
    def __init__(self, max_size=None, debug=False):
        """
        Inicializa o gerenciador de cache.
        :param max_size: Tamanho máximo do cache (None para ilimitado).
        :param debug: Se True, imprime informações de debug.
        """
        self.cache = {}
        self.queue = deque()
        self.max_size = max_size
        self.debug = debug

    def get(self, key):

        """
        Recupera um valor do cache, se existir.
        :param key: Chave a ser buscada no cache.
        :return: Valor associado à chave ou None se não existir.
        """
        
        if self.debug:
            print(CacheManager.LOG_SEARCHING_FOR_KEY.format(key=key))
        
        return self.cache.get(key)

    def set(self, key, value):
        
        """
        Adiciona um novo valor ao cache, respeitando o limite de tamanho.
        :param key: Chave a ser adicionada.
        :param value: Valor associado à chave.
        """
        
        if key in self.cache:
            if self.debug:
                print(CacheManager.LOG_KEY_ALREADY_EXISTS.format(key=key))
            return 

        if self.max_size is not None and len(self.cache) >= self.max_size:
            
            oldest_key = self.queue.popleft()
            del self.cache[oldest_key]
            if self.debug:
                print(CacheManager.LOG_REMOVING_OLD_KEY.format(oldest_key=oldest_key))

        self.queue.append(key)
        self.cache[key] = value

        if self.debug:
            print(CacheManager.LOG_ADDING_KEY.format(key=key, value=value))

    def __len__(self):

        """
        Retorna o número de itens no cache.
        """
        return len(self.cache)