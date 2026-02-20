import sqlite3

conn = sqlite3.connect('my_simple.db')
cursor = conn.cursor()

# Добавляем Марию
cursor.execute('INSERT INTO users (name, age) VALUES (?, ?)', ('Мария', 30))
conn.commit()

# Проверяем
cursor.execute('SELECT * FROM users')
rows = cursor.fetchall()

print("После добавления Марии:")
for row in rows:
    print(f"ID: {row[0]}, Имя: {row[1]}, Возраст: {row[2]}")

conn.close()
