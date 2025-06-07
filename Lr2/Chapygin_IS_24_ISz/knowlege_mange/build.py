import shutil
from pathlib import Path
from subprocess import call

BINARY_FILE_NAME = 'K-manage'

BUILD_CMD = [
    'pyinstaller',
    'run.py',
    '--name', BINARY_FILE_NAME,
    '--onefile',
]

if __name__ == '__main__':
    call(BUILD_CMD)
    shutil.copy(
        Path.cwd() / 'dist' / (BINARY_FILE_NAME + '.exe'),
        Path.cwd() / (BINARY_FILE_NAME + '.exe'),
    )
