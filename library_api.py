from fastapi import FastAPI
import sqlite3
from datetime import datetime
from pydantic import BaseModel

app = FastAPI(title = "Библиотека")

def get_db():
    conn = sqlite3.connect('Libary.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS libary (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        year INTEGER,
        is_read BOOLEAN DEFAULT False,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
    conn.commit()
    conn.close()

init_db()
