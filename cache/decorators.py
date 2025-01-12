from functools import wraps

def cached(cache_manager):
    """
    Decorador para adicionar cache a um método.
    :param cache_manager: Instância de CacheManager ou DiskCacheManager.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            # Para as funções sum e mul, ordena os valores para garantir chaves consistentes
            if func.__name__ in ["sum", "mul"]:
                values = args[0]
                normalized_args = sorted(values) 
                print(normalized_args)
            else:
                normalized_args = args 
            
            key = f"{func.__name__}({', '.join(map(str, normalized_args))})"
            
            # Verifica se o resultado já está em cache
            cached_result = cache_manager.get(key)
            if cached_result is not None:
                return cached_result
            
            # Se não estiver em cache, executa a função e armazena o resultado
            result = func(self, *args, **kwargs)
            cache_manager.set(key, result)

            return result
        
        return wrapper
    
    return decorator