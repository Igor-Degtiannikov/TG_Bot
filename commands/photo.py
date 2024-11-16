from .base import Command
from telebot import types

class PhotoCommand(Command):
    def execute(self, message):
        """
        Handle the 'Photo' button press.
        Ask the user to send a photo.
        """
        self.bot.send_message(message.chat.id, 'Please send a photo.')

def register_photo_handlers(bot):
    """
    Register the photo handlers.
    """
    @bot.message_handler(content_types=['photo'])
    def handle_photo(message):
        """
        Handle received photos and send a chat ID instruction.
        """
        bot.send_message(message.chat.id, 'Photo received!')
        bot.send_message(
            message.chat.id,
            "To find the chat ID:\n"
            "1. Add this bot to the desired chat.\n"
            "2. Send any message in that chat.\n"
            "3. Reply to the message with the command `/get_chat_id`.\n"
            "The bot will show you the chat ID.",
            parse_mode='Markdown'
        )
New ПР










