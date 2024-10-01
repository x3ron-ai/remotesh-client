from app import app, get_data, registration
from threading import Thread
from parser import main_parser
import os
import webbrowser
import pystray
from pystray import MenuItem as item
from PIL import Image

# Функция для запуска сервера
def run_server():
    app.run('0.0.0.0', 6124)

# Функция для открытия браузера
def open_browser(icon, item=None):
    webbrowser.open('http://127.0.0.1:6124')

# Функция для выхода из приложения
def quit_app(icon, item):
    icon.stop()

# Обработка событий клика
def on_clicked(icon, button, clicked):
    if button == 1:  # Левая кнопка мыши
        open_browser(icon)

# Функция для создания иконки в трее
def setup_tray():
    # Загрузите иконку для трея (иконка должна быть в формате PNG)
    image = Image.open("icon.png")  # Замените на путь к вашей иконке

    # Создаем меню для иконки
    menu = (
        item('Открыть', open_browser),
        item('Выход', quit_app)
    )

    # Создаем иконку в трее
    icon = pystray.Icon("my_app", image, "Моя программа", menu=pystray.Menu(*menu))

    # Устанавливаем функцию, которая будет вызываться при клике
    icon.visible = True
    icon.run(setup=lambda: icon.notify("Программа запущена"), on_click=on_clicked)

if __name__ == "__main__":
    # Проверяем, существует ли файл config.json
    if not os.path.exists('config.json'):
        registration()

    # Запускаем парсер в отдельном потоке
    parser_thread = Thread(target=main_parser, args=(get_data(),))
    parser_thread.setDaemon(True)
    parser_thread.start()

    # Запускаем сервер в отдельном потоке
    server_thread = Thread(target=run_server)
    server_thread.setDaemon(True)
    server_thread.start()

    # Запускаем иконку в трее
    setup_tray()
