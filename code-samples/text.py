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

    def load_latest_history(self):
        # Загрузка последней истории диалога из файлов в директории
        histories = sorted([f for f in os.listdir(self.history_dir) if f.endswith('.json')], reverse=True)
        if histories:
            self.current_history_file = os.path.join(self.history_dir, histories[0])
            with open(self.current_history_file, 'r') as file:
                self.conversation_history = json.load(file)
        else:
            self.start_new_history()

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
        self.load_latest_history()
        print("Начните диалог с AI (введите 'exit' для завершения или 'new' для начала нового диалога):")
        while True:
            user_input = input("Вы: ")
            if user_input.lower() == 'exit':
                print("Диалог завершен.")
                break
            elif user_input.lower() == 'new':
                self.start_new_history()
                print("Начат новый диалог.")
            else:
                response = self.generate_response(user_input)
                print(f"AI: {response}")

# Запуск интерактивного общения
if __name__ == "__main__":
    chatbot = ChatBot()
    chatbot.chat()