import tkinter as tk
from PIL import Image, ImageTk
import sqlite3
import subprocess
import platform
import os
from tkinter import simpledialog  # Импортируем simpledialog напрямую

def set_background(window, image_path):
    """Устанавливает JPG изображение в качестве фона окна Tkinter."""
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


def register_user(users_data_file, output_widget):
    """Регистрирует пользователя и выводит сообщения в виджет."""
    while True:
        surname = simpledialog.askstring("Регистрация", "Введите фамилию:")  # Использовали simpledialog.askstring
        if not surname: return None, None, None  # Allow cancel
        name = simpledialog.askstring("Регистрация", "Введите имя:")  # Использовали simpledialog.askstring
        if not name: return None, None, None

        while True:
            username = simpledialog.askstring("Регистрация", "Введите имя пользователя (логин, от 3 до 16 символов):")  # Использовали simpledialog.askstring
            if not username: return None, None, None
            if 3 <= len(username) <= 16:
                break
            else:
                output_widget.insert(tk.END, "Имя пользователя должно содержать от 3 до 16 символов. Попробуйте снова.\n")
                output_widget.see(tk.END)  # Auto-scroll

        while True:
            password = simpledialog.askstring("Регистрация", "Введите пароль (от 8 до 16 символов):", show="*")  # Использовали simpledialog.askstring
            if not password: return None, None, None
            if 8 <= len(password) <= 16:
                break
            else:
                output_widget.insert(tk.END, "Пароль должен содержать от 8 до 16 символов. Попробуйте снова.\n")
                output_widget.see(tk.END)

        confirm_password = simpledialog.askstring("Регистрация", "Подтвердите пароль:", show="*")  # Использовали simpledialog.askstring
        if not confirm_password: return None, None, None

        if password != confirm_password:
            output_widget.insert(tk.END, "Пароли не совпадают. Попробуйте снова.\n")
            output_widget.see(tk.END)
            continue

        try:
            with open(users_data_file, 'r') as f:
                for line in f:
                    stored_username, _, _, _ = line.strip().split(':')
                    if stored_username == username:
                        output_widget.insert(tk.END, "Имя пользователя уже занято. Попробуйте другое.\n")
                        output_widget.see(tk.END)
                        break
                else:
                    with open(users_data_file, 'a') as f:
                        f.write(f"{username}:{surname}:{name}:{password}\n")
                    output_widget.insert(tk.END, "Регистрация прошла успешно!\n")
                    output_widget.see(tk.END)
                    return username, surname, name
        except FileNotFoundError:
            with open(users_data_file, 'w') as f:
                f.write(f"{username}:{surname}:{name}:{password}\n")
            output_widget.insert(tk.END, "Регистрация прошла успешно!\n")
            output_widget.see(tk.END)
            return username, surname, name


def login_user(users_data_file, output_widget):
    username = simpledialog.askstring("Вход", "Введите имя пользователя (логин):") # Использовали simpledialog.askstring
    if not username: return None, None, None #Allow cancel

    password = simpledialog.askstring("Вход", "Введите пароль:", show="*") # Использовали simpledialog.askstring
    if not password: return None, None, None

    try:
        with open(users_data_file, 'r') as f:
            for line in f:
                stored_username, surname, name, stored_password = line.strip().split(':')
                if stored_username == username and stored_password == password:
                    output_widget.insert(tk.END, f"Вход выполнен успешно! Добро пожаловать, {name} {surname}!\n")
                    output_widget.insert(tk.END, "Теперь вы сможете ознакомится с библиотекой\n")
                    output_widget.see(tk.END)
                    return stored_username, surname, name
        output_widget.insert(tk.END, "Неверное имя пользователя или пароль.\n")
        output_widget.see(tk.END)
        return None, None, None
    except FileNotFoundError:
        output_widget.insert(tk.END, "Ошибка: Файл с данными пользователей не найден.\n")
        output_widget.see(tk.END)
        return None, None, None

def create_button(parent, text, command, row, column, padx=5, pady=5, sticky=tk.W+tk.E):
    """Helper function to create buttons with consistent styling."""
    btn = tk.Button(parent, text=text, command=command)
    btn.grid(row=row, column=column, padx=padx, pady=pady, sticky=sticky)
    return btn


