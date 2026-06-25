import hashlib


def calculate_file_hash(filepath: str, chunk_size: int = 4096):

    hasher = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            while chunk := f.read(chunk_size):
                hasher.update(chunk)
        return hasher.hexdigest()
    except (PermissionError, OSError):
        return None


def find_duplicates(files_metadata: list):
    hashes_map = {}

    for file_info in files_metadata:
        f_hash = file_info.get('hash')
        if f_hash:
            if f_hash not in hashes_map:
                hashes_map[f_hash] = []
            hashes_map[f_hash].append(file_info['path'])

    duplicates = {h: paths for h, paths in hashes_map.items() if len(paths) > 1}
    return duplicates