import openai
import os
import json
from dotenv import load_dotenv
from datetime import datetime

class ChatBot:
    def __init__(self):
        # Загрузка переменных окружения из файла .env
        load_dotenv()
        # Получение ключа API из переменной окружения
        openai.api_key = os.getenv('OPENAI_API_KEY')
        self.history_dir = '../history'
        os.makedirs(self.history_dir, exist_ok=True)
        self.current_history_file = None
        self.conversation_history = []

    def list_histories(self):
        # Получение списка файлов с историей диалогов
        return sorted([f for f in os.listdir(self.history_dir) if f.endswith('.json')])

    def load_history(self, filename):
        # Загрузка истории диалога из указанного файла
        self.current_history_file = os.path.join(self.history_dir, filename)
        with open(self.current_history_file, 'r') as file:
            self.conversation_history = json.load(file)

    def start_new_history(self):
        # Создание нового файла для истории диалога
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.current_history_file = os.path.join(self.history_dir, f'conversation_{timestamp}.json')
        self.conversation_history = []

    def save_history(self):
        # Сохранение истории диалога в файл
        if self.current_history_file:
            with open(self.current_history_file, 'w') as file:
                json.dump(self.conversation_history, file)

    def generate_response(self, user_input):
        # Добавляем пользовательский ввод в историю диалога
        self.conversation_history.append({"role": "user", "content": user_input})
        
        # Запрос к модели gpt-4o-2024-05-13 через endpoint /v1/chat/completions
        response = openai.ChatCompletion.create(
            model="gpt-4o-2024-05-13",
            messages=self.conversation_history,
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.9,
        )
        
        # Получаем ответ от модели
        ai_response = response.choices[0].message['content']
        
        # Добавляем ответ модели в историю диалога
        self.conversation_history.append({"role": "assistant", "content": ai_response})
        
        # Сохраняем историю диалога
        self.save_history()
        
        return ai_response

    def chat(self):
        print("Начните диалог с AI (введите 'exit' для завершения)O:")
        while True:
            user_input = input("Вы: ").strip().lower()
            if user_input == 'exit':
                print("Выход.")
                break
            else:
                response = self.generate_response(user_input)
                print(f"AI: {response}")
