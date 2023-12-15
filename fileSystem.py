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
        # return os.path.join(self.current_dir, path)
        return os.path.normpath(os.path.join(self.current_dir, path))

    # Private method to check if path is a dir
    def _isDirectory(self, path: str) -> bool:
        path = self._getAbsolutePath(path)
        current = self.root
        components = path.split("/")
        for component in components:
            if component:
                current = current.get(component, {})

        return isinstance(current, dict)

    # Private method to check if path already exists or not
    def _isValidPath(self, path: str) -> bool:
        path = self._getAbsolutePath(path)
        current = self.root
        components = path.split("/")
        for component in components:
            if component:
                current = current.get(component, {})

        return current is not None

    # Private method to Update file content
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

    # parse parameters from the echo command
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

    # Read file content
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

    # Method to create new file
    def touch(self, file_path: str) -> None:
        file_path = self._getAbsolutePath(file_path)
        current = self.root
        children = file_path.split("/")
        for child in children[:-1]:
            if child:
                current = current.setdefault(child, {})
        current[children[-1]] = ""

    # Method to add/append/print data
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

    # Method to read files
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

    # Method to remove
    def rm(self, path: str) -> None:
        try:
            path = self._getAbsolutePath(path)
            current = self.root
            components = path.split("/")
            for component in components[:-1]:
                if component:
                    current = current.get(component, {})

            # Remove the file or directory
            del current[components[-1]]
            print(f"rm: '{path}' removed")
        except KeyError:
            print(f"rm: cannot remove '{path}': No such file or directory")
        except Exception as e:
            print(f"rm: error removing '{path}': {e}")

    # Method to search for patterns in file
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

    # Method to copy files/folders
    def cp(self, source_path: str, destination_path: str = ".") -> None:
        source_path = self._getAbsolutePath(source_path)
        destination_path = self._getAbsolutePath(destination_path)

        # Check if the source path exists
        if not self._isValidPath(source_path):
            print(f"cp: cannot stat '{source_path}': No such file or directory")
            return

        # Working with relative Imports
        if destination_path == ".":
            destination_path = self.current_dir
        elif destination_path == "..":
            components = self.current_dir.split("/")
            destination_path = "/".join(components[:-1])
            if not destination_path:
                destination_path = "/"
        elif destination_path == "~":
            destination_path = "/"

        # Check if the destination path is a directory
        if self._isDirectory(destination_path):
            # If the destination is a directory, construct the destination path within that directory
            destination_path = os.path.join(
                destination_path, os.path.basename(source_path)
            )

        try:
            if self._isDirectory(source_path):
                # If source is a directory, create the destination directory
                self.mkdir(destination_path)
                # Copy each file from the source directory to the destination directory
                for item in self.ls(source_path):
                    item_source = os.path.join(source_path, item)
                    item_destination = os.path.join(destination_path, item)
                    if self._isDirectory(item_source):
                        self.cp(item_source, item_destination)
                    else:
                        self.touch(item_destination)
                        content = self._getFileContent(item_source)
                        self.echo(f'echo "{content}" > {item_destination}')
            else:
                # If source is a file, create the destination file and copy the content
                self.touch(destination_path)
                content = self._getFileContent(source_path)
                self.echo(f'echo "{content}" > {destination_path}')
        except Exception as e:
            print(f"cp: error copying '{source_path}' to '{destination_path}': {e}")

    # Methods to move files/folders
    def mv(self, source_path: str, destination_path: str) -> None:
        try:
            # Use cp to copy the source to the destination
            self.cp(source_path, destination_path)

            # Use rm to remove the source after copying
            self.rm(source_path)
            print(f"mv: '{source_path}' moved to '{destination_path}'")
        except Exception as e:
            print(f"mv: error moving '{source_path}' to '{destination_path}': {e}")
