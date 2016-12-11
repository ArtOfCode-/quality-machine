from sklearn import svm
import time
import chat
from config import Config


def main():
    config = Config("config.json")
    chat_client = chat.connect()
    chat.watch_room(chat_client, config.get('control_room'), chat.process_event, config)
    while True:
        time.sleep(5)

if __name__ == "__main__":
    main()
