import os # Импорт модуля os, предоставляет функции для взаимодействия с оперецаионной системой, для работы с переменным окружение, в данном случает из .env
from dotenv import load_dotenv # Импорт функции load_dotenv из библеотеки python-dotenv. Это необходимо, чтобы os.getenv() мог видеть и использовать значения из .env.

load_dotenv() # Вызов функцию, которая ищет файл .env в указанных путях и загруает их как переменное окружение

TELEGRAM_API_KEY = os.getenv('TELEGRAM_API_KEY') # os.getenv получает значение переменное окружения с именем, Сохраняет значение ключа в переменной
CHAT_API_KEY = os.getenv('CHAT_API_KEY')

if not TELEGRAM_API_KEY or not CHAT_API_KEY:
    raise ValueError('Ошибка! Нет ключей!!')