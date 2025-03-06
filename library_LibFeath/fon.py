import tkinter as tk
from PIL import Image, ImageTk

def set_background(window, image_path):


    try:
        image = Image.open(image_path)
        background_image = ImageTk.PhotoImage(image)

        
        background_label = tk.Label(window, image=background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)  
        background_label.image = background_image  
        return background_label
    
    except FileNotFoundError:
        print(f"Ошибка: Файл не найден по пути: {image_path}")
        return None  


root = tk.Tk()
root.title("LibFeath")
root.geometry("960x540")  


background = set_background(root, 'fon.jpg')

if background:
    
    label = tk.Label(root, text="Привет, мир!", bg="white")  
    label.pack(pady=20)

    button = tk.Button(root, text="Нажми меня", command=lambda: print("Не работает(((((("))
    button.pack(pady=10)

root.mainloop()
