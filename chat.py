from getpass import getpass
from typing import Callable
from termcolor import cprint, colored
from ChatExchange.chatexchange.client import Client
from ChatExchange.chatexchange.events import Event
from config import Config
import util
import commands


config = None
rooms = {}


def connect() -> Client:
    """
    Creates a Client instance and logs it into chat, then returns it.
    :return: A ChatExchange Client instance for use in chat comms.
    """
    username = util.environ_or_none('ChatExchangeU')
    password = util.environ_or_none('ChatExchangeP')

    if username is None:
        username = input("Chat username: ")

    if password is None:
        password = getpass("Chat password: ")

    client = Client("stackexchange.com")
    client.login(username, password)

    return client


def watch_room(client: Client, room_id: int, event_callback: Callable[[Event, Client], None],
               config_instance: Config) -> None:
    """
    Starts a socket watcher on the provided client for the specified room, with a callback for event processing.
    :param client: The CE Client to use for the watcher.
    :param room_id: The ID of the room to watch.
    :param event_callback: A method that will be called when an event occurs.
    :return: None.
    """
    global config, rooms
    config = config_instance

    room = client.get_room(room_id)
    room.join()
    room.watch_socket(event_callback)
    rooms[room_id] = room


def send_message(room_id: int, message: str) -> None:
    """
    Sends a message to the specified room.
    :param room_id: Integer room ID. Must already be in the rooms list - i.e. already have had watch_room called on it.
    :param message: Message to send.
    :return: None.
    """
    global config, rooms
    if room_id in rooms:
        rooms[room_id].send_message("[ [Quality Machine]({}) ] {}".format(config.get('repo'), message))
    else:
        raise ValueError("Invalid room ID.")


def process_event(event: Event, chat_client: Client) -> None:
    """
    Given an event from chat, delegate its processing.
    :param event: A ChatExchange Event, describing the activity.
    :param chat_client: The ChatExchange Client that the event was triggered on.
    :return: None.
    """
    event_handlers = {
        1: handle_message,
        2: handle_message,
        3: handle_user_join,
        4: handle_user_leave,
        18: handle_reply
    }
    if 'event_type' in event.data:
        if event.data['event_type'] in event_handlers:
            event_handlers[event.data['event_type']](event.data, chat_client)


def handle_message(data: dict, chat_client: Client) -> None:
    """
    Handle a message having been posted in a room.
    :param data: Data associated with the event.
    :param chat_client: The ChatExchange Client instance the event occurred on.
    :return: None
    """
    global config, control_room
    message = data['content']
    command_prefix = config.get('command_prefix')
    if message.startswith(command_prefix):
        print(colored("Received command: ", "blue", attrs=["bold"]) + message)
        parts = message.split(' ')
        command_name = parts[0][len(command_prefix):]
        args = parts[1:]
        room = rooms[data['room_id']]
        commands.execute(room, data, command_name, args)


def handle_user_join(data: dict, chat_client: Client) -> None:
    """
    Handle a user joining a room.
    :param data: Data associated with the event.
    :param chat_client: The ChatExchange Client instance the event occurred on.
    :return: None
    """
    pass


def handle_user_leave(data: dict, chat_client: Client) -> None:
    """
    Handle a user leaving a room.
    :param data: Data associated with the event.
    :param chat_client: The ChatExchange Client instance the event occurred on.
    :return: None
    """
    pass


def handle_reply(data: dict, chat_client: Client) -> None:
    """
    Handle a message being replied to.
    :param data: Data associated with the event.
    :param chat_client: The ChatExchange Client instance the event occurred on.
    :return: None
    """
    pass
