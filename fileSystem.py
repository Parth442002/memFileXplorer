import os
from typing import List


# FileSystem class to implement linux commands
class FileSystem:
    def __init__(self) -> None:
        self.current_dir = "/"
        self.root = {"/": {}}

    def _get_absolute_path(self, path: str) -> str:
        if path.startswith("/"):
            return path
        return os.path.join(self.current_dir, path)

    def mkdir(self, dir_name: str):
        new_dir_path = self._get_absolute_path(dir_name)
        current = self.root
        children = [child for child in new_dir_path.split("/") if child]
        for child in children:
            current = current.setdefault(child, {})

    def ls(self, path: str = "") -> List:
        path = self._get_absolute_path(path)
        current = self.root
        components = path.split("/")
        for component in components:
            if component:
                current = current[component]
        result = list(current.keys())
        # TO Skip the current Dir
        if len(result) > 1:
            return result[1:]
        return result
