import logging
import openai
from .base import Command
from states import ChatBotStates

class ChatGPTCommand(Command):
    def execute(self, message):
        """
        Handle the 'Using ChatGPT' button press.
        """
        logging.info(f"Handling 'Using ChatGPT' command for user {message.chat.id}")
        self.bot.send_message(message.chat.id, 'Write your question for ChatGPT:')
        self.bot.set_state(message.chat.id, ChatBotStates.WAITING_FOR_CHATGPT_INPUT)


def register_chatgpt_handlers(bot):
    """
    Register the state handler for ChatGPT input.
    """
    logging.info("Registering ChatGPT handlers...")

    @bot.message_handler(state=ChatBotStates.WAITING_FOR_CHATGPT_INPUT)
    def process_chatgpt_input(message):
        user_message = message.text
        try:
            logging.info(f"Processing ChatGPT input from user {message.chat.id}")
            response = openai.Completion.create(
                engine='text-davinci-003',
                prompt=user_message,
                max_tokens=50,
                temperature=0.7
            )
            bot.send_message(message.chat.id, response.choices[0].text.strip())
        except Exception as e:
            logging.error(f"Error while processing ChatGPT input: {str(e)}")
            bot.send_message(message.chat.id, f"An error occurred: {str(e)}")

        # Return to the main menu
        bot.set_state(message.chat.id, ChatBotStates.MAIN_MENU)
        bot.send_message(message.chat.id, "You are back in the main menu.")







