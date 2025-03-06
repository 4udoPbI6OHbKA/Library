import tkinter as tk
from PIL import Image, ImageTk

class AnimatedBackground:
    def __init__(self, master, image_path, speed=1):
       
        self.master = master
        self.image_path = image_path
        self.speed = speed
        self.x_offset = 0  # Смещение по горизонтали
        self.y_offset = 0  # Смещение по вертикали

        try:
            self.image = Image.open(self.image_path)
            self.background_image = ImageTk.PhotoImage(self.image)

            self.background_label = tk.Label(master, image=self.background_image)
            self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
            self.background_label.image = self.background_image  # Сохраняем ссылку

        except FileNotFoundError:
            print(f"Ошибка: Файл не найден: {image_path}")
            self.background_label = None
            return

        self.animate_background()

    def animate_background(self):
       
        if self.background_label is None:
            return # Нечего анимировать, если фон не загружен

        self.x_offset += self.speed
        self.y_offset += self.speed  # Можно анимировать и по вертикали

        # Зацикливаем смещение (чтобы не выходить за пределы изображения)
        self.x_offset %= self.image.width
        self.y_offset %= self.image.height

        # Создаем обрезанное изображение для отображения
        cropped_image = self.image.crop((self.x_offset, self.y_offset,
                                          self.master.winfo_width() + self.x_offset,
                                          self.master.winfo_height() + self.y_offset))
        self.animated_image = ImageTk.PhotoImage(cropped_image)
        self.background_label.config(image=self.animated_image)
        self.background_label.image = self.animated_image  # Сохраняем ссылку!


        self.master.after(20, self.animate_background)  # Запускаем анимацию снова через 20 мс


# Пример использования
root = tk.Tk()
root.title("Подвижный фон")
root.geometry("800x600")

# Создаем анимированный фон
animated_bg = AnimatedBackground(root, "fon.jpg", speed=1)  # speed - скорость анимации

# Добавляем виджеты (пример)
label = tk.Label(root, text="Текст поверх фона", bg="white")
label.pack(pady=20)

root.mainloop()

if __name__ == "__main__":
    создать_окно_с_фоном_и_кнопкой()
