import sqlite3

conn = sqlite3.connect("your_database.db")
cursor = conn.cursor()
cursor.execute('SELECT * FROM Books')
books = cursor.fetchall()

for book in books:
  print(book)
conn.close()
