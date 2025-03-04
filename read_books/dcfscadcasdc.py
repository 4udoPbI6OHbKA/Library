import os

def opa(file):
    try:
        os.startfile(file)
    except FileNotFoundError:
        print(f"Ошибка: Файл '{file}' не найден.")
    except OSError:
        print(f"Ошибка: Не удалось открыть файл с помощью блокнота.")


# Пример использования
file = "booklist.txt"  # Замените на имя вашего файла
opa(file)
