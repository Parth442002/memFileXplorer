import os
from typing import List
import re


class FileSystem:
    def __init__(self) -> None:
        self.current_dir = "/"
        self.root = {"/": {}}

    # Private Method to get Absolute Path
    def _getAbsolutePath(self, path: str) -> str:
        if path.startswith("/"):
            return path
        return os.path.join(self.current_dir, path)

    def _isDirectory(self, path: str) -> bool:
        path = self._getAbsolutePath(path)
        current = self.root
        components = path.split("/")
        for component in components:
            if component:
                current = current.get(component, {})

        return isinstance(current, dict)

    def _isValidPath(self, path: str) -> bool:
        path = self._getAbsolutePath(path)
        current = self.root
        components = path.split("/")
        for component in components:
            if component:
                current = current.get(component, {})

        return current is not None

    def _echoUpdateContent(self, file_path: str, content: str) -> None:
        file_path = self._getAbsolutePath(file_path)
        current = self.root
        components = file_path.split("/")

        # Traverse the file path and create directories if needed
        for component in components[:-1]:
            if component:
                current = current.setdefault(component, {})

        # Update or create the file with the specified content
        current[components[-1]] = content

    def _echoAppendContent(self, file_path: str, content: str) -> None:
        file_path = self._getAbsolutePath(file_path)
        current = self.root
        components = file_path.split("/")

        # Traverse the file path and create directories if needed
        for component in components[:-1]:
            if component:
                current = current.setdefault(component, {})

        # Append the content to the existing file or create a new file
        current[components[-1]] = current.get(components[-1], "") + content

    def _echoCommandParser(self, string: str):
        echo_parts = string.split(" ")
        quoted_contents = re.findall(r"'(.*?)'|\"(.*?)\"", string)
        # Use the first non-empty quoted content found
        quoted_content = next(
            (content for content in sum(quoted_contents, ()) if content), None
        )

        filename = echo_parts[-1]
        operation = echo_parts[-2] if len(echo_parts) > 2 else None

        return quoted_content, operation, filename

    def _getFileContent(self, path: str) -> str:
        path = self._getAbsolutePath(path)
        current = self.root
        components = path.split("/")
        for component in components:
            if component:
                current = current.get(component, {})

        return current if isinstance(current, str) else ""

    # Method to make a new folder
    def mkdir(self, dir_name: str):
        new_dir_path = self._getAbsolutePath(dir_name)
        current = self.root
        children = [child for child in new_dir_path.split("/") if child]
        for child in children:
            current = current.setdefault(child, {})

    # Method to list all children
    def ls(self, path: str = "") -> List:
        path = self._getAbsolutePath(path)
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
            destination_path = self._getAbsolutePath(path)

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
        file_path = self._getAbsolutePath(file_path)
        current = self.root
        children = file_path.split("/")
        for child in children[:-1]:
            if child:
                current = current.setdefault(child, {})
        current[children[-1]] = ""

    def echo(self, echo_string: str) -> None:
        content, operation, filename = self._echoCommandParser(echo_string)

        if operation == ">":
            self._echoUpdateContent(filename, content)
        elif operation == ">>":
            self._echoAppendContent(filename, content)
        else:
            if content:
                print(content)
            else:
                print(
                    "Invalid operation. Use '>' to update/override or '>>' to append."
                )

    def cat(self, file_path: str) -> None:
        file_path = self._getAbsolutePath(file_path)
        current = self.root
        components = file_path.split("/")

        # Traverse the file path
        for component in components:
            if component:
                current = current.get(component, {})

        # Check if the path points to a file
        if isinstance(current, str):
            content = current
            if content:
                print(content)
            else:
                print(f"cat: {file_path}: File is empty")
        else:
            print(f"cat: {file_path}: Is a directory or does not exist")

    def rm(self, path: str) -> None:
        path = self._getAbsolutePath(path)
        current = self.root
        components = path.split("/")
        for component in components[:-1]:
            if component:
                current = current.get(component, {})

        # Remove the file or directory
        del current[components[-1]]

    def grep(self, pattern: str, file_path: str) -> None:
        file_path = self._getAbsolutePath(file_path)
        # Check if the file exists
        if not self._isValidPath(file_path):
            print(f"grep: '{file_path}': No such file or directory")
            return

        # Check if the file is a directory
        if self._isDirectory(file_path):
            print(f"grep: '{file_path}': Is a directory")
            return

        try:
            # Read the content of the file
            content = self._getFileContent(file_path)

            # Use regular expression to find matches
            matches = re.findall(pattern, content)

            # Print the matches or "No match found"
            if matches:
                print("The following Matches were found:-")
                for match in matches:
                    print(match)
            else:
                print("No match found")
        except Exception as e:
            print(f"grep: error reading '{file_path}': {e}")
