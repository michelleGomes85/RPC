import os
import json
from collections import OrderedDict

from config.config import N_CACHE_DISK, NAME_CACHE_DISK

class DiskCacheManager:
    
    WRITE = 'w'
    READ = 'r'
    
    def __init__(self, cache_file=NAME_CACHE_DISK, cache_limit=N_CACHE_DISK):
        
        """
        
        Inicializa o gerenciador de cache.

        :param cache_file: Nome do arquivo onde o cache será armazenado.
        :param cache_limit: Número máximo de registros no cache.
        
        """
        
        self.cache_file = cache_file
        self.cache_limit = cache_limit
        
        self._initialize_cache()

    def _initialize_cache(self):
        
        """Cria o arquivo de cache se ele não existir."""
        
        if not os.path.exists(self.cache_file):
            with open(self.cache_file, DiskCacheManager.WRITE) as f:
                json.dump(OrderedDict(), f)

    def _load_cache(self):
        
        """Carrega o cache do disco."""
        
        with open(self.cache_file, DiskCacheManager.READ) as f:
            return OrderedDict(json.load(f))

    def _save_cache(self, cache):
        
        """Salva o cache no disco."""
        
        with open(self.cache_file, DiskCacheManager.WRITE) as f:
            json.dump(cache, f)

    def get(self, key):
        
        """
        Verifica se uma chave está no cache.

        :param key: Chave a ser verificada.
        :return: Valor associado à chave ou None se a chave não estiver no cache.
        """
        
        cache = self._load_cache()
        return cache.get(str(key))

    def insert(self, key, value):
        
        """
        Insere um registro no cache.

        :param key: Chave do registro.
        :param value: Valor associado à chave.
        """
        
        cache = self._load_cache()
        cache[str(key)] = value
        
        if len(cache) > self.cache_limit:
            cache.popitem(last=False)  # Remove o mais antigo
            
        self._save_cache(cache)

    def remove(self, key):
        
        """
        Remove um registro do cache.

        :param key: Chave do registro a ser removido.
        """
        
        cache = self._load_cache()
        if str(key) in cache:
            del cache[str(key)]
            self._save_cache(cache)

    def clear(self):
        
        """Limpa todo o cache."""
        
        self._save_cache(OrderedDict())
