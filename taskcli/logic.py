from .storage import load_tasks, save_tasks
from .exceptions import TaskNotFoundError, InvalidTaskError

def add_task(description: str, priority: str = "средний", due_date: str = None) -> int:
    """
    Добавляет задачу и возвращает её ID.
    :param description: текст задачи
    :param priority: приоритет (низкий, средний, высокий)
    :param due_date: дата выполнения в формате ГГГГ-ММ-ДД (опционально)
    :return: ID новой задачи
    :raises InvalidTaskError: если описание пустое
    """
    if not description or not description.strip():
        raise InvalidTaskError("Описание задачи не может быть пустым.")
    
    tasks = load_tasks()
    new_id = max([task['id'] for task in tasks], default=0) + 1
    task = {
        'id': new_id,
        'description': description.strip(),
        'completed': False,
        'priority': priority,
        'due_date': due_date
    }
    tasks.append(task)
    save_tasks(tasks)
    return new_id

def view_tasks() -> list:
    """Возвращает список всех задач."""
    return load_tasks()

def delete_task(task_id: int) -> bool:
    """
    Удаляет задачу по ID.
    :returns: True в случае успеха
    :raises TaskNotFoundError: если задача не найдена
    """
    tasks = load_tasks()
    filtered = [task for task in tasks if task['id'] != task_id]
    if len(filtered) == len(tasks):
        raise TaskNotFoundError(task_id)
    save_tasks(filtered)
    return True

def complete_task(task_id: int) -> bool:
    """
    Отмечает задачу выполненной.
    :returns: True
    :raises TaskNotFoundError: если задача не найдена
    :raises InvalidTaskError: если задача уже выполнена
    """
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == task_id:
            if task['completed']:
                raise InvalidTaskError(f"Задача {task_id} уже выполнена.")
            task['completed'] = True
            save_tasks(tasks)
            return True
    raise TaskNotFoundError(task_id)
