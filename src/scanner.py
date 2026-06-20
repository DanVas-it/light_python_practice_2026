import os
import hashlib
from datetime import datetime
from pathlib import Path

def calculate_file_hash(filepath: str, chunk_size: int = 4096):
    hasher = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            while chunk := f.read(chunk_size):
                hasher.update(chunk)
        return hasher.hexdigest()
    except (PermissionError, OSError):
        return None

def scan_and_analyze(target_dir: Path, backup_dir: Path = None):
    target_str = str(target_dir)
    backup_str = str(backup_dir) if backup_dir else None

    hashes_map = {}
    diff = {
        'missing': [],   # Есть в источнике, но нет в бэкапе
        'modified': [],  # Есть везде, но изменен
        'extra': []      # Нет в источнике, но есть в бэкапе
    }
    total_source_files = 0

    def traverse_source(current_path: str):
        nonlocal total_source_files
        try:
            items = os.listdir(current_path)
        except PermissionError:
            return

        for item in items:
            full_path = os.path.join(current_path, item)

            if os.path.isdir(full_path):
                traverse_source(full_path)
            elif os.path.isfile(full_path):
                total_source_files += 1
                try:
                    stat = os.stat(full_path)
                    size = stat.st_size
                    mtime = datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')

                    f_hash = calculate_file_hash(full_path)
                    if f_hash:
                        if f_hash not in hashes_map:
                            hashes_map[f_hash] = []
                        hashes_map[f_hash].append(full_path)

                    if backup_str:
                        rel_path = os.path.relpath(full_path, target_str)
                        backup_file_path = os.path.join(backup_str, rel_path)

                        if not os.path.exists(backup_file_path):
                            diff['missing'].append(rel_path)
                        else:
                            b_stat = os.stat(backup_file_path)
                            b_size = b_stat.st_size
                            b_mtime = datetime.fromtimestamp(b_stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')

                            if size != b_size or mtime != b_mtime:
                                diff['modified'].append(rel_path)

                except (PermissionError, OSError):
                    continue

    def traverse_backup_for_extra(current_path: str):
        try:
            items = os.listdir(current_path)
        except PermissionError:
            return

        for item in items:
            full_path = os.path.join(current_path, item)

            if os.path.isdir(full_path):
                traverse_backup_for_extra(full_path)
            elif os.path.isfile(full_path):
                rel_path = os.path.relpath(full_path, backup_str)
                source_file_path = os.path.join(target_str, rel_path)

                if not os.path.exists(source_file_path):
                    diff['extra'].append(rel_path)

    traverse_source(target_str)

    if backup_str:
        traverse_backup_for_extra(backup_str)

    duplicates = {h: paths for h, paths in hashes_map.items() if len(paths) > 1}

    return total_source_files, duplicates, diff