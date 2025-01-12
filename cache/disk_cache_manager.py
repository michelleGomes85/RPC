import os
import json
from collections import OrderedDict
from config.constants import N_CACHE_DISK, NAME_CACHE_DISK, ENCODING

class DiskCacheManager:

    LOG_FILE_IS_NOT_DICTIONARY = "\n[DEBUG - DiskCacheManager] Arquivo de cache não é um dicionário. Reinicializando cache.\n"
    LOG_ERROR_CACHE = "\n[DEBUG - DiskCacheManager] Erro ao carregar cache: {e}. Reinicializando cache.\n"
    LOG_SEARCHING_KEY = "\n[DEBUG - DiskCacheManager] Buscando chave: {key}\n"
    LOG_ADDING_KEY = "\n[DEBUG - DiskCacheManager] Inserindo chave: {key}, Valor: {value}\n"
    LOG_REMOVED_KEY = "\n[DEBUG - DiskCacheManager] Removendo chave antiga: {removed_key}\n"
    LOG_CLEAR_CACHE = "\n[DEBUG - DiskCacheManager] Limpando cache.\n"
    
    WRITE = 'w'
    READ = 'r'
    
    def __init__(self, cache_file, cache_limit=N_CACHE_DISK, debug=False):

        """
        Inicializa o gerenciador de cache.
        :param cache_file: Nome do arquivo onde o cache será armazenado.
        :param cache_limit: Número máximo de registros no cache.
        :param debug: Se True, imprime informações de debug.
        """

        self.cache_file = cache_file
        self.cache_limit = cache_limit
        self.debug = debug
        
        self._initialize_cache()
        self.dic_cache = self._load_cache()

    def _initialize_cache(self):

        """Cria o arquivo de cache se ele não existir."""

        if not os.path.exists(self.cache_file):
            with open(self.cache_file, self.WRITE) as file:
                json.dump({}, file) 

    def _save_cache(self):

        """Salva o cache em memória no disco."""

        with open(self.cache_file, self.WRITE) as file:
            json.dump(self.dic_cache, file)

    def _load_cache(self):

        """
        Carrega o cache do disco para a memória.
        Se o arquivo estiver corrompido ou mal formatado, reinicializa o cache.
        """

        try:
            with open(self.cache_file, self.READ) as file:
                cache = json.load(file)  
                if isinstance(cache, dict):
                    return OrderedDict(cache)
                else:
                    if self.debug:
                        print(DiskCacheManager.LOG_FILE_IS_NOT_DICTIONARY)

                    return OrderedDict()  
        except (json.JSONDecodeError, FileNotFoundError) as e:
            if self.debug:
                print(DiskCacheManager.LOG_ERROR_CACHE.format(e=e))

            return OrderedDict()

    def get(self, key):

        """
        Verifica se uma chave está no cache.
        :param key: Chave a ser verificada.
        :return: Valor associado à chave ou None se a chave não estiver no cache.
        """

        if self.debug:
            print(DiskCacheManager.LOG_SEARCHING_KEY.format(key=key))

        return self.dic_cache.get(str(key))

    def set(self, key, value):

        """
        Insere um registro no cache.
        :param key: Chave do registro.
        :param value: Valor associado à chave.
        """

        if self.debug:
            print(DiskCacheManager.LOG_ADDING_KEY.format(key=key, value=value))
        
        # Adiciona o novo valor ao cache em memória
        self.dic_cache[str(key)] = value

        # Remove os registros mais antigos se o cache exceder o limite
        while len(self.dic_cache) > self.cache_limit:
            removed_key, _ = self.dic_cache.popitem(last=False)
            if self.debug:
                print(DiskCacheManager.LOG_REMOVED_KEY.format(removed_key=removed_key))

        # Salva o cache atualizado no disco
        self._save_cache()

    def clear(self):
        
        """Limpa todo o cache."""

        if self.debug:
            print(DiskCacheManager.LOG_CLEAR_CACHE)

        self.dic_cache.clear()
        self._save_cache()

    def _size_in_cache(self):

        """
        Calcula o tamanho do cache em bytes.
        :return: Tamanho do cache em bytes.
        """

        json_string = json.dumps(self.dic_cache)
        return len(json_string.encode(ENCODING))