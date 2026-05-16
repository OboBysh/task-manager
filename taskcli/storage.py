import json
import os
from .exceptions import StorageError

TASKS_FILE = 'tasks.json'

def load_tasks():
    """Загружает список задач из JSON-файла."""
    if not os.path.exists(TASKS_FILE):
        return []
    try:
        with open(TASKS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if not isinstance(data, list):
                raise StorageError("Файл задач должен содержать список.")
            return data
    except json.JSONDecodeError as e:
        raise StorageError(f"Ошибка чтения JSON: {e}") from e
    except IOError as e:
        raise StorageError(f"Ошибка доступа к файлу {TASKS_FILE}: {e}") from e

def save_tasks(tasks):
    """Сохраняет список задач в JSON-файл."""
    try:
        with open(TASKS_FILE, 'w', encoding='utf-8') as f:
            json.dump(tasks, f, indent=4, ensure_ascii=False)
    except IOError as e:
        raise StorageError(f"Не удалось сохранить задачи: {e}") from e
