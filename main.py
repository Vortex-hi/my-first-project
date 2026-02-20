from fastapi import FastAPI

app = FastAPI(title="World of Darkness API")

# Временные данные (потом уйдут в БД)
clans = [
    {"id": 1, "name": "Brujah", "description": "Бунтари, философы и панки"},
    {"id": 2, "name": "Toreador", "description": "Художники, эстеты, одержимые красотой"},
    {"id": 3, "name": "Ventrue", "description": "Аристократы, лидеры, властители"},
    {"id": 4, "name": "Malkavian", "description": "Безумцы, провидцы, проклятые"},
    {"id": 5, "name": "Nosferatu", "description": "Чудовища с лицами, хранители тайн"},
]

characters = [
    {"id": 1, "name": "Maxim Strauss", "clan_id": 3, "generation": 7, "description": "Князь Сан-Франциско, архивист"},
    {"id": 2, "name": "Damsel", "clan_id": 1, "generation": 9, "description": "Анарх, бармен в The Last Round"},
    {"id": 3, "name": "Gary Golden", "clan_id": 5, "generation": 8, "description": "Владыка туннелей, примигент"},
]

# ---- Эндпоинты для кланов ----
@app.get("/clans")
def get_clans():
    return clans

@app.get("/clans/{clan_id}")
def get_clan(clan_id: int):
    for clan in clans:
        if clan["id"] == clan_id:
            return clan
    return {"error": "Clan not found"}

# ---- Эндпоинты для персонажей ----
@app.get("/characters")
def get_characters():
    return characters

@app.get("/characters/{char_id}")
def get_character(char_id: int):
    for char in characters:
        if char["id"] == char_id:
            return char
    return {"error": "Character not found"}

# ---- Создание нового персонажа (пока просто добавляем в список) ----
@app.post("/characters")
def create_character(name: str, clan_id: int, generation: int, description: str = ""):
    new_id = max([c["id"] for c in characters]) + 1 if characters else 1
    character = {
        "id": new_id,
        "name": name,
        "clan_id": clan_id,
        "generation": generation,
        "description": description
    }
    characters.append(character)
    return character
