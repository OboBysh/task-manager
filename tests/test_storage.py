import os
import tempfile
from taskcli.storage import load_tasks, save_tasks, TASKS_FILE

def test_save_and_load():
    test_file = 'test_tasks.json'
    original = TASKS_FILE
    # подменяем путь на временный
    import taskcli.storage as storage_mod
    storage_mod.TASKS_FILE = test_file
    try:
        sample = [{'id': 1, 'description': 'Test', 'completed': False}]
        save_tasks(sample)
        assert load_tasks() == sample
    finally:
        storage_mod.TASKS_FILE = original
        if os.path.exists(test_file):
            os.remove(test_file)

def test_load_empty_when_missing():
    # убеждаемся, что если файла нет, возвращается пустой список
    assert isinstance(load_tasks(), list)
