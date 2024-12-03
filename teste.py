
from cache.disk_cache_manager import DiskCacheManager

cache_manager = DiskCacheManager()

cache_manager.insert(1, False)
cache_manager.insert(2, True)
cache_manager.insert(3, True)
cache_manager.insert(10000000000000000000000000, True)
cache_manager.insert(4, True)
cache_manager.insert(5, True)
cache_manager.insert(9, True)
cache_manager.insert(100000000000000000000000000, True)
cache_manager.insert(12, True)
cache_manager.insert(100, True)
cache_manager.insert(200, True)

