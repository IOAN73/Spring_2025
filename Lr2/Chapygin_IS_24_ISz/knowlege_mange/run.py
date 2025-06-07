import subprocess
import os
from pathlib import Path

os.environ['PYTHONPATH'] = str(Path.cwd())


COMMAND = [
    '.venv\\Scripts\\python.exe',
    Path.cwd()  / 'knowlege_manage' / 'main.py'
]

if __name__ == '__main__':
    subprocess.call(COMMAND)
