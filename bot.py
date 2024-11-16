import json
import logging
import telebot
from telebot import types
from telebot.storage import StateMemoryStorage
from telebot.custom_filters import StateFilter
from dotenv import load_dotenv
import openai
import config

from states import ChatBotStates
from commands.commands_registry import get_commands
from commands.chatgpt import register_chatgpt_handlers
from commands.help import register_help_handlers
from commands.back import BackCommand
from commands.photo import register_photo_handlers


# Logging configuration
logging.basicConfig(level=logging.INFO)

# Load environment variables
load_dotenv()

# Initialize bot and FSM storage
storage = StateMemoryStorage()
bot = telebot.TeleBot(config.TELEGRAM_API_KEY, state_storage=storage)
bot.add_custom_filter(StateFilter(bot))
openai.api_key = config.CHAT_API_KEY

def load_users():
    """Load the list of users from the 'users.json' file."""
    try:
        with open('users.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_users(users):
    """Save the updated list of users to the 'users.json' file."""
    with open('users.json', 'w') as file:
        json.dump(users, file)

@bot.message_handler(commands=['start'])
def start_message(message):
    """
    Handle the /start command.
    Greets the user and distinguishes between new and returning users.
    """
    logging.info(f"User {message.chat.id} issued /start command.")
    users = load_users()
    user_id = str(message.chat.id)

    if user_id not in users:
        logging.info(f"New user detected: {user_id}")
        bot.send_message(
            message.chat.id,
            "Hello! I am a bot that can use ChatGPT. Nice to meet you!"
        )
        users[user_id] = True
        save_users(users)
    else:
        logging.info(f"Returning user detected: {user_id}")
        bot.send_message(
            message.chat.id,
            "Welcome back! Glad to see you again. How can I help you today?"
        )

    show_main_menu(message)

def show_main_menu(message):
    """Display the main menu with options."""
    logging.info(f"Displaying main menu to user {message.chat.id}")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Using ChatGPT')
    item2 = types.KeyboardButton('Help')
    item3 = types.KeyboardButton('Photo')
    markup.add(item1, item2, item3)
    bot.send_message(message.chat.id, "Please choose an option:", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def message_reply(message):
    """
    Handle user text messages and execute the corresponding command.
    """
    logging.info(f"User {message.chat.id} sent a message: {message.text}")

    commands = get_commands(bot)
    handler = commands.get(message.text)
    if handler:
        logging.info(f"Executing command handler for {message.text}")
        handler.execute(message)
    else:
        logging.warning(f"Unknown command: {message.text}")
        bot.send_message(
            message.chat.id,
            "Unknown command. Please select an option from the menu."
        )

# Register handlers for specific commands and features
logging.info("Registering ChatGPT handlers...")
register_chatgpt_handlers(bot)

logging.info("Registering Help handlers...")
register_help_handlers(bot)

logging.info("Registering Photo handlers...")
register_photo_handlers(bot)

logging.info("Registering Back handlers...")
back_command = BackCommand(bot)
back_command.register()

logging.info("Bot is starting polling...")
if __name__ == "__main__":
    bot.infinity_polling()


New ПР

