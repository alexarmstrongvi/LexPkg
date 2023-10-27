import subprocess
from pathlib import Path
from contextlib import contextmanager
import os
from typing import Optional

from lexpkg import PACKAGE_DIR

def find_working_dir(path: Path) -> Optional[Path]:
    while not (path/'.git').is_dir() and path != path.root:
        path = path.parent
    return path if path != path.root else None

# Git working dir should be the same as the package dir assuming the project is
# version controlled with git
WORKING_DIR = find_working_dir(Path(__file__)) or PACKAGE_DIR

@contextmanager
def changed_directory(path: Path):
    if not path.is_dir():
        path = path.parent
    original_dir = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(original_dir)

def get_status(path: Path = WORKING_DIR) -> str:
    with changed_directory(path):
        rv = subprocess.run(['git','status'], capture_output=True)
    if rv.returncode != 0:
        return rv.stderr.decode('utf-8')
    return rv.stdout.decode('utf-8')

def get_hash(path: Path = WORKING_DIR) -> str:
    with changed_directory(path):
        # Option 1) git rev-parse HEAD
        # Option 2) git log -n1 --format="%H"
        rv = subprocess.run(['git','rev-parse','HEAD'], capture_output=True)
    if rv.returncode != 0:
        return rv.stderr.decode('utf-8')
    return rv.stdout.decode('utf-8').strip()

def get_diff(path: Path = WORKING_DIR) -> str:
    # TODO: Include staged diff
    with changed_directory(path):
        rv = subprocess.run(['git','diff'], capture_output=True)
    if rv.returncode != 0:
        return rv.stderr.decode('utf-8')
    return rv.stdout.decode('utf-8')
