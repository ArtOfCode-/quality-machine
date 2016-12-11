from sklearn import svm
from typing import Any
import json


class SocketMessage:
    def __init__(self, action: str, data: Any):
        self.action = action
        self.data = json.dumps(data)

    def __str__(self) -> str:
        return "SocketMessage<action={}, data={}>".format(self.action, self.data)


class SocketResponse:
    def __init__(self, socket_response: SocketMessage=None, chat_response: str=None):
        self.socket = socket_response
        self.chat = chat_response

    def __str__(self) -> str:
        return "SocketResponse<socket={}, chat={}>".format(str(self.socket), self.chat)


def handle_frame(action: str, data: dict) -> SocketResponse:
    """
    Handles a single received message from the websocket.
    :param action: The action received from the websocket.
    :param data: The deserialized data from the websocket frame.
    :param clf: A machine-learning classifier instance.
    :return: A SocketResponse for the supercaller to process.
    """
    action_handlers = {
        'hb': handle_heartbeat,
        '97-questions-newest': handle_new_question
    }
    if action in action_handlers:
        return action_handlers[action](data)
    else:
        return SocketResponse()


def handle_heartbeat(data: dict) -> SocketResponse:
    return SocketResponse(socket_response=SocketMessage("hb", "hb"))

def handle_new_question(data: dict) -> SocketResponse:
    """
    Processes a new question, as reported by the websocket.
    :param data: The deserialized data from the websocket frame.
    :param clf: A machine-learning classifier instance.
    :return: A SocketResponse for the supercaller to process.
    """
    print(data)
    return SocketResponse(chat_response="New question posted: [{0}](http://english.stackexchange.com/q/{0})".format(data['id']))
