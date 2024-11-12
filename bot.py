import telebot
from telebot import types
import openai
import config
from dotenv import load_dotenv
import os
import json

load_dotenv()

bot = telebot.TeleBot(config.TELEGRAM_API_KEY)
openai.api_key = config.CHAT_API_KEY


def load_users():
    """Loads the list of users from the users.json file"""
    try:
        with open('users.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_users(users):
    """Saves the updated list of users to the users.json file"""
    with open('users.json', 'w') as file:
        json.dump(users, file)


@bot.message_handler(commands=['start'])
def start_message(message):
    """Sends a welcome message to a new user and adds them to the user list"""
    users = load_users()
    user_id = str(message.chat.id)

    if user_id not in users:
        bot.send_message(message.chat.id, 'Hello! I am a bot that can use ChatGPT.')
        users[user_id] = True
        save_users(users)
    else:
        bot.send_message(message.chat.id, "Welcome back! Here's what I can do for you:")

    show_main_menu(message)


def show_main_menu(message):
    """Displays the main menu with options"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Using ChatGPT')
    item2 = types.KeyboardButton('Help')
    item3 = types.KeyboardButton('Photo')
    markup.add(item1, item2, item3)
    bot.send_message(message.chat.id, 'Pick what you want', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def message_reply(message):
    """Processes text messages and performs actions based on user choice"""
    if message.text == 'Using ChatGPT':
        bot.send_message(message.chat.id, 'Write the message:')
        bot.register_next_step_handler(message, get_chatgpt_response)
    elif message.text == 'Photo':
        bot.send_message(message.chat.id, 'Please send a photo:')
    elif message.text == 'Help':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        instruction_button = types.KeyboardButton('Instruction')
        about_button = types.KeyboardButton('What is ChatGPT')
        back_button = types.KeyboardButton('Back')
        markup.add(instruction_button, about_button, back_button)
        bot.send_message(message.chat.id, 'Here are some options to help you:', reply_markup=markup)
    elif message.text == 'Instruction':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        back_button = types.KeyboardButton('Back')
        markup.add(back_button)
        bot.send_message(message.chat.id, 'Select “Using ChatGPT”, then post your question, and wait for a response.')
    elif message.text == 'What is ChatGPT':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        back_button = types.KeyboardButton('Back')
        markup.add(back_button)
        bot.send_message(message.chat.id, 'ChatGPT is an advanced AI language model developed by OpenAI')
    elif message.text == 'Find Chat ID':
        bot.send_message(
            message.chat.id,
            "To find the chat ID:\n1. Add this bot to the desired chat.\n"
            "2. Send any message in that chat.\n"
            "3. Reply to that message using the /get_chat_id command in this bot.\n"
            "The bot will display the chat ID for you to use."
        )
    elif message.text == 'Back':
        show_main_menu(message)


def get_chatgpt_response(message):
    """Processes the user's message and sends it to ChatGPT, returning the response"""
    user_message = message.text
    try:
        response = openai.Completion.create(
            engine='text-davinci-003',
            prompt=user_message,
            max_tokens=50,
            temperature=0.7
        )
        bot.send_message(message.chat.id, response.choices[0].text.strip())
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred while communicating with ChatGPT: {str(e)}")


@bot.message_handler(commands=['send_photo'])
def send_photo_command(message):
    """
    Command to send a photo to the specified chat.
    Usage: Reply to a photo and enter the command /send_photo <chat_id>.
    """
    if message.reply_to_message and message.reply_to_message.photo:
        try:
            chat_id = int(message.text.split()[1])
            file_id = message.reply_to_message.photo[-1].file_id
            bot.send_photo(chat_id, file_id)
            bot.send_message(message.chat.id, f'The photo was successfully sent to chat {chat_id}.')
        except (IndexError, ValueError):
            bot.send_message(message.chat.id, 'Please specify a valid chat ID after the command.')
    else:
        bot.send_message(message.chat.id, 'Please use this command in response to a photo.')


@bot.message_handler(commands=['send_text'])
def send_text_command(message):
    """
    Command to send a text message to the specified chat.
    Usage: /send_text <chat_id> <message>.
    """
    try:
        command_parts = message.text.split(maxsplit=2)
        chat_id = int(command_parts[1])
        text_message = command_parts[2]
        bot.send_message(chat_id, text_message)
        bot.send_message(message.chat.id, f'The message was sent to chat {chat_id}.')
    except IndexError:
        bot.send_message(message.chat.id, 'Please specify the chat ID and the message text after the command.')
    except ValueError:
        bot.send_message(message.chat.id, 'Please provide a valid chat ID.')


@bot.message_handler(content_types=['photo'])
def photo(message):
    """Provides a hint to the user to send a photo with the chat ID using /send_photo"""
    bot.send_message(message.chat.id,
                     'To send a photo to another chat, reply to the photo with the command /send_photo <chat_id>.')

    # Show the "Find Chat ID" and "Back" buttons after sending the above message
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    find_chat_id_button = types.KeyboardButton('Find Chat ID')
    back_button = types.KeyboardButton('Back')
    markup.add(find_chat_id_button, back_button)
    bot.send_message(message.chat.id, 'If you need help finding the chat ID, click the button below:',
                     reply_markup=markup)


bot.infinity_polling()

#How are you? It is can be work