class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("LibFeath")
        self.root.geometry("960x540")

        self.users_data_file = "users.txt"
        self.logged_in_username = None
        self.logged_in_surname = None
        self.logged_in_name = None

        # Set background image
        self.background = set_background(self.root, 'fon.jpg')

        # Output Widget (Text area)
        self.output_widget = tk.Text(self.root, wrap=tk.WORD, state="normal")
        self.output_widget.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.6)  # Adjusted

        # Scrollbar for the Text widget
        scrollbar = tk.Scrollbar(self.root, command=self.output_widget.yview)
        scrollbar.place(relx=0.9, rely=0.1, relheight=0.6)
        self.output_widget['yscrollcommand'] = scrollbar.set


        # Initial text
        self.output_widget.insert(tk.END, "Добро пожаловать в библиотеку LitFeath\n")
        self.output_widget.insert(tk.END, "Версия библиотеки 0.31\n")
        self.output_widget.insert(tk.END, "Здесь вы сможете ознакомится с нашим асортиментом книг\n")
        self.output_widget.insert(tk.END, "Для просмотра книг зарегестрируйтесь или войдите в учётную запись\n")
        self.output_widget.config(state="disabled")  # Make it read-only

        # Buttons Frame
        self.buttons_frame = tk.Frame(self.root)
        self.buttons_frame.place(relx=0.1, rely=0.75, relwidth=0.8, relheight=0.2)

        # Initial Buttons
        self.reg_button = create_button(self.buttons_frame, "Регистрация", self.register, 0, 0)
        self.login_button = create_button(self.buttons_frame, "Вход", self.login, 0, 1)
        self.exit_button = create_button(self.buttons_frame, "Выход", self.exit_app, 0, 2)
        self.library_button = None   #Will be created after login
        self.logout_button = None

        self.booklist_button = None

        #Grid configuration
        for i in range(3):
            self.buttons_frame.columnconfigure(i, weight=1) #Equal button width


    def register(self):
        """Handles user registration."""
        self.output_widget.config(state="normal") #Enable editing
        self.logged_in_username, self.logged_in_surname, self.logged_in_name = register_user(self.users_data_file, self.output_widget)
        if self.logged_in_username:
            self.output_widget.insert(tk.END, f"Регистрация и вход выполнены успешно! Добро пожаловать, {self.logged_in_name} {self.logged_in_surname}!\n")
            self.output_widget.insert(tk.END, "Теперь вы сможете ознакомиться с библиотекой\n")
            self.show_library_buttons()  #Show library options
        self.output_widget.config(state="disabled")  #Disable editing

    def login(self):
        """Handles user login."""
        self.output_widget.config(state="normal") #Enable editing
        self.logged_in_username, self.logged_in_surname, self.logged_in_name = login_user(self.users_data_file, self.output_widget)
        if self.logged_in_username:
            self.show_library_buttons()
        self.output_widget.config(state="disabled")

    def exit_app(self):
        """Exits the application."""
        self.root.destroy()

    def logout(self):
        """Logs out the current user."""
        self.output_widget.config(state="normal")
        self.output_widget.insert(tk.END, f"Вы вышли из учетной записи {self.logged_in_name} {self.logged_in_surname}.\n")
        self.output_widget.see(tk.END)
        self.logged_in_username = None
        self.logged_in_surname = None
        self.logged_in_name = None

        #Restore initial buttons
        self.reg_button.grid(row=0, column=0)
        self.login_button.grid(row=0, column=1)
        self.exit_button.grid(row=0, column=2)

        if self.library_button:
            self.library_button.destroy()
            self.library_button = None
        if self.logout_button:
            self.logout_button.destroy()
            self.logout_button = None

        self.output_widget.config(state="disabled")


    def show_library_buttons(self):
        """Shows the library-related buttons and hides registration/login."""

        #Hide initial buttons
        self.reg_button.grid_forget()
        self.login_button.grid_forget()
        self.exit_button.grid_forget()

        #Create Library and Logout buttons
        self.library_button = create_button(self.buttons_frame, "Библиотека", self.open_library, 0, 0)
        self.logout_button = create_button(self.buttons_frame, "Выход из учетной записи", self.logout, 0, 1)
        self.exit_button = create_button(self.buttons_frame, "Выход", self.exit_app, 0, 2) #Reuse the exit

    def open_library(self):
        """Opens the library functionality."""
        self.output_widget.config(state="normal")
        self.output_widget.insert(tk.END, "\nЗдесь вы сможете ознакомится с функционалом:\n")
        self.output_widget.insert(tk.END, "Весь список книг - blt\n")
        self.output_widget.insert(tk.END, "Читать книгу - rbk\n")
        self.output_widget.insert(tk.END, "Назад - bck\n")
        self.output_widget.see(tk.END) #Autoscroll

        self.booklist_button = create_button(self.buttons_frame, "Весь список книг", self.show_booklist, 1, 0)
        self.readbook_button = create_button(self.buttons_frame, "Читать книгу", self.open_book, 1, 1)
        self.back_button = create_button(self.buttons_frame, "Назад", self.show_library_buttons, 1, 2)  #Go back to library main menu

        self.output_widget.config(state="disabled")

    def show_booklist(self):
        """Displays the book list in the output widget."""
        self.output_widget.config(state="normal")
        self.output_widget.insert(tk.END, "\nПолный каталог литературы:\n")
        self.output_widget.see(tk.END)

        conn = sqlite3.connect("your_database.db")  #Replace with your actual db file
        cursor = conn.cursor()

        try:
            cursor.execute('SELECT * FROM Books') #Replace "Books" if your table has another name
            books = cursor.fetchall()

            for book in books:
                self.output_widget.insert(tk.END, str(book) + "\n") #Show each book in output
                self.output_widget.see(tk.END)

        except sqlite3.Error as e:
            self.output_widget.insert(tk.END, f"Database Error: {e}\n")
            self.output_widget.see(tk.END)

        finally:
            conn.close()

        self.output_widget.config(state="disabled")


    def get_files_in_directory(self, directory_path):
        files = []
        try:
            for filename in os.listdir(directory_path):
                if filename.endswith(".txt"):
                    files.append(filename)
        except FileNotFoundError:
            self.output_widget.config(state="normal")
            self.output_widget.insert(tk.END, f"Ошибка: Директория '{directory_path}' не найдена.\n")
            self.output_widget.see(tk.END)
            self.output_widget.config(state="disabled")
            return None
        return files

    def open_file(self, file_name):
        try:
            if platform.system() == "Windows":
                subprocess.Popen(["notepad.exe", file_name])
            elif platform.system() == "Darwin":
                subprocess.Popen(["open", file_name])
            else:
                subprocess.Popen(["xdg-open", file_name])
        except FileNotFoundError:
            self.output_widget.config(state="normal")
            self.output_widget.insert(tk.END, f"Ошибка: Файл '{file_name}' не найден.\n")
            self.output_widget.see(tk.END)
            self.output_widget.config(state="disabled")
        except Exception as e:
            self.output_widget.config(state="normal")
            self.output_widget.insert(tk.END, f"Произошла ошибка: {e}\n")
            self.output_widget.see(tk.END)
            self.output_widget.config(state="disabled")

    def open_book(self):
        base_path = os.path.join(os.path.expanduser("~"), "Desktop", "LibFeath", "library")
        books_path = os.path.join(base_path, "books")

        files = self.get_files_in_directory(books_path)

        if files is None or not files:
            self.output_widget.config(state="normal")
            self.output_widget.insert(tk.END, "В директории 'books' нет текстовых файлов.\n")
            self.output_widget.see(tk.END)
            self.output_widget.config(state="disabled")
            return

        self.output_widget.config(state="normal")
        self.output_widget.insert(tk.END, "Доступные файлы:\n")
        for i, filename in enumerate(files):
            self.output_widget.insert(tk.END, f"{i+1}. {filename}\n")

        self.output_widget.see(tk.END)
        self.output_widget.config(state="disabled")


        def open_selected_book():
            choice = simpledialog.askstring("Открыть книгу", "Введите номер файла для открытия (или bck - назад):") #Использовали simpledialog.askstring
            if choice == "bck":
                return

            try:
                choice = int(choice)
                if 1 <= choice <= len(files):
                    selected_file = os.path.join(books_path, files[choice-1])
                    self.open_file(selected_file)
                    self.output_widget.config(state="normal")
                    self.output_widget.insert(tk.END, "Вы открыли книгу\n")
                    self.output_widget.see(tk.END)
                    self.output_widget.config(state="disabled")

                else:
                    self.output_widget.config(state="normal")
                    self.output_widget.insert(tk.END, "Неверный номер файла. Попробуйте еще раз.\n")
                    self.output_widget.see(tk.END)
                    self.output_widget.config(state="disabled")

            except ValueError:
                self.output_widget.config(state="normal")
                self.output_widget.insert(tk.END, "Пожалуйста, введите число или 'bck' для выхода.\n")
                self.output_widget.see(tk.END)
                self.output_widget.config(state="disabled")

        open_selected_book()


if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()
    
