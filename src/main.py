import sys
from pathlib import Path
from scanner import scan_directory

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

    print("Начинаем сканирование...")
    files = scan_directory(target_dir)

    print(f"Найдено файлов: {len(files)}\n")

    for f in files:
        print(f"[{f['mtime']}] {f['size']} байт | {f['path']}")

if __name__ == "__main__":
    main()