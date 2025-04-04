import tkinter as tk
from PIL import Image, ImageTk
import sqlite3
import subprocess
import platform
import os
from tkinter import simpledialog

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


def register_user(users_data_file, output_widget, surname_entry, name_entry, username_entry, password_entry, confirm_password_entry, clear_callback):
    surname = surname_entry.get()
    name = name_entry.get()
    username = username_entry.get()
    password = password_entry.get()
    confirm_password = confirm_password_entry.get()

    if not all([surname, name, username, password, confirm_password]):
        output_widget.insert(tk.END, "Пожалуйста, заполните все поля.\n")
        output_widget.see(tk.END)
        return None, None, None

    if not (3 <= len(username) <= 16):
        output_widget.insert(tk.END, "Имя пользователя должно содержать от 3 до 16 символов. Попробуйте снова.\n")
        output_widget.see(tk.END)
        return None, None, None

    if not (8 <= len(password) <= 16):
        output_widget.insert(tk.END, "Пароль должен содержать от 8 до 16 символов. Попробуйте снова.\n")
        output_widget.see(tk.END)
        return None, None, None

    if password != confirm_password:
        output_widget.insert(tk.END, "Пароли не совпадают. Попробуйте снова.\n")
        output_widget.see(tk.END)
        return None, None, None

    try:
        with open(users_data_file, 'r') as f:
            for line in f:
                stored_username, _, _, _ = line.strip().split(':')
                if stored_username == username:
                    output_widget.insert(tk.END, "Имя пользователя уже занято. Попробуйте другое.\n")
                    output_widget.see(tk.END)
                    return None, None, None
            else:
                with open(users_data_file, 'a') as f:
                    f.write(f"{username}:{surname}:{name}:{password}\n")
                output_widget.insert(tk.END, "Регистрация прошла успешно!\n")
                output_widget.see(tk.END)
                clear_callback()
                return username, surname, name
    except FileNotFoundError:
        with open(users_data_file, 'w') as f:
            f.write(f"{username}:{surname}:{name}:{password}\n")
        output_widget.insert(tk.END, "Регистрация прошла успешно!\n")
        output_widget.see(tk.END)
        clear_callback()
        return username, surname, name


def login_user(users_data_file, output_widget, username_entry, password_entry, clear_callback):
    username = username_entry.get()
    password = password_entry.get()

    if not all([username, password]):
        output_widget.insert(tk.END, "Пожалуйста, заполните все поля.\n")
        output_widget.see(tk.END)
        return None, None, None

    try:
        with open(users_data_file, 'r') as f:
            for line in f:
                stored_username, surname, name, stored_password = line.strip().split(':')
                if stored_username == username and stored_password == password:
                    output_widget.insert(tk.END, f"Вход выполнен успешно! Добро пожаловать, {name} {surname}!\n")
                    output_widget.insert(tk.END, "Теперь вы сможете ознакомится с библиотекой\n")
                    output_widget.see(tk.END)
                    clear_callback()
                    return stored_username, surname, name
        output_widget.insert(tk.END, "Неверное имя пользователя или пароль.\n")
        output_widget.see(tk.END)
        return None, None, None
    except FileNotFoundError:
        output_widget.insert(tk.END, "Ошибка: Файл с данными пользователей не найден.\n")
        output_widget.see(tk.END)
        return None, None, None

def create_button(parent, text, command, row, column, padx=5, pady=5, sticky=tk.W+tk.E):
    btn = tk.Button(parent, text=text, command=command)
    btn.grid(row=row, column=column, padx=padx, pady=pady, sticky=sticky)
    return btn


