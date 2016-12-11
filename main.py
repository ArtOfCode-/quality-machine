from sklearn import svm
import time
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
    while True:
        time.sleep(5)

if __name__ == "__main__":
    main()
