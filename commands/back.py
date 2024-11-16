from telebot import types
from states import ChatBotStates

class BackCommand:
    def __init__(self, bot):
        self.bot = bot

    def register(self):
        """
        Register the handler for the 'Back' button.
        """
        @self.bot.message_handler(func=lambda message: message.text == 'Back')
        def back_to_main_menu(message):
            """
            Handle the 'Back' button. Return the user to the main menu.
            """
            self.bot.set_state(message.chat.id, ChatBotStates.MAIN_MENU)

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('Using ChatGPT')
            item2 = types.KeyboardButton('Help')
            item3 = types.KeyboardButton('Photo')
            markup.add(item1, item2, item3)

            self.bot.send_message(
                message.chat.id,
                "You are back in the main menu.",
                reply_markup=markup
            )
New ПР

























