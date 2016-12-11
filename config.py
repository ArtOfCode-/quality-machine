import json


class Config:
    def __init__(self, file_name: str):
        """
        Create a new Config instance with a specified config file, and parse the file.
        :param file_name: A path to a JSON config file.
        """
        self.file = file_name
        with open(self.file) as f:
            self.config = json.load(f)

    def get(self, prop_name: str):
        """
        Retrieve the property specified in prop_name or None if it doesn't exist.
        :param prop_name: Name of the property to retrieve.
        :return: Value of the property, or None.
        """
        return self.config[prop_name] if prop_name in self.config else None
