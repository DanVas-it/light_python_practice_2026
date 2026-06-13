from pathlib import Path
from datetime import datetime

def scan_directory(target_dir: Path):

    files_metadata = []

    # Метод rglob('*') рекурсивно ищет все файлы и папки
    for path in target_dir.rglob('*'):
        if path.is_file():
            stat = path.stat()

            size_bytes = stat.st_size

            mod_time = datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')

            # Сохраняем данные
            files_metadata.append({
                'path': str(path),
                'size': size_bytes,
                'mtime': mod_time
            })

    return files_metadata