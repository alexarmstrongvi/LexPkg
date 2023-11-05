"""Utilities for scripts."""
# Standard library
import configparser
from copy import deepcopy
import json
import logging
from pathlib import Path
import shutil
import time
from typing import Iterable, Optional

try:  # isort: split
    # Standard library
    import tomllib  # Added in python 3.11
except ImportError:
    # 3rd party
    import tomli as tomllib  # type: ignore

# 3rd party
import yaml

# 1st party
from lexpkg import user_input

# Globals
log = logging.getLogger(__name__)


################################################################################
# NOTE: Projects are better off choosing a single configuration format so the
# read and save functions below are mostly a reference for how to read files in
# the various configuration libraries. Currently, I prefer YAML for configuring
# scripts
def read_config(path: Path) -> dict:
    """Read configuration file."""
    if path.suffix in (".yaml", ".yml"):
        with path.open("r") as ifile:
            cfg = yaml.safe_load(ifile)
    elif path.suffix == ".json":
        with path.open("r") as ifile:
            cfg = json.load(ifile)
    elif path.suffix == ".ini":
        cfg = configparser.ConfigParser()
        cfg.read(path)
        # NOTE: This type conversion is not perfect so consider sticking with
        # ConfigParser if INI is the configuration file type for the project
        cfg = dict(cfg)
    elif path.suffix == ".toml":
        with path.open("rb") as ifile:
            cfg = tomllib.load(ifile)
    else:
        raise NotImplementedError(f"Unexpected file format: {path}")
    return cfg


def save_config(cfg: dict, path: Path) -> None:
    """Save configuration settings."""
    if path.suffix in (".yaml", ".yml"):
        with path.open("w") as ofile:
            yaml.safe_dump(cfg, ofile)
    elif path.suffix == ".json":
        with path.open("w") as ofile:
            json.dump(cfg, ofile)
    # NOTE: There is no standard way to convert a python dictionary to INI
    # or TOML format as they are more limited than JSON and YAML
    else:
        raise NotImplementedError(f"Unexpected file format: {path}")


def merge_config_files(
    cfgs: Iterable[dict],
    default_cfg: Optional[dict] = None,
) -> dict:
    """Merge configuration files with later ones overwriting earlier ones.

    Parameters
    ==========
    cfgs:
        Separate configurations to be merged
    default_cfg:
        Configuration with default values for all parameters

    Returns
    =======
    Single merged configuration file
    """
    if default_cfg is not None:
        merged_cfg = deepcopy(default_cfg)
        allow_new_keys = False
    else:
        merged_cfg = {}
        allow_new_keys = True

    for cfg_update in cfgs:
        update_config(
            original=merged_cfg,
            update=cfg_update,
            copy=False,
            allow_new_keys=allow_new_keys,
        )
    return merged_cfg


def update_config(
    original: dict,
    update: dict,
    copy: bool = True,
    allow_new_keys: bool = False,
    concat_lists: bool = False,
    overwrite_lists: bool = False,
) -> dict:
    """Update a configuration dictionary using a dictionary with updated
    values.

    The intended use case is combining common configuration formats (e.g. YAML,
    JSON, TOML) after being read into python dictionaries. Therefore, this
    function aims to handle the subset of python types these configuration
    formats support (e.g. int, float, str, dict, list). Other types (e.g. tuple,
    set, numpy array, bytes) are not handled in any special way and therefore
    will overwrite the original value similar to an int or float value.

    Parameters
    ==========
    original:
        Original configuration dictionary
    update:
        Configuration dictionary with values to update in the original
    copy:
        Apply updates to a copy of the original, returning a new dictionary
    allow_new_keys:
        Allow the update to contain keys not in the original
    concat_lists:
        Update lists by concatenating them, allowing duplicates
    overwrite_lists:
        Update lists by overwriting the original with the updated list

    Returns
    =======
    Updated configuration dictionary
    """

    if copy:
        # Use shallow copy to reduce memory usage
        # This requires care be taken when updating mutable values below
        original = original.copy()

    for key, val in update.items():
        if key not in original:
            if not allow_new_keys:
                raise KeyError(f"{key!r} not in original dictionary")
            original[key] = val
        elif isinstance(val, dict):
            if original[key] is None:
                original[key] = update_config({}, val, copy, allow_new_keys=True)
            else:
                original[key] = update_config(original[key], val, copy, allow_new_keys)
        elif isinstance(val, list):
            original_list = original[key] or []
            if overwrite_lists:
                original[key] = val
            elif concat_lists:
                original[key] = original_list + val
            else:
                original[key] = update_list(original_list, val)
        else:
            original[key] = val

    return original


def update_list(original, update):
    """Append new elements, preserving order from both lists.

    This will not handle duplicates already in the original or update.
    It is assumed the user intends those duplicates.
    """
    merged_list = original.copy()
    for x in update:
        if x not in original:
            merged_list.append(x)
    return merged_list


def require_empty_dir(
    path: Path,
    parents: bool = False,
    overwrite: bool = False,
) -> None:
    # Make directory if it doesn't exist or is empty
    if not path.is_dir():
        path.mkdir(parents=parents)
        return
    if not any(path.iterdir()):
        return

    if not overwrite:
        # Check if user wants to delete contents of directory
        overwrite = user_input.request_permission(f"Delete contents of {path}?")

    files = list(path.rglob("*"))
    if overwrite:
        log.warning("Deleting all %d files from %s", len(files), path)
        time.sleep(2)  # Give the user a moment to realize if this was a mistake
        shutil.rmtree(path)
        path.mkdir(parents=parents)
    else:
        raise FileExistsError(
            f"{len(files)} files found (e.g. {files[0].name}): {path}"
        )
