from pathlib import Path
from scanner import scan_directory

def compare_directories(source_base: Path, backup_base: Path, ext_filter: str = None):
    source_files = scan_directory(source_base, ext_filter)
    backup_files = scan_directory(backup_base, ext_filter)

    source_map = {}
    for f in source_files:
        rel_path = str(Path(f['path']).relative_to(source_base))
        source_map[rel_path] = f

    backup_map = {}
    for f in backup_files:
        rel_path = str(Path(f['path']).relative_to(backup_base))
        backup_map[rel_path] = f

    result = {
        'missing': [],
        'modified': [],
        'extra': []
    }

    for rel_path, src_info in source_map.items():
        if rel_path not in backup_map:
            result['missing'].append(rel_path)
        else:
            bak_info = backup_map[rel_path]
            if src_info['hash'] != bak_info['hash'] or src_info['size'] != bak_info['size']:
                result['modified'].append(rel_path)

    for rel_path in backup_map:
        if rel_path not in source_map:
            result['extra'].append(rel_path)

    return result