
print("Добро пожаловать в библиотеку LitFeath")
print("Версия библиотеки 0.141")
print("Здесь вы сможете ознакомится с нашим асортиментом книг")
print("Для просмотра книг зарегестрируйтесь или войдите в учётную запись")

import sqlite3

def register_user(users_data_file):
    while True:
        surname = input("Введите фамилию: ")
        name = input("Введите имя: ")

        while True:
            username = input("Введите имя пользователя (логин, от 3 до 16 символов): ")
            if 3 <= len(username) <= 16:
                break
            else:
                print("Имя пользователя должно содержать от 3 до 16 символов. Попробуйте снова.")

        while True:
            password = input("Введите пароль (от 8 до 16 символов): ")
            if 8 <= len(password) <= 16:
                break
            else:
                print("Пароль должен содержать от 8 до 16 символов. Попробуйте снова.")

        confirm_password = input("Подтвердите пароль: ")

        if password != confirm_password:
            print("Пароли не совпадают. Попробуйте снова.")
            continue

        try:
            with open(users_data_file, 'r') as f:
                for line in f:
                    stored_username, _, _, _ = line.strip().split(':')
                    if stored_username == username:
                        print("Имя пользователя уже занято. Попробуйте другое.")
                        break
                else:
                    with open(users_data_file, 'a') as f:
                        f.write(f"{username}:{surname}:{name}:{password}\n")
                    print("Регистрация прошла успешно!")
                    return
        except FileNotFoundError:
            with open(users_data_file, 'w') as f:
                f.write(f"{username}:{surname}:{name}:{password}\n")
            print("Регистрация прошла успешно!")
            return


def login_user(users_data_file):
    username = input("Введите имя пользователя (логин): ")
    password = input("Введите пароль: ")

    try:
        with open(users_data_file, 'r') as f:
            for line in f:
                stored_username, surname, name, stored_password = line.strip().split(':')
                if stored_username == username and stored_password == password:
                    print(f"Вход выполнен успешно! Добро пожаловать, {name} {surname}!")
                    print("Теперь вы сможете ознакомится с библиотекой")
                    return stored_username, surname, name
        print("Неверное имя пользователя или пароль.")
        return None, None, None
    except FileNotFoundError:
        print("Ошибка: Файл с данными пользователей не найден.")
        return None, None, None


def registration():
    print("\nВыберите действие:")
    print("Регистрация - reg")
    print("Вход - lin")
    print("Выход - esc")


def authorization():
    print("\nВыберите действие:")
    print("Перейти к библиотеке - lib")
    print("Выход из учётной записи - lou")
    print("Выход - esc")


def library():
    print("\nЗдесь вы сможете ознакомится с функционалом:")
    print("Весь список книг - blt")
    print("Читать книгу(пока не доступно) - rbk")
    print("Назад - bck")


def booklist():
    print("Полный каталог литературы:")
    conn = sqlite3.connect("your_database.db")
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM Books')
    books = cursor.fetchall()

    for book in books:
        print(book)

    conn.close()


def book_sorting():
    print("\nВсе книги вы можете сортировать алфавиту:")
    print("Сортировать по фамилиям авторов - sbl")
    print("Сортировать по именам авторов - sbn")
    print("Сортировать по названиям книг - sbt")
    print("Назад - bck")


def poname():
    conn = sqlite3.connect("your_database.db")
    cursor = conn.cursor()

    cursor.execute("""SELECT name, family, bookname, bookid FROM books
        ORDER BY LOWER(name) ASC
    """)
    results = cursor.fetchall()
    print("Книги были отсортированы по именам авторов:")
    for row in results:
        print(row)

    conn.close()


def pofamily():
    conn = sqlite3.connect("your_database.db")
    cursor = conn.cursor()

    cursor.execute("""SELECT family, name, bookname, bookid FROM books
        ORDER BY LOWER(family) ASC
    """)
    results = cursor.fetchall()
    print("Книги были отсортированы по фамилиям авторов:")
    for row in results:
        print(row)

    conn.close()


def pobookname():
    conn = sqlite3.connect("your_database.db")
    cursor = conn.cursor()

    cursor.execute("""SELECT bookname, name, family, bookid FROM books
        ORDER BY LOWER(bookname) ASC
    """)
    results = cursor.fetchall()
    print("Книги были отсортированы по названию:")
    for row in results:
        print(row)

    conn.close()


def main():
    users_data_file = "users.txt"
    logged_in_username = None
    logged_in_surname = None
    logged_in_name = None

    while True:
        if logged_in_username:
            authorization()
            choice = input("Введите действие: ")

            if choice == "lou":
                print(f"Вы вышли из учетной записи {logged_in_name} {logged_in_surname}.")
                logged_in_username = None
                logged_in_surname = None
                logged_in_name = None
            elif choice == "esc":
                print("Выход из программы.")
                break
            elif choice == "lib":
                library()
                choice2 = input("Введите действие: ")

                if choice2 == "blt":
                    booklist()
                    book_sorting()
                    choice3 = input("Введите действие: ")

                    if choice3 == "sbn":
                        pofamily()
                        book_sorting()
                        choice4 = input("Введите действие: ")

                    elif choice3 == "sbl":
                        poname()
                        book_sorting()
                        choice4 = input("Введите действие: ")

                    elif choice3 == "sbt":
                        pobookname()
                        book_sorting()
                        choice4 = input("Введите действие: ")

                    elif choice3 == "bck":
                        library()
                        choice2 = input("Введите действие: ")

                    else:
                        print("Неверный ввод. Попробуйте снова.")

                elif choice2 == "rbk":
                    library()
                    choice2 = input("Введите действие: ")
                    pass

                elif choice2 == "bck":
                    authorization()
                    choice = input("Введите действие: ")

                else:
                    print("Неверный ввод. Попробуйте снова.")

            else:
                print("Неверный ввод. Попробуйте снова.")

        else:
            registration()
            choice = input("Введите действие: ")

            if choice == "reg":
                register_user(users_data_file)
            elif choice == "lin":
                logged_in_username, logged_in_surname, logged_in_name = login_user(users_data_file)
                if logged_in_username:
                    pass
            elif choice == "esc":
                print("Выход из программы.")
                break
            else:
                print("Неверный ввод. Попробуйте снова.")


if __name__ == "__main__":
    main()
