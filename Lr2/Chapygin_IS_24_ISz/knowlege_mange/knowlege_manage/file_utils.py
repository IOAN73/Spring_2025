import os
from pathlib import Path


def create_directory(directory_name):
    os.mkdir(directory_name)


def create_file(filename):
    with open(filename, 'w', encoding='utf-8') as file:
        return file.write('')


def file_read(file_name):
    with open(file_name, encoding='utf-8') as file:
        return file.read()


def file_write(file_name, text):
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(text)


def rename_file(old_name, new_name):
    os.rename(old_name, new_name)


def delete_file(rem_file_name):
    os.remove(rem_file_name)


def get_nodes(folder: Path):
    folder = folder.resolve()
    tree = _scan_folder(folder)
    nodes = _convert_to_nodes(tree, folder, folder)
    return nodes


def _scan_folder(folder):
    tree = {}
    for root, dirs, files in os.walk(folder):
        root_path = Path(root)
        relative_root = root_path.relative_to(folder)
        current_level = tree
        for part in relative_root.parts:
            current_level = current_level.setdefault(part, {})
        current_level['__files__'] = files
    return tree


def _convert_to_nodes(tree, parent_path, root_path):
    nodes = []
    for key, value in tree.items():
        if key == '__files__':
            for file in value:
                file_path = root_path / file
                nodes.append({'id': str(file_path.relative_to(parent_path)), 'label': file})
            continue
        full_path = root_path / key
        node = {'id': str(full_path.relative_to(parent_path)), 'label': key}
        children = _convert_to_nodes(value, parent_path, full_path)
        if children:
            node['child'] = children
        nodes.append(node)
    return nodes
