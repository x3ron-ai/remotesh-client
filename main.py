from app import app, get_data, registration
import requests
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
def open_browser(icon, item):
    webbrowser.open('http://127.0.0.1:6124')

# Функция для выхода из приложения
def quit_app(icon, item):
    icon.stop()

# Функция для создания иконки в трее
def setup_tray():
    if not os.path.exists('icon.png'):
        r = requests.get('https://shh.stariybog.ru/static/images/icon.png')
        with open('icon.png', 'wb') as f:
            f.write(r.content)
    image = Image.open("icon.png")

    # Создаем меню для иконки
    menu = (
        item('Открыть', open_browser),
        item('Выход', quit_app)
    )

    # Создаем иконку в трее
    icon = pystray.Icon("RemoteSH", image, "RemoteSH", menu=pystray.Menu(*menu))

    # Запускаем иконку
    icon.run()

if __name__ == "__main__":
    # Проверяем, существует ли файл config.json
    if not os.path.exists('config.json'):
        registration()
        open_browser('?', '?')

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
