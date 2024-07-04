import openai
import os
from dotenv import load_dotenv

# Загрузка переменных окружения из файла .env
load_dotenv()
# Получение ключа API из переменной окружения
openai.api_key = os.getenv('OPENAI_API_KEY')

try:
    # Запрос списка моделей
    models = openai.Model.list()

    # Вывод списка моделей
    for model in models['data']:
        print(model['id'])
except openai.error.AuthenticationError as e:
    print("Ошибка аутентификации:", e)
except Exception as e:
    print("Произошла ошибка:", e)
