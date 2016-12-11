from sklearn import svm
import time
import json
from termcolor import cprint
import chat
from config import Config


def main():
    config = Config("config.json")

    cprint("Connecting to SE chat...", "blue")
    chat_client = chat.connect()
    cprint("Success.", "green")

    chat.watch_room(chat_client, config.get('control_room'), chat.process_event, config)
    cprint("Watching socket. Entering main event loop.", "blue")

    values, labels = load_classification_data(config.get("class_data_file"))

    while True:
        time.sleep(5)


def load_classification_data(data_file: str) -> (list, list):
    """
    Given a path to a data file, load the classification data contained in it into Python structures.
    :param data_file:
    :return: Two lists, the first containing class values and the second containing labelling information.
    """
    with open(data_file, "r") as f:
        data = json.load(f)

    values, labels = [], []
    for item in data['items']:
        values.append(item['class_values'])
        labels.append(item['label'])

    return values, labels

if __name__ == "__main__":
    main()
