import argparse
from .logic import add_task, view_tasks, delete_task, complete_task
from .exceptions import TaskNotFoundError, InvalidTaskError, StorageError

def main():
    parser = argparse.ArgumentParser(description="CLI-менеджер списка дел")
    subparsers = parser.add_subparsers(dest='command', help='Доступные команды')

    # Команда add
    add_parser = subparsers.add_parser('add', help='Добавить задачу')
    add_parser.add_argument('description', type=str, help='Текст задачи')
    add_parser.add_argument(
        '-p', '--priority', choices=['низкий', 'средний', 'высокий'],
        default='средний', help='Приоритет (по умолчанию: средний)'
    )
    add_parser.add_argument(
        '--due', type=str, default=None,
        help='Дата выполнения в формате ГГГГ-ММ-ДД'
    )

    # Команда view
    subparsers.add_parser('view', help='Показать все задачи')

    # Команда delete
    delete_parser = subparsers.add_parser('delete', help='Удалить задачу по ID')
    delete_parser.add_argument('id', type=int, help='ID задачи для удаления')

    # Команда complete
    complete_parser = subparsers.add_parser('complete', help='Отметить задачу выполненной')
    complete_parser.add_argument('id', type=int, help='ID задачи для отметки')

    args = parser.parse_args()

    try:
        if args.command == 'add':
            task_id = add_task(args.description, args.priority, args.due)
            print(f"✅ Задача добавлена с ID {task_id}.")
        elif args.command == 'view':
            tasks = view_tasks()
            if not tasks:
                print("📭 Список задач пуст.")
                return
            print("\n--- Список дел ---")
            priority_symbols = {
                'высокий': '!!!',
                'средний': ' ! ',
                'низкий': '   '
            }
            for t in tasks:
                status = "[x]" if t['completed'] else "[ ]"
                prio = priority_symbols.get(t.get('priority', 'средний'), ' ? ')
                due = f" (до {t['due_date']})" if t.get('due_date') else ""
                print(f"{status} {prio} ID {t['id']}: {t['description']}{due}")
            print("--------------------")
        elif args.command == 'delete':
            delete_task(args.id)
            print(f"🗑️ Задача {args.id} удалена.")
        elif args.command == 'complete':
            complete_task(args.id)
            print(f"✅ Задача {args.id} отмечена выполненной.")
        else:
            parser.print_help()
    except (TaskNotFoundError, InvalidTaskError, StorageError) as e:
        print(f"❌ Ошибка: {e}")
        exit(1)
