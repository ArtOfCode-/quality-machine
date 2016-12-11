from ChatExchange.chatexchange.rooms import Room


class CommandResponse:
    def __init__(self, status: bool, message: str):
        self.status = status
        self.message = message


def command_help(event: dict, args: list) -> CommandResponse:
    """
    Constant command - return a vaguely useful string describing the bot's function.
    :param event: Unused event data.
    :param args: Unused argument list.
    :return: A constant CommandResponse.
    """
    return CommandResponse(True, "I'm a bot that detects low-quality contributions using machine-learning algorithms.")


def command_alive(event: dict, args: list) -> CommandResponse:
    """
    Constant command - return a string, just to indicate that the bot's alive.
    :param event: Unused event data.
    :param args: Unused argument list.
    :return: A constant CommandResponse.
    """
    return CommandResponse(True, "You'll have to try harder than that to kill me.")


# This dict lists commands by their name and defines their executable methods. Each key should be a str of the command
# name, and each value should be a typing.Callable[[dict, list], CommandResponse], where the dict argument is the data
# field of a ChatExchange.chatexchange.events.Event and the list field is the arguments to the command as sent in chat.
command_dict = {
    'help': command_help,
    'alive': command_alive
}


def execute(room: Room, event_data: dict, command_name: str, args: list) -> None:
    """
    Finds and runs a command specified by its name.
    :param room: The ChatExchange Room that the command was run in.
    :param event_data: The data field of a ChatExchange.chatexchange.events.Event.
    :param command_name: The name of the command to execute, without the prefix.
    :param args: A list of arguments to pass to the command.
    :return: None
    """
    global command_dict
    if command_name in command_dict:
        response = command_dict[command_name](event_data, args)
        if response.status:
            room.send_message(response.message)
        else:
            room.send_message("Error: {}".format(response.message))
    else:
        room.send_message("`{}`: no such command".format(command_name))
