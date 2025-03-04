import subprocess
import platform
import os

def opa1(путь_к_директории):
  файлы = []
  try:
    for filename in os.listdir(путь_к_директории):
      if filename.endswith(".txt"):
        файлы.append(filename)
  except FileNotFoundError:
    print(f"Ошибка: Директория '{путь_к_директории}' не найдена.")
    return None
  return файлы

def opa(имя_файла):
  try:
    if platform.system() == "Windows":
      subprocess.Popen(["notepad.exe", имя_файла])
    elif platform.system() == "Darwin":
      subprocess.Popen(["open", имя_файла])
    else:
      subprocess.Popen(["xdg-open", имя_файла])
  except FileNotFoundError:
    print(f"Ошибка: Файл '{имя_файла}' не найден.")
  except Exception as e:
    print(f"Произошла ошибка: {e}")

def opa2():
  base_path = os.path.join(os.path.expanduser("~"), "Desktop", "LibFeath", "library")
  books_path = os.path.join(base_path, "books")

  файлы = opa1(books_path)

  if файлы is None or not файлы:
    print("В директории 'books' нет текстовых файлов.")
    return

  print("Доступные файлы:")
  for i, filename in enumerate(файлы):
    print(f"{i+1}. {filename}")

  while True:
    try:
      выбор = int(input("Введите номер файла для открытия (или 0 для выхода): "))
      if выбор == 0:
        return
      if 1 <= выбор <= len(файлы):
        выбранный_файл = os.path.join(books_path, файлы[выбор-1])
        opa(выбранный_файл)
        break
      else:
        print("Неверный номер файла. Попробуйте еще раз.")
    except ValueError:
      print("Пожалуйста, введите число.")

opa2()
