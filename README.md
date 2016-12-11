# quality-machine
Machine learning for detecting low-quality contributions on http://english.stackexchange.com.

## Setup
QM maintains a list of dependencies in `requirements.txt`. You can also use this file to install requirements directly:

    you@yourpc:~$ sudo -H python3 -m pip install -r requirements.txt

You'll need to copy the example config across to a real config file:

    you@yourpc:~$ cp config.sample.json config.json

Once you're done there, you can run the project by executing the `main.py` file.

    you@yourpc:~$ python3 main.py

You'll need an account on [StackExchange](http://stackexchange.com) that has access to chat. You'll be prompted for its
username and password each time you run the bot, though you can save them in the `ChatExchangeU` and `ChatExchangeP`
environment variables if you want.

## Configuration
QM is configured from a JSON configuration file, `config.json`. The important fields are:

 - `location`: a description of who, or what, is running the bot. Example: `ArtOfCode/EC2`.
 - `control_room`: a numeric ID of the room you want the bot to run in.
 - `command_prefix`: a string that the bot will use to identify commands it's being sent.
 - `class_data_file`: a path to a JSON file containing classification data.

## Classification data
The `class_data_file` field in the config file should point to another JSON file containing classification data. This
data should also be in a specific format. You will not normally need to touch this file - the bot will read and write it
as necessary for normal operation. The format is as such:

    {
        "items": [
            {
                "class_values": [8.792, 12.01, 197.6, 83, 22.059],
                "label": 1
            },
            {
                "class_values": [0.192, 6.7, 20.5, 15.15, 4.82],
                "label": 0
            }
        ]
    }

That is, `items` should be an array of objects, each of which contains a `class_values` and a `label` field. The
`class_values` field is an array of values for each classification class, and the `label` field indicates the desired
result of a classification - okay, or low quality.
