import sys
from pathlib import Path

def main():
    user_input = input("Введите путь к папке для сканирования: ").strip()

    if not user_input:
        print("Ошибка: Путь не может быть пустым.", file=sys.stderr)
        sys.exit(1)

    target_dir = Path(user_input)

    if not target_dir.exists() or not target_dir.is_dir():
        print(f"Ошибка: Путь '{target_dir}' не существует или не является папкой.", file=sys.stderr)
        sys.exit(1)

    print(f"Успешно! Выбрана папка для сканирования: {target_dir.resolve()}")

if __name__ == "__main__":
    main()