import pytest
from taskcli.logic import add_task, delete_task, complete_task, view_tasks
from taskcli.storage import save_tasks
from taskcli.exceptions import TaskNotFoundError, InvalidTaskError

@pytest.fixture(autouse=True)
def reset_storage():
    """Перед каждым тестом очищаем хранилище."""
    save_tasks([])

def test_add_task():
    tid = add_task("Тест")
    assert tid == 1
    tasks = view_tasks()
    assert len(tasks) == 1
    assert tasks[0]['description'] == "Тест"
    assert tasks[0]['completed'] == False

def test_add_empty_description():
    with pytest.raises(InvalidTaskError):
        add_task("   ")

def test_delete_existing():
    tid = add_task("Удаляемая")
    delete_task(tid)
    assert len(view_tasks()) == 0

def test_delete_nonexistent():
    with pytest.raises(TaskNotFoundError):
        delete_task(999)

def test_complete():
    tid = add_task("Выполнимая")
    complete_task(tid)
    assert view_tasks()[0]['completed'] == True

def test_complete_twice():
    tid = add_task("Дважды")
    complete_task(tid)
    with pytest.raises(InvalidTaskError):
        complete_task(tid)
