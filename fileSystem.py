import os
from typing import List
import re
import json


class FileSystem:
    def __init__(self) -> None:
        self.current_dir = "/"
        self.root = {"/": {}}

    def save_session(self, filename: str) -> None:
        """
        Method to Save current active terminal session
        """
        try:
            data = {"current_dir": self.current_dir, "root": self.root}
            with open(filename, "w") as file:
                json.dump(data, file, indent=2)
        except Exception as e:
            print(f"Error: Unable to save session in '{filename}': {e}")

    def load_session(self, filename: str) -> None:
        """
        Method to load a prev terminal session
        """
        try:
            with open(filename, "r") as file:
                data = json.load(file)

            self.current_dir = data.get("current_dir", "/")
            self.root = data.get("root", {"/": {}})

            print(f"Session loaded from {filename}")
        except FileNotFoundError:
            print(f"Error: Session file '{filename}' not found.")
        except json.JSONDecodeError as e:
            print(f"Error: Unable to decode JSON from '{filename}': {e}")
        except Exception as e:
            print(f"Error: Unable to load session from '{filename}': {e}")

    def _getAbsolutePath(self, path: str) -> str:
        """
        Method to get the absolute path
        """
        if path.startswith("/"):
            return path
        # return os.path.join(self.current_dir, path)
        return os.path.normpath(os.path.join(self.current_dir, path))

    def _isDirectory(self, path: str) -> bool:
        """
        To check if path leads to a Directory
        """
        path = self._getAbsolutePath(path)
        current = self.root
        components = path.split("/")
        for component in components:
            if component:
                current = current.get(component, {})

        return isinstance(current, dict)

    def _isValidPath(self, path: str) -> bool:
        """
        Private method to check if path is valid
        """
        path = self._getAbsolutePath(path)
        current = self.root
        components = path.split("/")
        for component in components:
            if component:
                current = current.get(component, {})

        return current is not None

    def _echoUpdateContent(self, file_path: str, content: str) -> None:
        """
        Private method to Update/override file content
        """
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
        """
        Private method to append to file
        """
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
        """
        method to parse echo command parameters
        """
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
        """
        Method to read text content inside a file
        """
        path = self._getAbsolutePath(path)
        current = self.root
        components = path.split("/")
        for component in components:
            if component:
                current = current.get(component, {})

        return current if isinstance(current, str) else ""

    def mkdir(self, dir_name: str):
        """
        Method to create a new folder
        """
        try:
            new_dir_path = self._getAbsolutePath(dir_name)
            current = self.root
            children = [child for child in new_dir_path.split("/") if child]
            for child in children:
                current = current.setdefault(child, {})
        except Exception as e:
            print(f"Error:': {e}")

    def ls(self, path: str = "") -> List:
        """
        Method to list all the files/folders in Directory
        """
        path = self._getAbsolutePath(path)
        current = self.root
        components = path.split("/")
        for component in components:
            if component:
                current = current[component]
        result = list(current.keys())
        return result

    def cd(self, path: str) -> None:
        """
        Methods to change the current working directory
        """
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
                    if destination[component] != None:
                        destination = destination.get(component, {})

            if isinstance(destination, dict):
                self.current_dir = destination_path
            else:
                print(f"{path}: Not a directory")

    def touch(self, file_path: str) -> None:
        """
        Create new file
        """
        try:
            file_path = self._getAbsolutePath(file_path)
            current = self.root
            components = file_path.split("/")

            # Traverse the file path and create directories if needed
            for component in components[:-1]:
                if component:
                    current = current.setdefault(component, {})

            # Create the new file
            current[components[-1]] = ""
        except Exception as e:
            print(f"touch: error creating file '{file_path}': {e}")

    def echo(self, echo_string: str) -> None:
        """
        Method to perform echo command to print/append/overide text in files
        """
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
        """
        Method to read file content
        """
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
        """
        Method to remove files/folder/directories
        """
        try:
            path = self._getAbsolutePath(path)
            current = self.root
            components = path.split("/")
            for component in components[:-1]:
                if component:
                    current = current.get(component, {})

            # Remove the file or directory
            del current[components[-1]]
        except KeyError:
            print(f"rm: cannot remove '{path}': No such file or directory")
        except Exception as e:
            print(f"rm: error removing '{path}': {e}")

    def grep(self, pattern: str, file_path: str) -> None:
        """
        To search for string pattern in files
        """
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

    def cp(self, source_path: str, destination_path: str = ".") -> None:
        """
        Method to copy paste files/directories/folders
        """
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

    def mv(self, source_path: str, destination_path: str) -> None:
        """
        Move files/folders
        """
        try:
            # Use cp to copy the source to the destination
            self.cp(source_path, destination_path)

            # Use rm to remove the source after copying
            self.rm(source_path)
        except Exception as e:
            print(f"mv: error moving '{source_path}' to '{destination_path}': {e}")
