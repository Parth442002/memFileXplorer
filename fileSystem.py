import os
from typing import List


class FileSystem:
    def __init__(self) -> None:
        self.current_dir = "/"
        self.root = {"/": {}}

    # Private Method to get Absolute Path
    def _get_absolute_path(self, path: str) -> str:
        if path.startswith("/"):
            return path
        return os.path.join(self.current_dir, path)

    # Method to make a new folder
    def mkdir(self, dir_name: str):
        new_dir_path = self._get_absolute_path(dir_name)
        current = self.root
        children = [child for child in new_dir_path.split("/") if child]
        for child in children:
            current = current.setdefault(child, {})

    # Method to list all children
    def ls(self, path: str = "") -> List:
        path = self._get_absolute_path(path)
        current = self.root
        components = path.split("/")
        for component in components:
            if component:
                current = current[component]
        result = list(current.keys())
        return result

    # Method to change current_directory
    def cd(self, path: str) -> None:
        if path == "/":
            self.current_dir = "/"
        elif path == "~":
            self.current_dir = "/"
        elif path == "..":
            components = self.current_dir.split("/")
            self.current_dir = "/".join(components[:-1])
            if not self.current_dir:
                self.current_dir = "/"
        else:
            destination_path = self._get_absolute_path(path)

            # Check if the destination is a directory
            destination = self.root
            components = destination_path.split("/")
            for component in components:
                if component:
                    destination = destination.get(component, {})

            if isinstance(destination, dict):
                self.current_dir = destination_path
            else:
                print(f"{path}: Not a directory")

    def touch(self, file_path: str) -> None:
        file_path = self._get_absolute_path(file_path)
        current = self.root
        children = file_path.split("/")
        for child in children[:-1]:
            if child:
                current = current.setdefault(child, {})
        current[children[-1]] = ""
