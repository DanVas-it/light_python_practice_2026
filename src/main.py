import sys
import argparse
from pathlib import Path
from scanner import scan_and_analyze  # Импортируем нашу новую функцию


def main():
    parser = argparse.ArgumentParser(description="Потоковое сканирование папки, поиск дубликатов и сравнение с бэкапом")
    parser.add_argument("directory", type=str, nargs="?", help="Путь к папке для сканирования")
    parser.add_argument("--backup", "-b", type=str, help="Путь к папке резервной копии для сравнения")

    args = parser.parse_args()

    if not args.directory:
        print("Ошибка: Путь не может быть пустым.", file=sys.stderr)
        sys.exit(1)

    target_dir = Path(args.directory)

    if not target_dir.exists() or not target_dir.is_dir():
        print(f"Ошибка: Путь '{target_dir}' не существует или не является папкой.", file=sys.stderr)
        sys.exit(1)

    backup_dir = Path(args.backup) if args.backup else None
    if backup_dir and (not backup_dir.exists() or not backup_dir.is_dir()):
        print(f"Ошибка: Путь бэкапа '{backup_dir}' не существует или не папка.", file=sys.stderr)
        sys.exit(1)

    print(f"Успешно! Выбрана папка для сканирования: {target_dir.resolve()}")
    if backup_dir:
        print(f"Выбрана папка бэкапа для сравнения: {backup_dir.resolve()}")

    print("\nЗапуск анализа файловой системы...")

    total_files, duplicates, diff = scan_and_analyze(target_dir, backup_dir)

    print(f"Сканирование завершено. Обработано файлов в источнике: {total_files}\n")

    print("=== ОТЧЕТ О ДУБЛИКАТАХ ===")
    if not duplicates:
        print("Дубликаты не найдены.\n")
    else:
        print(f"Найдено групп дубликатов: {len(duplicates)}\n")
        for file_hash, paths in duplicates.items():
            print(f"Группа совпадений (хэш: {file_hash[:8]}...):")
            for path in paths:
                print(f"  - {path}")
            print()

    # --- Вывод сравнения с бэкапом ---
    if backup_dir:
        print("=== ОТЧЕТ О РАСХОЖДЕНИЯХ С БЭКАПОМ ===")

        # 1. Отсутствующие файлы
        if diff['missing']:
            print(f"\n[!] Отсутствуют в бэкапе ({len(diff['missing'])} шт.):")
            for p in diff['missing']:
                print(f"  - {p}")
        else:
            print("\n✔ Отсутствующие файлы: отсутствуют (все файлы на месте)")

        # 2. Измененные файлы
        if diff['modified']:
            print(f"\n[~] Измененные файлы ({len(diff['modified'])} шт.):")
            for p in diff['modified']:
                print(f"  - {p}")
        else:
            print("✔ Измененные файлы: нет изменений")

        # 3. Лишние файлы
        if diff['extra']:
            print(f"\n[+] Лишние файлы в бэкапе ({len(diff['extra'])} шт.):")
            for p in diff['extra']:
                print(f"  - {p}")
        else:
            print("✔ Лишние файлы в бэкапе: нет лишних")


if __name__ == "__main__":
    main()