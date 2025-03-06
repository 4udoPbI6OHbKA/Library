import tkinter as tk
from PIL import Image, ImageTk

def set_background(window, image_path):


    try:
        image = Image.open(image_path)
        background_image = ImageTk.PhotoImage(image)

        # Создание Label для отображения изображения
        background_label = tk.Label(window, image=background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)  # Заполнение всего окна
        background_label.image = background_image  # Важно!  Сохраняем ссылку, иначе будет garbage collected
        return background_label
    except FileNotFoundError:
        print(f"Ошибка: Файл не найден по пути: {image_path}")
        return None  # Или обработайте ошибку как-то иначе

def create_transparent_button(parent, image_path, text, command):

    try:
        image = Image.open(image_path)
        button_image = ImageTk.PhotoImage(image)

        # Создаем Label, который выглядит как кнопка
        button_label = tk.Label(
            parent,
            image=button_image,
            text=text,
            compound="center",  # Размещаем текст поверх изображения
            relief="raised",    # Или "sunken" для эффекта нажатия
            borderwidth=0,      # Убираем рамку
            cursor="hand2"       # Изменяем курсор при наведении
        )
        button_label.image = button_image  # Сохраняем ссылку!

        # Привязываем клик к Label для имитации нажатия кнопки
        button_label.bind("<Button-1>", lambda event: command())

        return button_label

    except FileNotFoundError:
        print(f"Ошибка: Файл не найден по пути: {image_path}")
        return None

# Пример использования
root = tk.Tk()
root.title("LibFeath")
root.geometry("800x600")

# Устанавливаем фон для окна
background = set_background(root, 'fon.jpg')

if background:
    # Добавляем виджеты поверх фона
    label = tk.Label(root, text="Добро пожаловать в библиотеку LitFeath", bg="white")
    label.pack(pady=20)

    # Создаем "кнопку" с прозрачным фоном
    def button_click():
        print("Кнопка нажата!")

    transparent_button = create_transparent_button(
        root,
        "fon.jpg",  # Путь к изображению для кнопки
        "Нажми меня",              # Текст на кнопке
        button_click               # Функция, которая будет вызвана при нажатии
    )
    if transparent_button:
        transparent_button.pack(pady=10)

root.mainloop()
