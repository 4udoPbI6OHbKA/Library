print("Добро пожаловать в библиотеку LitFeath")
print("Версия библиотеки 0.1")
print("Здесь вы сможете ознакомится с нашим асортиментом книг")
print("Для просмотра книг зарегестрируйтесь или войдите в учётную запись")

def register_user(users_data_file):
    while True:
        surname = input("Введите фамилию: ")
        name = input("Введите имя: ")
        username = input("Введите имя пользователя (логин): ")
        password = input("Введите пароль: ")
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
    print("Читать книгу - rbk")
    print("Назад - bck")

    
def booklist():
    print("Полный каталог литературы:")
    



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
                choice = input("Введите действие: ")

                if choice == "blt":
                    
                
                
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