class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("LibFeath")
        self.root.geometry("1200x960")
        self.root.resizable(False, False)
        icon = tk.PhotoImage(file = "favicon.png")
        self.root.iconphoto(False, icon)
        

        self.users_data_file = "users.txt"
        self.logged_in_username = None
        self.logged_in_surname = None
        self.logged_in_name = None

        self.background = set_background(self.root, 'fon.jpg')

        self.output_widget = tk.Text(self.root, wrap=tk.WORD, state="normal")
        self.output_widget.place(relx=0.3, rely=0.25, relwidth=0.4, relheight=0.29)

        scrollbar = tk.Scrollbar(self.root, command=self.output_widget.yview)
        scrollbar.place(relx=0.7, rely=0.25, relheight=0.27)
        self.output_widget['yscrollcommand'] = scrollbar.set

        self.output_widget.insert(tk.END, "Добро пожаловать в библиотеку LitFeath\n")
        self.output_widget.insert(tk.END, "Версия библиотеки 0.5\n")
        self.output_widget.insert(tk.END, "Здесь вы сможете ознакомится с нашим асортиментом книг\n")
        self.output_widget.insert(tk.END, "Для просмотра книг зарегестрируйтесь или войдите в учётную запись\n")
        self.output_widget.config(state="disabled")

        self.entry_frame = tk.Frame(self.root)
        self.entry_frame.place(relx=0.1, rely=0.52, relwidth=0.8, relheight=0.2)
        self.entry_frame.columnconfigure(1, weight=1)

        self.surname_label = tk.Label(self.entry_frame, text="Фамилия:")
        self.surname_entry = tk.Entry(self.entry_frame)

        self.name_label = tk.Label(self.entry_frame, text="Имя:")
        self.name_entry = tk.Entry(self.entry_frame)

        self.username_label = tk.Label(self.entry_frame, text="Имя пользователя:")
        self.username_entry = tk.Entry(self.entry_frame)

        self.password_label = tk.Label(self.entry_frame, text="Пароль:")
        self.password_entry = tk.Entry(self.entry_frame, show="*")

        self.confirm_password_label = tk.Label(self.entry_frame, text="Подтвердите пароль:")
        self.confirm_password_entry = tk.Entry(self.entry_frame, show="*")

        self.buttons_frame = tk.Frame(self.root)
        self.buttons_frame.place(relx=0.1, rely=0.64, relwidth=0.8, relheight=0.8)

        self.reg_button = create_button(self.buttons_frame, "Регистрация", self.show_registration_fields, 0, 0)
        self.login_button = create_button(self.buttons_frame, "Вход", self.show_login_fields, 0, 1)
        self.exit_button = create_button(self.buttons_frame, "Выход", self.exit_app, 0, 2)

        self.library_button = None
        self.logout_button = None

        self.booklist_button = None
        self.readbook_button = None
        self.back_button = None

        self.library_buttons_created = False

        for i in range(3):
            self.buttons_frame.columnconfigure(i, weight=1)

        self.hide_entry_fields()

    def clear_entries(self):
        self.surname_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.confirm_password_entry.delete(0, tk.END)

    def hide_entry_fields(self):
        self.surname_label.grid_forget()
        self.surname_entry.grid_forget()
        self.name_label.grid_forget()
        self.name_entry.grid_forget()
        self.username_label.grid_forget()
        self.username_entry.grid_forget()
        self.password_label.grid_forget()
        self.password_entry.grid_forget()
        self.confirm_password_label.grid_forget()
        self.confirm_password_entry.grid_forget()

    def show_registration_fields(self):
        self.hide_entry_fields()
        self.surname_label.grid(row=0, column=0, sticky=tk.W)
        self.surname_entry.grid(row=0, column=1, sticky=tk.W + tk.E)
        self.name_label.grid(row=1, column=0, sticky=tk.W)
        self.name_entry.grid(row=1, column=1, sticky=tk.W + tk.E)
        self.username_label.grid(row=2, column=0, sticky=tk.W)
        self.username_entry.grid(row=2, column=1, sticky=tk.W + tk.E)
        self.password_label.grid(row=3, column=0, sticky=tk.W)
        self.password_entry.grid(row=3, column=1, sticky=tk.W + tk.E)
        self.confirm_password_label.grid(row=4, column=0, sticky=tk.W)
        self.confirm_password_entry.grid(row=4, column=1, sticky=tk.W + tk.E)
        
        self.reg_button.config(command=self.register)


    def show_login_fields(self):
        self.hide_entry_fields()
        self.username_label.grid(row=2, column=0, sticky=tk.W)
        self.username_entry.grid(row=2, column=1, sticky=tk.W + tk.E)
        self.password_label.grid(row=3, column=0, sticky=tk.W)
        self.password_entry.grid(row=3, column=1, sticky=tk.W + tk.E)

        self.login_button.config(command=self.login)


    def register(self):
        self.output_widget.config(state="normal")
        self.logged_in_username, self.logged_in_surname, self.logged_in_name = register_user(
            self.users_data_file,
            self.output_widget,
            self.surname_entry,
            self.name_entry,
            self.username_entry,
            self.password_entry,
            self.confirm_password_entry,
            self.clear_entries
        )
        if self.logged_in_username:
            self.output_widget.insert(tk.END, f"Регистрация и вход выполнены успешно! Добро пожаловать, {self.logged_in_name} {self.logged_in_surname}!\n")
            self.output_widget.insert(tk.END, "Теперь вы сможете ознакомиться с библиотекой\n")
            self.show_library_buttons()
        self.output_widget.config(state="disabled")
        self.reg_button.config(command=self.show_registration_fields)


    def login(self):
        self.output_widget.config(state="normal")
        self.logged_in_username, self.logged_in_surname, self.logged_in_name = login_user(
            self.users_data_file,
            self.output_widget,
            self.username_entry,
            self.password_entry,
            self.clear_entries
        )
        if self.logged_in_username:
            self.show_library_buttons()
        self.output_widget.config(state="disabled")
        self.login_button.config(command=self.show_login_fields)

    def exit_app(self):
        self.root.destroy()

    def logout(self):
        self.output_widget.config(state="normal")
        self.output_widget.insert(tk.END, f"Вы вышли из учетной записи {self.logged_in_name} {self.logged_in_surname}.\n")
        self.output_widget.see(tk.END)
        self.logged_in_username = None
        self.logged_in_surname = None
        self.logged_in_name = None

        if self.booklist_button:
            self.booklist_button.grid_forget()
        if self.readbook_button:
            self.readbook_button.grid_forget()
        if self.back_button:
            self.back_button.grid_forget()

        self.show_login_register_buttons()

        self.output_widget.config(state="disabled")
        self.clear_entries()
        self.hide_entry_fields()

    def show_login_register_buttons(self):
        if self.booklist_button:
            self.booklist_button.grid_forget()
            self.booklist_button = None
        if self.readbook_button:
            self.readbook_button.grid_forget()
            self.readbook_button = None
        if self.back_button:
            self.back_button.grid_forget()
            self.back_button = None

        self.reg_button.grid(row=0, column=0)
        self.login_button.grid(row=0, column=1)
        self.exit_button.grid(row=0, column=2)

        if self.library_button:
            self.library_button.grid_forget()
            self.library_button = None
        if self.logout_button:
            self.logout_button.grid_forget()
            self.logout_button = None

        
        self.library_buttons_created = False

    def show_library_buttons(self):
        if self.reg_button:
            self.reg_button.grid_forget()
        if self.login_button:
            self.login_button.grid_forget()
        if self.exit_button:
            self.exit_button.grid_forget()
        self.hide_entry_fields()

        self.library_button = create_button(self.buttons_frame, "Библиотека", self.open_library, 0, 0)
        self.logout_button = create_button(self.buttons_frame, "Выход из учетной записи", self.logout, 0, 1)
        self.exit_button = create_button(self.buttons_frame, "Выход", self.exit_app, 0, 2)
        self.library_buttons_created = True

    def open_library(self):
        self.output_widget.config(state="normal")
        self.output_widget.insert(tk.END, "\nЗдесь вы сможете ознакомится с функционалом:\n")
        self.output_widget.insert(tk.END, "Весь список книг\n")
        self.output_widget.insert(tk.END, "Читать книгу\n")
        self.output_widget.insert(tk.END, "Назад\n")
        self.output_widget.see(tk.END)
        self.output_widget.config(state="disabled")

        if self.library_button:
            self.library_button.grid_forget()
        if self.logout_button:
            self.logout_button.grid_forget()
        if self.exit_button:
            self.exit_button.grid_forget()

        self.booklist_button = create_button(self.buttons_frame, "Весь список книг", self.show_booklist, 0, 0)
        self.readbook_button = create_button(self.buttons_frame, "Читать книгу", self.open_book, 0, 1)
        self.back_button = create_button(self.buttons_frame, "Назад", self.show_library_buttons, 0, 2)


    def show_booklist(self):

        if self.back_button:
            self.back_button.destroy()
            self.back_button = None

        self.back_button2 = create_button(self.buttons_frame, "Назад", self.show_library_buttons, 0, 2)
            
        self.output_widget.config(state="normal")
        self.output_widget.insert(tk.END, "\nПолный каталог литературы:\n")
        self.output_widget.see(tk.END)

        conn = sqlite3.connect("your_database.db")
        cursor = conn.cursor()

        try:
            cursor.execute('SELECT * FROM Books')
            books = cursor.fetchall()

            for book in books:
                self.output_widget.insert(tk.END, str(book) + "\n")
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
            choice = simpledialog.askstring("Открыть книгу", "Введите номер файла для открытия (или bck - назад):")
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
