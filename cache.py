import os
import sys
from typing import List

class AbstractCache:
    def __init__(self):
        raise NotImplementedError

    def contains(self, target: str) -> bool:
        raise NotImplementedError

    def get(self, target: str) -> List[str]:
        raise NotImplementedError

    def add(self, target: str, friends: List[str]) -> None:
        raise NotImplementedError

    def delete(self, target: str) -> None:
        raise NotImplementedError

    def invalidate(self) -> int:
        raise NotImplementedError

    def flush(self) -> None:
        raise NotImplementedError


class DummyCache(AbstractCache):
    def __init__(self):
        pass
    
    def contains(self, target: str) -> bool:
        return False

    def get(self, target: str) -> List[str]:
        return "DUMMY"

    def add(self, target: str, friends: List[str]) -> None:
        pass

    def delete(self, target: str) -> None:
        pass

    def invalidate(self) -> int:
        return 0 

    def flush(self) -> None:
        pass


class FileCache(AbstractCache):
    """
       Filesystem-based caching
       Uses ramdisk by default
    """
    def __init__(self, path_to_cache: str = "/dev/shm") -> None:
        """path_to_cache may be changed to arbitrary path"""
        cache_folder_name = "newcon_cache"
        self.path_to_cache = os.path.join(path_to_cache, cache_folder_name)
        if "newcon_cache" not in os.listdir(path_to_cache):
            os.chdir(path_to_cache)
            os.mkdir(cache_folder_name)
        
        self.index = set([filename[:-4] for filename in os.listdir(self.path_to_cache) if filename.endswith(".lst")])
    
    def __new__(self):
        """This modification makes FileCache singleton, there's always only one instance of it"""
        if not hasattr(self, 'instance'):
            self.instance = super(FileCache, self).__new__(self)
        return self.instance

    def contains(self, target: str) -> bool:
        """Checks whether this user is in cache"""
        if target in self.index:
            return True
        else:
            return False
   
    def get(self, target: str) -> List[str]:
        """Gets user from cache, should be called only and only if 
           contains method succeeded. Friends are stored as ID per line"""
        filename = os.path.join(self.path_to_cache, f"{target}.lst")
        with open(filename, "r") as f:
            id_list = f.readlines()

        id_list = [num.strip() for num in id_list]
        return id_list

    def add(self, target: str, friends: List[str]) -> None:
        """Adds file with IDs to cache"""
        filename = os.path.join(self.path_to_cache, f"{target}.lst")
        with open(filename, "w") as f:
            try:
                friends = "\n".join(friends)
            except TypeError:
                friends = "\n".join([str(num) for num in friends])

            f.write(friends)

        self.index.add(target)

    def invalidate(self) -> int:
        """Invalidates cache based on time file created. Returns amount
           entries deleted from cache"""
        raise NotImplementedError

    def delete(self, target: str, clear_index: bool = True) -> None:
        """Deletes entry by ID"""
        filename = os.path.join(self.path_to_cache, f"{target}.lst")
        try:
            os.remove(filename)
        except FileNotFoundError:
            pass

        if clear_index:
            self.index.remove(target)

    def flush(self) -> None:
        """Deletes all entries in cache folder"""
        for target in self.index:
            self.delete(target, clear_index = False)

        self.index.clear()

