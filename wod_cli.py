import sqlite3

# Подключаемся к базе
conn = sqlite3.connect('my_wod.db')
cursor = conn.cursor()

# Создаём таблицу
cursor.execute('''
CREATE TABLE IF NOT EXISTS characters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    clan TEXT NOT NULL,
    generation INTEGER
)
''')
conn.commit()

def show_all():
    cursor.execute('SELECT * FROM characters')
    rows = cursor.fetchall()
    
    if not rows:
        print("📭 База пуста. Добавьте первого персонажа!")
        return
    
    print("\n" + "="*50)
    print("📋 СПИСОК ВСЕХ ПЕРСОНАЖЕЙ:")
    print("="*50)
    for row in rows:
        print(f"🆔 {row[0]} | 👤 {row[1]} | 🧛 Клан: {row[2]} | 📊 Поколение: {row[3]}")
    print("="*50 + "\n")

def add_character():
    print("\n➕ ДОБАВЛЕНИЕ НОВОГО ПЕРСОНАЖА")
    name = input("Введите имя: ").strip()
    if not name:
        print("❌ Имя не может быть пустым!")
        return
    
    clan = input("Введите клан (Brujah/Toreador/Ventrue и т.д.): ").strip()
    if not clan:
        print("❌ Клан не может быть пустым!")
        return
    
    try:
        gen = int(input("Введите поколение (число от 1 до 15): "))
        if gen < 1 or gen > 15:
            print("❌ Поколение должно быть от 1 до 15!")
            return
    except ValueError:
        print("❌ Поколение должно быть числом!")
        return
    
    cursor.execute('''
    INSERT INTO characters (name, clan, generation)
    VALUES (?, ?, ?)
    ''', (name, clan, gen))
    conn.commit()
    
    print(f"✅ Персонаж '{name}' добавлен в базу!")

def search_by_name():
    print("\n🔍 ПОИСК ПЕРСОНАЖА")
    name = input("Введите имя для поиска: ").strip()
    
    cursor.execute('SELECT * FROM characters WHERE name LIKE ?', (f'%{name}%',))
    rows = cursor.fetchall()
    
    if not rows:
        print(f"❌ Персонажи с именем '{name}' не найдены")
        return
    
    print(f"\n📋 Найдено персонажей: {len(rows)}")
    for row in rows:
        print(f"🆔 {row[0]} | 👤 {row[1]} | 🧛 {row[2]} | 📊 {row[3]}")

def show_menu():
    print("="*50)
    print("          🧛 WORLD OF DARKNESS CLI 🧛")
    print("="*50)
    print("1. 📋 Показать всех персонажей")
    print("2. ➕ Добавить нового персонажа")
    print("3. 🔍 Найти персонажа по имени")
    print("4. ❌ Выйти")
    print("="*50)

def main():
    while True:
        show_menu()
        choice = input("Выберите действие (1-4): ").strip()
        
        if choice == "1":
            show_all()
        elif choice == "2":
            add_character()
        elif choice == "3":
            search_by_name()
        elif choice == "4":
            print("\n👋 До свидания! База данных закрыта.")
            conn.close()
            break
        else:
            print("❌ Неверный выбор. Введите 1, 2, 3 или 4.")
        
        input("\nНажмите Enter, чтобы продолжить...")

if __name__ == "__main__":
    main()
