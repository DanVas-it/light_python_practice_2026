import sys
from pathlib import Path
from scanner import scan_directory
from duplicates import find_duplicates
from comparator import compare_directories

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

    answer = input("Хотите сравнить эту папку с бэкапом? (y/n): ").strip().lower()

    if answer in ('y', 'yes', 'д', 'да'):
        backup_input = input("Введите путь к папке резервной копии: ").strip()
        if not backup_input:
            print("Сравнение отменено: не указан путь.", file=sys.stderr)
            return

        backup_dir = Path(backup_input)
        if not backup_dir.exists() or not backup_dir.is_dir():
            print(f"Ошибка: Путь бэкапа '{backup_dir}' не существует или не папка.", file=sys.stderr)
            sys.exit(1)

        print("Сканирование резервной копии...")
        backup_files = scan_directory(backup_dir)

        diff = compare_directories(files, target_dir, backup_files, backup_dir)

        print("\nОТЧЕТ О РАСХОЖДЕНИЯХ")

        # 1. Отсутствующие файлы
        if diff['missing']:
            print(f"\nОтсутствуют в бэкапе ({len(diff['missing'])} шт.):")
            for p in diff['missing']:
                print(f"- {p}")
        else:
            print("\nОтсутствующие файлы: отсутствуют (все файлы на месте)")

        # 2. Измененные файлы
        if diff['modified']:
            print(f"\nИзмененные файлы ({len(diff['modified'])} шт.):")
            for p in diff['modified']:
                print(f"- {p}")
        else:
            print("Измененные файлы: нет изменений")

        # 3. Лишние файлы
        if diff['extra']:
            print(f"\nЛишние файлы в бэкапе ({len(diff['extra'])} шт.):")
            for p in diff['extra']:
                print(f"- {p}")
        else:
            print("Лишние файлы в бэкапе: нет лишних")

if __name__ == "__main__":
    main()