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
        return background_label #Возвращаем label, чтобы можно было потом его изменить или удалить
    except FileNotFoundError:
        print(f"Ошибка: Файл не найден по пути: {image_path}")
        return None  # Или обработайте ошибку как-то иначе


def set_button_background(button, image_path):
    width = 100
    height = 100
    
    try:
        image = Image.open(image_path)
        button_image = ImageTk.PhotoImage(image)
        button.config(image=button_image, compound=tk.CENTER)  # compound=tk.CENTER нужно, чтобы текст был поверх изображения
        button.image = button_image  # Сохраняем ссылку!
    except FileNotFoundError:
        print(f"Ошибка: Файл не найден по пути: {image_path}")

# Пример использования
root = tk.Tk()
root.title("LibFeath")
root.geometry("1200x900")  # Установите размер окна

# Замените 'fon.jpg' на фактический путь к вашему файлу
background = set_background(root, 'fon.jpg')

if background:  # Убедимся, что фон был успешно установлен
    # Добавляем виджеты поверх фона (пример)
    label = tk.Label(root, text="Добро пожаловать в библиотеку LibFeath", bg="white")  # Сделаем фон текста белым для видимости
    label.pack(pady=20)

    # Создаем кнопку с фоном
    button = tk.Button(root, text="Кнопка с фоном")
    set_button_background(button, "fon2.png") # Замените на путь к вашему изображению для кнопки
    button.pack(pady=10)

root.mainloop()
