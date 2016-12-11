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


def handle_frame(action: str, data: dict, clf: svm.SVC) -> SocketResponse:
    """
    Handles a single received message from the websocket.
    :param action: The action received from the websocket.
    :param data: The deserialized data from the websocket frame.
    :param clf: A machine-learning classifier instance.
    :param client: A ChatClient we can use for talking to chat.
    :return: None.
    """
    action_handlers = {
        'hb': handle_heartbeat
    }
    if action in action_handlers:
        return action_handlers[action](data, clf)
    else:
        return SocketResponse()


def handle_heartbeat(data: dict, clf: svm.SVC) -> SocketResponse:
    return SocketResponse(socket_response=SocketMessage("hb", "hb"))
