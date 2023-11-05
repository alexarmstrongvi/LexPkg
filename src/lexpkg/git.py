# Standard library
import logging
from pathlib import Path
import subprocess
from typing import Optional

# 1st party
from lexpkg import PACKAGE_DIR

# Globals
log = logging.getLogger(__name__)


################################################################################
def find_working_dir(path: Path) -> Optional[Path]:
    while not (path / ".git").is_dir() and path != path.root:
        path = path.parent
    return path if path != path.root else None


# Git working dir should be the same as the package dir assuming the project is
# version controlled with git
WORKING_DIR = find_working_dir(Path(__file__)) or PACKAGE_DIR


################################################################################
def get_status(path: Path = WORKING_DIR) -> str:
    return subprocess.check_output(
        args=["git", "status"],
        text=True,
        cwd=path,
    )


def get_hash(path: Path = WORKING_DIR) -> str:
    return subprocess.check_output(
        args=["git", "rev-parse", "HEAD"],
        # args = ['git','log', '-n', '1', '--format', '%H'],
        text=True,
        cwd=path,
    ).strip()


def get_diff(path: Path = WORKING_DIR) -> str:
    return subprocess.check_output(
        args=["git", "diff", "HEAD"],
        text=True,
        cwd=path,
    )
