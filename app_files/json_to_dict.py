""" Module for converting .json to dictionary """

import json

class JsonToDict:
    """Json to Dict Converter
    """
    def __init__(self, filepath) -> None:
        """Convert `json` to `dictionary`

        Args:
            filepath (`str`): Filepath of the `.json` file to be converted
        """
        self.filepath = filepath

    def convert(self):
        """This is convert `json` to `dictionary`

        Raises:
            `FileNotFoundError`: Raises error when no file exists in filepath

        Returns:
            `dict`: Converted dictionary
        """
        with open(self.filepath, "r", encoding='UTF-8') as json_file:
            contents = dict(json.loads(json_file.read()))

        return contents
            