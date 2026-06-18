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
        file_hash = calculate_file_hash(file_info['path'])
        if file_hash:
            if file_hash not in hashes_map:
                hashes_map[file_hash] = []

            hashes_map[file_hash].append(file_info['path'])

    duplicates = {}
    for file_hash, paths in hashes_map.items():
        if len(paths) > 1:
            duplicates[file_hash] = paths

    return duplicates