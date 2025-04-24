import json

def cargar_productos():
    with open("productos.json", "r", encoding="utf-8") as f:
        return json.load(f)