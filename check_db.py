import sqlite3

conn = sqlite3.connect('my_simple.db')
cursor = conn.cursor()

cursor.execute('SELECT * FROM users')
rows = cursor.fetchall()

print("Содержимое базы my_simple.db:")
for row in rows:
    print(f"ID: {row[0]}, Имя: {row[1]}, Возраст: {row[2]}")

conn.close()
