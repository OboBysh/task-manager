class StorageError(Exception):
    """Ошибка при работе с хранилищем данных."""
    pass

class TaskNotFoundError(Exception):
    """Задача с указанным ID не найдена."""
    def __init__(self, task_id: int):
        super().__init__(f"Задача с ID {task_id} не найдена.")
        self.task_id = task_id

class InvalidTaskError(Exception):
    """Некорректные данные задачи (например, пустое описание)."""
    pass
