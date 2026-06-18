import os
from datetime import datetime
from pathlib import Path


def scan_directory(target_dir: Path):
    files_metadata = []

    base_path = str(target_dir)

    def traverse(current_path: str):
        try:
            items = os.listdir(current_path)
        except PermissionError:
            return

        for item in items:
            full_path = os.path.join(current_path, item)

            if os.path.isdir(full_path):
                traverse(full_path)

            elif os.path.isfile(full_path):
                try:
                    stat = os.stat(full_path)
                    size_bytes = stat.st_size
                    mod_time = datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')

                    files_metadata.append({
                        'path': full_path,
                        'size': size_bytes,
                        'mtime': mod_time
                    })
                except (PermissionError, OSError):
                    continue

    traverse(base_path)

    return files_metadata