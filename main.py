from fastapi import FastAPI

# Создаем приложение
app = FastAPI()

# Словарь с данными (потом заменим на базу данных)
users = {
    1: {"name": "Иван", "age": 25},
    2: {"name": "Мария", "age": 30}
}

# GET-запрос на главную страницу
@app.get("/")
def root():
    return {"message": "Hello World"}

# GET-запрос для получения всех пользователей
@app.get("/users")
def get_users():
    return users

# GET-запрос для получения одного пользователя по ID
@app.get("/users/{user_id}")
def get_user(user_id: int):
    if user_id in users:
        return users[user_id]
    return {"error": "User not found"}
