import os
from pathlib import Path


class FilePathResolver(object):
    """
    This class manages the paths of the data to be processed.
    Exposing the path of valid files in the given directory, recursively.
    """

    FILE_EXTENSION = ".xml"

    def __init__(self, data_path: str) -> None:
        self._data_path = data_path

        self._files = None

    @property
    def files(self) -> list:
        """
        Resolves and returns the files in the given path
        that matches, converted to lowercase,
        the set file extension (FilePathResolver.FILE_EXTENSION).
        """
        if self._files is None:
            self._files = [
                file
                for file in Path(self._data_path).rglob("*")
                # This will cover any variation of ".xml" like
                # .XML, .Xml, .XmL ...
                if file.suffix.lower() == self.FILE_EXTENSION
                # Excluding directories
                and not os.path.isdir(file.absolute())
            ]
        return self._files
