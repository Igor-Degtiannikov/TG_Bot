import telebot
from telebot import types # импорт модуля types из библеотки telebot
import openai
import config
from dotenv import load_dotenv
import os
import json

load_dotenv()

bot = telebot.TeleBot(config.TELEGRAM_API_KEY)
openai.api_key = config.CHAT_API_KEY

def load_users():
    try:
        with open('users.join', 'r') as file: # Открывает файл в режиме "r" - чтения
            return json.load(file) # Если он сущетсвует, функция сгружает из него данные = словарь с данными о пользователях
    except FileNotFoundError: # Если файл не найден, срабатывает исключение
        return {} # Возвращает пустой словарь

def save_users(users):
    with open('users.json', 'w') as file: # Открывает файл в режиме "w" - записи
        json.dump(users, file) # Зарписывает в файл обновленный словарь
@bot.message_handler(commands=['start'])
def start_message(message):
    users = load_users() # Загружает список пользователей из файла.(Если он не существует, то файл пустой)
    user_id = str(message.chat.id)

    if user_id not in users: # Если пользователя нет в users = значит он впервые пришел,м и ему отправляется приветсвенное сообщение
        bot.send_message(message.chat.id, 'Hello! I am new bot, which can use ChatGPT.')
        users[user_id] = True # Добовляем пользователя в список
        save_users(users) # Сохраняем
    else:
        bot.send_message(message.chat.id, "Welcome back! Here's what I can do for you: ")

    show_main_menu(message)

def show_main_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Using ChatGPT')
    item2 = types.KeyboardButton('Help')
    markup.add(item1, item2)
    bot.send_message(message.chat.id,'Pick what you want', reply_markup=markup)

@bot.message_handler(content_types='text')
def message_replay(message):
    if message.text == 'Using ChatGPT':
        bot.send_message(message.chat.id,'Write the message:')
        bot.register_next_step_handler(message, get_chatgpt_response)

    elif message.text == 'Help':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        instruction_button = types.KeyboardButton('Instruction')
        about_button = types.KeyboardButton('What is ChatGPT')
        back_button = types.KeyboardButton('Back')
        markup.add(instruction_button,about_button,back_button)
        bot.send_message(message.chat.id,'Here are some options to help you:', reply_markup=markup)

    elif message.text == 'Instruction':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        back_button = types.KeyboardButton('Back')
        markup.add(back_button)
        bot.send_message(message.chat.id,'Select “Using ChatGPT”, then post your question, and wait for a response.')

    elif message.text == 'What is ChatGPT':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        back_button = types.KeyboardButton('Back')
        markup.add(back_button)
        bot.send_message(message.chat.id,'ChatGPT is an advanced AI language model developed by OpenAI')

    elif message.text == 'Back':
        show_main_menu(message)

def get_chatgpt_response(message): # Функция предназначена для обработки текста сообщения пользователя и взаимодействия с ChatGPT.
    user_message = message.text #  Извлекает текст из сообщения пользователя, сохраняет его в переменную user_message
    try: #Начинает блок try, который используется для обработки ошибок
        response = openai.Completion.create( #Отправляет запрос к ChatGPT через OpenAI API с параметрами
            engine='text-davinci-003', #модель ChatGPT, которая будет использоваться для генерации ответа
            prompt=user_message, #Передает текст пользователя в качестве запроса к модели.
            max_tokens=50, #Указывает максимальное количество токенов (слов или частей слов)
            temperature=0.7 #Определяет степень случайности в ответах модели
        )

        bot.send_message(message.chat.id,response.choices[0].text.strip()) # Текст ответа от ChatGPT, который отправляется пользователю.
    except Exception as e: # Начинает блок обработки ошибок, который выполняется, если в блоке try произошла ошибка,
        bot.send_message(message.chat.id, f"Произошла ошибка при общении с ChatGPT: {str(e)}") # str(e): Преобразует объект ошибки в строку, чтобы можно было понять, что пошло не так

bot.infinity_polling()