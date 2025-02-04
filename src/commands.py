import os
import re
import shutil
from datetime import datetime


def copy_file(source, dest):
    if not os.path.exists(source):
        raise FileNotFoundError(f"Source '{source}' not found")
    shutil.copy(source, dest)
    print(f"Copied '{source}' to '{dest}'")


def delete_path(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Path '{path}' not found")
    if os.path.isfile(path):
        os.remove(path)
        print(f"Deleted file '{path}'")
    else:
        shutil.rmtree(path)
        print(f"Deleted directory '{path}'")


def count_files(path):
    if not os.path.isdir(path):
        raise NotADirectoryError(f"'{path}' is not a directory")
    total = 0
    for _, _, files in os.walk(path):
        total += len(files)
    return total


def search_files(path, pattern):
    if not os.path.isdir(path):
        raise NotADirectoryError(f"'{path}' is not a directory")
    regex = re.compile(pattern)
    matches = []
    for root, _, files in os.walk(path):
        for file in files:
            if regex.search(file):
                matches.append(os.path.join(root, file))
    return matches


def add_date_to_filenames(path, recursive):
    if os.path.isfile(path):
        _process_file(path)
    elif os.path.isdir(path):
        if recursive:
            for root, _, files in os.walk(path):
                for file in files:
                    _process_file(os.path.join(root, file))
        else:
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                if os.path.isfile(item_path):
                    _process_file(item_path)


def _process_file(file_path):
    ctime = os.path.getctime(file_path)
    date_str = datetime.fromtimestamp(ctime).strftime("%Y%m%d")
    dir_name, file_name = os.path.split(file_path)
    base, ext = os.path.splitext(file_name)
    new_name = f"{base}_{date_str}{ext}"
    new_path = os.path.join(dir_name, new_name)
    os.rename(file_path, new_path)
    print(f"Renamed '{file_path}' to '{new_path}'")


def _get_size(path):
    if os.path.isfile(path):
        return os.path.getsize(path)
    total = 0
    for root, _, files in os.walk(path):
        for file in files:
            total += os.path.getsize(os.path.join(root, file))
    return total


def _format_size(size):
    units = ["B", "KB", "MB", "GB"]
    index = 0
    while size >= 1024 and index < 3:
        size /= 1024
        index += 1
    return f"{size:.2f}{units[index]}"


def analyse_directory(path):
    if not os.path.isdir(path):
        raise NotADirectoryError(f"'{path}' is not a directory")
    items = [os.path.join(path, item) for item in os.listdir(path)]
    total_size = sum(_get_size(item) for item in items)
    print(f"Full size: {_format_size(total_size)}")
    entries = []
    for item in items:
        name = os.path.basename(item)
        size = _get_size(item)
        entries.append((name, size))
    entries.sort(key=lambda x: -x[1])
    for name, size in entries:
        print(f"- {name} {_format_size(size)}")
