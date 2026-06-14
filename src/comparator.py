from pathlib import Path

def compare_directories(source_files: list, source_base: Path, backup_files: list, backup_base: Path):

    source_map = {}
    for f in source_files:
        rel_path = str(Path(f['path']).relative_to(source_base))
        source_map[rel_path] = f

    backup_map = {}
    for f in backup_files:
        rel_path = str(Path(f['path']).relative_to(backup_base))
        backup_map[rel_path] = f

    result = {
        'missing': [], # Есть в источнике, но нет в бэкапе (отсутствующие)
        'modified': [], # Есть везде, но изменился размер или дата (измененные)
        'extra': [] # Нет в источнике, но есть в бэкапе (лишние)
    }

    for rel_path, src_info in source_map.items():
        if rel_path not in backup_map:
            result['missing'].append(rel_path)
        else:
            bak_info = backup_map[rel_path]
            if src_info['size'] != bak_info['size'] or src_info['mtime'] != bak_info['mtime']:
                result['modified'].append(rel_path)

    for rel_path in backup_map:
        if rel_path not in source_map:
            result['extra'].append(rel_path)

    return result