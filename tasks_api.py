from fastapi import FastAPI
import sqlite3
from datetime import datetime
# Подключили библиотеки


app = FastAPI(title = "Task manager")#Подписываем стартовую страницу

#Подключаем базу
def get_db():
    conn = sqlite3.connect('Tasks.db')
    conn.row_factory = sqlite3.Row #Делаем нормальный вывод строки
    return conn

# Создадим таблицу
def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        completed BOOLEAN DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
    conn.commit()
    conn.close()

init_db()


@app.get('/tasks')
def get_tasks():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall()
    conn.close()


    return [dict(task) for task in tasks]




from pydantic import BaseModel

# Схема для создания задачи
class TaskCreate(BaseModel):
    title: str
    description: str = None

@app.post("/tasks")
def create_task(task: TaskCreate):
    if not task.title:
        return {"error": "Title cannot be empty"}, 400
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO tasks (title, description, completed)
    VALUES (?, ?, ?)
    ''', (task.title, task.description, False))
    conn.commit()
    
    # Получаем созданную задачу
    task_id = cursor.lastrowid
    cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
    new_task = cursor.fetchone()
    conn.close()
    
    return dict(new_task)

class TaskUpdate(BaseModel):
    title: str
    description: str = None
    completed: bool

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: TaskUpdate):
    if not task.title:
        return {"error": "Title cannot be empty"}, 400
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Проверяем, существует ли задача
    cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
    existing = cursor.fetchone()
    if not existing:
        conn.close()
        return {"error": "Task not found"}, 404
    
    # Обновляем
    cursor.execute('''
    UPDATE tasks 
    SET title = ?, description = ?, completed = ?
    WHERE id = ?
    ''', (task.title, task.description, task.completed, task_id))
    conn.commit()
    
    # Получаем обновлённую
    cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
    updated = cursor.fetchone()
    conn.close()
    
    return dict(updated)


class TaskPatch(BaseModel):
    completed: bool

@app.patch("/tasks/{task_id}")
def patch_task(task_id: int, task: TaskPatch):
    conn = get_db()
    cursor = conn.cursor()
    
    # Проверяем существование
    cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
    existing = cursor.fetchone()
    if not existing:
        conn.close()
        return {"error": "Task not found"}, 404
    
    # Обновляем только completed
    cursor.execute('''
    UPDATE tasks 
    SET completed = ?
    WHERE id = ?
    ''', (task.completed, task_id))
    conn.commit()
    
    # Получаем обновлённую
    cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
    updated = cursor.fetchone()
    conn.close()
    
    return dict(updated)

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    conn = get_db()
    cursor = conn.cursor()
    
    # Проверяем существование
    cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
    existing = cursor.fetchone()
    if not existing:
        conn.close()
        return {"error": "Task not found"}, 404
    
    # Удаляем
    cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    
    return {"message": "Task deleted successfully"}


