import json

def add_id(id):
    """Добавляет id в список запощеных
    Args:
        id: Id новости"""
    with open("used.json", "r") as fp:
        data = json.load(fp)
    data.append(id)
    with open("used.json", "w") as fp:
        data = json.dump(data, fp)

def check_id(id):
    """Проверяет, есть ли id в списке запощеных
    Args:
        id: Id новости"""
    with open("used.json", "r") as fp:
        data = json.load(fp)
    return id in data