from sklearn import svm
import numpy as np
import websocket
import json
from termcolor import cprint, colored
import chat
from config import Config
import sockets


def main():
    config = Config("config.json")

    cprint("Connecting to SE chat...", "blue")
    chat_client = chat.connect()
    cprint("Success.", "green")

    chat.watch_room(chat_client, config.get('control_room'), chat.process_event, config)
    cprint("Watching socket. Entering main event loop.", "blue")

    values, labels = load_classification_data(config.get("class_data_file"))
    clf = svm.SVC()
    clf.fit(values, labels)

    chat.send_message(config.get('control_room'), "Started with {} classification records loaded. "
                      "Running on {}.".format(len(labels), config.get('location')))
    cprint("{} classifier records loaded.", "blue", attrs=['bold'])

    ws = websocket.create_connection("ws://qa.sockets.stackexchange.com/")
    ws.send("97-questions-newest")

    while True:
        received = ws.recv()
        json_frame = json.loads(received)
        action_name = json_frame['action']
        frame_data = json.loads(json_frame['data'])

        print(colored("WS frame received: ", "yellow", attrs=['bold']) + received)

        response = sockets.handle_frame(action_name, frame_data)
        print(colored("WS frame response: ", "yellow", attrs=['bold']) + response)

        if response.socket:
            ws.send(json.dumps({'action': response.socket.action, 'data': response.socket.data}))

        if response.chat:
            chat.send_message(config.get('control_room'), response.chat)


def load_classification_data(data_file: str) -> (list, list):
    """
    Given a path to a data file, load the classification data contained in it into Python structures.
    :param data_file:
    :return: Two lists, the first containing class values and the second containing labelling information.
    """
    with open(data_file, "r") as f:
        data = json.load(f)

    values = np.array([x['class_values'] for x in data['items']])
    labels = np.array([x['label'] for x in data['item']])

    return values, labels

if __name__ == "__main__":
    main()
