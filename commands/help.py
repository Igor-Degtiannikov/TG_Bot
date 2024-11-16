from .base import Command
from telebot import types

class HelpCommand(Command):
    def execute(self, message):
        """
        Display help options and buttons for navigation.
        """
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        instruction_button = types.KeyboardButton('Instruction')
        about_button = types.KeyboardButton('What is ChatGPT')
        back_button = types.KeyboardButton('Back')
        markup.add(instruction_button, about_button, back_button)
        self.bot.send_message(
            message.chat.id,
            "Here are some options to help you:",
            reply_markup=markup
        )


def register_help_handlers(bot):
    """
    Register handlers for help-related buttons.
    """
    @bot.message_handler(func=lambda m: m.text == 'Instruction')New ПРNew ПР
    def send_instruction(message):
        """
        Handle the 'Instruction' button.
        Send instructions to the user on how to use the bot.
        """
        bot.send_message(
            message.chat.id,
            "1. Use the 'Using ChatGPT' button to ask questions.\n"
            "2. Type your question and wait for the bot to respond.\n"
            "3. Use 'Back' to return to the main menu."
        )

    @bot.message_handler(func=lambda m: m.text == 'What is ChatGPT')
    def send_about(message):
        """
        Handle the 'What is ChatGPT' button.
        Provide information about ChatGPT.
        """
        bot.send_message(
            message.chat.id,
            "ChatGPT is an advanced AI model developed by OpenAI. "
            "It can generate human-like text based on the input it receives."
        )

    @bot.message_handler(func=lambda m: m.text == 'Back')
    def go_back(message):
        """
        Handle the 'Back' button.
        Return the user to the main menu.
        """
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('Using ChatGPT')
        item2 = types.KeyboardButton('Help')
        item3 = types.KeyboardButton('Photo')
        markup.add(item1, item2, item3)
        bot.send_message(
            message.chat.id,
            "You are back in the main menu.",
            reply_markup=markup
        )



































