import argparse
import json
import os

# Определяем файл, где будут храниться задачи
TASKS_FILE = 'tasks.json'

def load_tasks():
    """Загружает задачи из JSON файла."""
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return [] # Возвращаем пустой список, если файл пуст или поврежден
    return []

def save_tasks(tasks):
    """Сохраняет задачи в JSON файл."""
    with open(TASKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, indent=4, ensure_ascii=False)

def add_task(description):
    """Добавляет новую задачу в список."""
    tasks = load_tasks()
    task = {
        'id': len(tasks) + 1,
        'description': description,
        'completed': False
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"Задача '{description}' добавлена с ID {task['id']}.")

def view_tasks():
    """Отображает все задачи в списке."""
    tasks = load_tasks()
    if not tasks:
        print("Задачи не найдены. Добавьте задачи!")
        return

    print("\n--- Ваш список дел ---")
    for task in tasks:
        status = "[x]" if task['completed'] else "[ ]"
        print(f"{status} ID {task['id']}: {task['description']}")
    print("-----------------------")

def delete_task(task_id):
    """Удаляет задачу по ее ID."""
    tasks = load_tasks()
    initial_task_count = len(tasks)
    tasks = [task for task in tasks if task['id'] != task_id]
    
    if len(tasks) < initial_task_count:
        save_tasks(tasks)
        print(f"Задача с ID {task_id} удалена.")
    else:
        print(f"Задача с ID {task_id} не найдена.")

def complete_task(task_id):
    """Отмечает задачу как выполненную по ее ID."""
    tasks = load_tasks()
    found = False
    for task in tasks:
        if task['id'] == task_id:
            task['completed'] = True
            found = True
            break
    
    if found:
        save_tasks(tasks)
        print(f"Задача с ID {task_id} отмечена как выполненная.")
    else:
        print(f"Задача с ID {task_id} не найдена.")

def main():
    """Основная функция для обработки аргументов командной строки и выполнения команд."""
    parser = argparse.ArgumentParser(
        description="Простое CLI-приложение для списка дел."
    )

    subparsers = parser.add_subparsers(dest='command', help='Доступные команды')

    # Команда добавления
    add_parser = subparsers.add_parser('add', help='Добавить новую задачу')
    add_parser.add_argument('description', type=str, help='Описание задачи')

    # Команда просмотра
    view_parser = subparsers.add_parser('view', help='Просмотреть все задачи')

    # Команда удаления
    delete_parser = subparsers.add_parser('delete', help='Удалить задачу по ID')
    delete_parser.add_argument('id', type=int, help='ID задачи для удаления')

    # Команда выполнения
    complete_parser = subparsers.add_parser('complete', help='Отметить задачу как выполненную по ID')
    complete_parser.add_argument('id', type=int, help='ID задачи для отметки как выполненной')

    args = parser.parse_args()

    if args.command == 'add':
        add_task(args.description)
    elif args.command == 'view':
        view_tasks()
    elif args.command == 'delete':
        delete_task(args.id)
    elif args.command == 'complete':
        complete_task(args.id)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
