from .chatgpt import ChatGPTCommand
from .help import HelpCommand
from .photo import PhotoCommand

def get_commands(bot):
    """
    Returns a dictionary of commands, where the key is the command text
    and the value is the command object.
    """
    return {
        'Using ChatGPT': ChatGPTCommand(bot),
        'Help': HelpCommand(bot),
        'Photo': PhotoCommand(bot)
    }
New ПР





