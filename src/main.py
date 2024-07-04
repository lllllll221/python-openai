from chat_bot import ChatBot
from image_generator import ImageGenerator

def main():
    while True:
        print("Выберите режим:")
        print("1: Генерация изображения")
        print("2: Чат с AI")
        print("3: Выйти")

        choice = input("Ваш выбор: ").strip().lower()
        if choice == 'exit':
            print("Выход.")
            break

        if choice == '1':
            prompt = input("Введите описание изображения: ").strip()
            if prompt.lower() == 'exit':
                print("Выход.")
                break
            generator = ImageGenerator()
            generator.generate_image(prompt)
        elif choice == '2':
            bot = ChatBot()
            histories = bot.list_histories()
            if histories:
                print("Доступные диалоги:")
                for i, history in enumerate(histories):
                    print(f"{i+1}: {history}")
                history_choice = input("Выберите диалог для продолжения или введите 'new' для нового диалога: ").strip().lower()
                if history_choice == 'exit':
                    print("Выход.")
                    break
                if history_choice == 'new':
                    bot.start_new_history()
                else:
                    bot.load_history(histories[int(history_choice)-1])
            else:
                print("Нет доступных диалогов, начат новый диалог.")
                bot.start_new_history()
            bot.chat()
        elif choice == '3':
            print("Выход.")
            break
        else:
            print("Неверный выбор, попробуйте снова.")

if __name__ == "__main__":
    main()
