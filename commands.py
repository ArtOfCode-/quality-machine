from ChatExchange.chatexchange.rooms import Room


class CommandResponse:
    def __init__(self, status: bool, message: str):
        self.status = status
        self.message = message


def command_help(event: dict, args: list) -> CommandResponse:
    return CommandResponse(True, "I'm a bot that detects low-quality contributions using machine-learning algorithms.")


# This dict lists commands by their name and defines their executable methods. Each key should be a str of the command
# name, and each value should be a typing.Callable[[dict, list], CommandResponse], where the dict argument is the data
# field of a ChatExchange.chatexchange.events.Event and the list field is the arguments to the command as sent in chat.
command_dict = {
    'help': command_help
}


def execute(room: Room, event_data: dict, command_name: str, args: list) -> None:
    global command_dict
    if command_name in command_dict:
        response = command_dict[command_name](event_data, args)
        if response.status:
            room.send_message(response.message)
        else:
            room.send_message("Error: {}".format(response.message))
    else:
        room.send_message("`{}`: no such command".format(command_name))
