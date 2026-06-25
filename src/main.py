import sys
import argparse
from pathlib import Path
from scanner import scan_directory
from duplicates import find_duplicates
from comparator import compare_directories


def main():
    parser = argparse.ArgumentParser(description="Индексатор папок: сканирование, дубликаты и бэкап")
    parser.add_argument("directory", type=str, nargs="?", help="Путь к исходной папке")
    parser.add_argument("--backup", "-b", type=str, help="Путь к резервной копии")

    parser.add_argument("--ext", "-e", type=str, help="Фильтр по расширению.")

    args = parser.parse_args()

    if not args.directory:
        print("Ошибка: Путь не может быть пустым.", file=sys.stderr)
        sys.exit(1)

    target_dir = Path(args.directory)

    if not target_dir.exists() or not target_dir.is_dir():
        print(f"Ошибка: Путь '{target_dir}' не существует.", file=sys.stderr)
        sys.exit(1)

    print(f"Сканирование исходной папки: {target_dir.resolve()}")
    if args.ext:
        print(f"Применен фильтр расширений: {args.ext}")

    source_files = scan_directory(target_dir, args.ext)
    print(f"Найдено файлов: {len(source_files)}\n")

    print("Поиск дубликатов...")
    duplicates = find_duplicates(source_files)
    if not duplicates:
        print("Дубликаты не найдены.\n")
    else:
        print(f"Найдено групп дубликатов: {len(duplicates)}")
        for f_hash, paths in duplicates.items():
            print(f"Группа (хэш: {f_hash[:8]}...):")
            for p in paths:
                print(f"  - {p}")
        print()

    if args.backup:

        backup_dir = Path(args.backup)

        if not backup_dir.exists() or not backup_dir.is_dir():
            print(f"Ошибка: Путь бэкапа '{backup_dir}' не существует.", file=sys.stderr)
            sys.exit(1)

        diff = compare_directories(target_dir, backup_dir, args.ext)

        print("\nОТЧЕТ О РАСХОЖДЕНИЯХ")

        if diff['missing']:
            print(f"\nОтсутствуют в бэкапе ({len(diff['missing'])}):")
            for p in diff['missing']: print(f"  - {p}")

        if diff['modified']:
            print(f"\nИзмененные файлы ({len(diff['modified'])}):")
            for p in diff['modified']: print(f"  - {p}")

        if diff['extra']:
            print(f"\nЛишние файлы в бэкапе ({len(diff['extra'])}):")
            for p in diff['extra']: print(f"  - {p}")

        if not diff['missing'] and not diff['modified'] and not diff['extra']:
            print("Папки полностью идентичны.")


if __name__ == "__main__":
    main()