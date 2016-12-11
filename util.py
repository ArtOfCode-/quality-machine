from typing import Union
import os


def environ_or_none(name: str) -> Union[str, None]:
    """
    Retrieve a value from the environment, or None if it doesn't exist.
    :param name: The name of the environment variable to retrieve.
    :return:
    """
    if name in os.environ:
        return os.environ[name]
    else:
        return None
