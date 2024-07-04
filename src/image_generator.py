import openai
import requests
import os
from dotenv import load_dotenv

class ImageGenerator:
    def __init__(self):
        # Загрузка переменных окружения из файла .env
        load_dotenv()
        # Получение ключа API из переменной окружения
        self.api_key = os.getenv('OPENAI_API_KEY')
        openai.api_key = self.api_key

    def generate_image(self, prompt, output_dir='../image', output_filename='dalle3_generated_image.png'):
        response = openai.Image.create(
            prompt=prompt,
            n=1,  # Количество изображений
            size="1024x1024",  # Размер изображения
            model="dall-e-3"  # Указание модели DALL-E 3
        )

        # Получите URL сгенерированного изображения
        image_url = response['data'][0]['url']
        print(f"Ссылка на изображение: {image_url}")

        # Создайте папку для сохранения изображения, если она не существует
        os.makedirs(output_dir, exist_ok=True)

        # Сохраните изображение локально
        image_path = os.path.join(output_dir, output_filename)
        img_data = requests.get(image_url).content
        with open(image_path, 'wb') as handler:
            handler.write(img_data)

        print(f"Изображение сохранено по пути: {image_path}")
