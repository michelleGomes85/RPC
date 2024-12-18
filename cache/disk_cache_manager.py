import os
import json
from collections import OrderedDict

from config.constants import N_CACHE_DISK, NAME_CACHE_DISK, ENCODING

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
        self.dic_cache = self._load_cache()

    def _initialize_cache(self):
        
        """Cria o arquivo de cache se ele não existir."""
        
        if not os.path.exists(self.cache_file):
            with open(self.cache_file, DiskCacheManager.WRITE) as file:
                json.dump(OrderedDict(), file)
    
    def _save_cache(self, cache):
        
        """Salva o cache no disco."""
        
        with open(self.cache_file, DiskCacheManager.WRITE) as file:
            json.dump(cache, file)

    def _load_cache(self):
        
        """Carrega o cache do disco, e coloca em um dicionario -> Usa OrderedDict, para ele ficar na estrutura FIFO"""
        
        with open(self.cache_file, DiskCacheManager.READ) as file:
            return OrderedDict(json.load(file))

    def get(self, key):
        
        """
        Verifica se uma chave está no cache.

        :param key: Chave a ser verificada.
        :return: Valor associado à chave ou None se a chave não estiver no cache.
        """
        
        return self.dic_cache.get(str(key))

    def insert(self, key, value):
        
        """
        Insere um registro no cache.

        :param key: Chave do registro.
        :param value: Valor associado à chave.
        """
        
        cache = self.dic_cache

        cache[str(key)] = value

        size_cache = self._size_in_cache(cache)

        while size_cache > self.cache_limit:
            cache.popitem(last=False)
            size_cache = self._size_in_cache(cache)
    
        self._save_cache(cache)
        self.dic_cache = self._load_cache()

    def clear(self):
        
        """Limpa todo o cache."""
        
        self._save_cache(OrderedDict())

    def _size_in_cache(self, cache):
        
        # Convertendo o JSON para uma string
        json_string = json.dumps(cache)

        # Obtendo o tamanho em bytes
        size_in_cache = len(json_string.encode(ENCODING))

        return size_in_cache