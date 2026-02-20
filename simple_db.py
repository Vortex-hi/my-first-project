import sqlite3

conn = sqlite3.connect('my_simple.db')

cursor = conn.cursor()


cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER
)
''')

conn.commit()

cursor.execute('''
INSERT INTO users (name, age) VALUES (?, ?)
''', ('Иван', 25))

conn.commit()

cursor.execute('SELECT * FROM users')
rows = cursor.fetchall()
print("После добавления Ивана:")
for row in rows:
    print(f"  ID: {row[0]}, {row[1]}, {row[2]} лет")

conn.close()
print("Готово! База закрыта")
