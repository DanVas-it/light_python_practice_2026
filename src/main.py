import sys
from pathlib import Path
from scanner import scan_directory
from duplicates import find_duplicates

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

    print("Поиск дубликатов...")
    duplicates = find_duplicates(files)

    if not duplicates:
        print("Дубликаты не найдены.\n")
    else:
        print(f"Найдено групп дубликатов: {len(duplicates)}\n")
        for file_hash, paths in duplicates.items():
            print(f"Группа совпадений (хэш: {file_hash[:8]}...):")
            for path in paths:
                print(f"- {path}")
            print()

if __name__ == "__main__":
    main()