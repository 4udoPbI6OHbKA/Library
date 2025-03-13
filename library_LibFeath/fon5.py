import tkinter as tk
from PIL import Image, ImageTk

def set_background(window, image_path):
    """
    Устанавливает фоновое изображение, которое растягивается под размер окна.

    Args:
        window: Объект Tkinter окна.
        image_path: Путь к файлу изображения.

    Returns:
        tk.Label: Объект метки с фоновым изображением (или None в случае ошибки).
    """
    try:
        image = Image.open(image_path)
        # Сохраняем исходный размер изображения для обработки изменения размера окна
        window._original_image_size = image.size  
        window.background_image = ImageTk.PhotoImage(image) # Сохраняем изображение в атрибут окна, чтобы избежать GC

        background_label = tk.Label(window, image=window.background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        # background_label.image = background_image  # Не нужно, т.к. image хранится в window

        return background_label

    except FileNotFoundError:
        print(f"Ошибка: Файл не найден по пути: {image_path}")
        return None


def on_resize(event):
    """
    Обработчик события изменения размера окна.  Перемасштабирует фоновое изображение.
    """
    if hasattr(root, 'background_image') and hasattr(root, '_original_image_size'): # Проверяем, что фон был установлен
        try:
            # Получаем новые размеры окна
            width = root.winfo_width()
            height = root.winfo_height()

            # Масштабируем изображение
            image = Image.open('fon.jpg') # Переоткрываем изображение, т.к.  PIL не позволяет просто перемасштабировать ImageTk.PhotoImage
            resized_image = image.resize((width, height), Image.Resampling.LANCZOS) # Используем LANCZOS для лучшего качества
            root.background_image = ImageTk.PhotoImage(resized_image)

            # Обновляем изображение метки
            background.config(image=root.background_image)
            background.image = root.background_image  # Важно для сохранения ссылки на изображение
        except Exception as e:
            print(f"Ошибка при изменении размера: {e}")



root = tk.Tk()
root.title("LibFeath")
root.geometry("960x540")  # Начальный размер окна


background = set_background(root, 'fon.jpg')

if background:
    label = tk.Label(root, text="Привет, мир!", bg="white")
    label.pack(pady=20)

    button = tk.Button(root, text="Нажми меня", command=lambda: print("Не работает(((((("))
    button.pack(pady=10)

    # Привязываем обработчик изменения размера окна
    root.bind("<Configure>", on_resize)


root.mainloop()
