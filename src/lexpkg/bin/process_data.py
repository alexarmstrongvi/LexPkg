#!/usr/bin/env python
"""Example script of processing data.

>> process_data.py -i inputs/ -o output/
>> process_data.py -i inputs/ -o output/ -l DEBUG --log-file run.log --log-cli-level INFO
>> process_data.py -c my_config.yml
>> process_data.py -c my_config.yml -o output/ -l DEBUG

This script includes more features than necessary for simple personal-
use scripts. Feel free to keep what you need. The target use case for
this example is a script intended for many users, with many
configuration options, multiple inputs and outputs, and a need for
reproducibility.
"""

# Standard library
import argparse
from copy import deepcopy
from datetime import datetime
import logging
import os
from pathlib import Path
import pprint
import sys

# 3rd party
import yaml

# 1st party
from lexpkg import SRC_DIR, git, scripting
from lexpkg.logging_utils import (
    configure_logging,
    require_root_console_handler,
    summarize_logging,
    summarize_version_control,
    update_log_filenames,
)

# Globals
log = logging.getLogger(__name__)
DEFAULT_CFG = SRC_DIR / "data/process_data.yml"


################################################################################
def main():
    validate_environment()

    # Load and merge all user configuration options
    args = parse_argv()
    default_cfg = scripting.read_config(DEFAULT_CFG)
    cfgs = (scripting.read_config(Path(p)) for p in args.configs)
    cfg = scripting.merge_config_files(cfgs, default_cfg)
    cfg = override_config(cfg, args)
    cfg = reformat_config(cfg)
    validate_config(cfg)

    # Get common configuration sections and parameters
    icfg = cfg["inputs"]
    ocfg = cfg["outputs"]
    odir = Path(ocfg["dir"])

    # Setup
    if ocfg["timestamp_subdir"]:
        odir = odir / datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    scripting.require_empty_dir(odir, ocfg["overwrite"])
    update_log_filenames(odir, ocfg["logging"])
    configure_logging(**ocfg["logging"])
    require_root_console_handler(args.log_cli_level)
    log.debug("Logging Summary:\n%s", summarize_logging())

    # Reproducibility
    log.debug("Final configuration:\n%s", pprint.pformat(cfg, indent=4))
    opath = odir / "config.yml"
    yaml.safe_dump(cfg, opath.open("w"))
    log.info("Final configuration saved: %s", opath)

    log.debug("Version Control Summary:\n%s", summarize_version_control())
    opath = odir / "git_diff.patch"
    opath.write_text(git.get_diff())
    log.info("Git diff patch saved: %s", opath)

    # NOTE: The following is use-case dependent so is mostly for illustration.

    # Run
    img_dir = Path(icfg["image_dir"])
    img_suffix = icfg["image_suffix"]
    scores = []
    for path in img_dir.glob(f"*{img_suffix}"):
        img = read_image(path, icfg["color_mode"])
        preprocessed_img = preprocess(img, **cfg["preprocessing"])

        if ocfg["debug_images"] and path.name in ocfg["debug_images"]:
            save_image(preprocessed_img, odir / f"preprocessed_{path.name}")
            log.debug("Saved preprocessed image: %s", path.name)

        score = compute_score(preprocessed_img, **cfg["scoring"])
        scores.append(score)

    # Save outputs
    if ocfg["scores_fname"] is not None:
        opath = odir / ocfg["scores_fname"]
        save_scores(scores, opath)
        log.info("Output scores saved: %s", opath)

    log.info("*** Program finished ***")


################################################################################
# Business logic
# pylint: disable=unused-argument
def read_image(path, color_mode):
    return [[1, 2, 3], [4, 5, 6], [7, 8, 9]]


def preprocess(img, kwarg1=None, kwarg2=None):
    return [[pixel / 255 for pixel in row] for row in img]


def compute_score(img, kwarg1=None, kwarg2=None, **kwargs):
    return sum(sum(row) for row in img)


def save_image(img, opath):
    opath.write_text(str(img))


def save_scores(scores, opath):
    opath.write_text(str(scores))


# pylint: enable=unused-argument


################################################################################
# Scripting functions that do not generalize well beyond this script
def validate_environment() -> None:
    """Validate the program's runtime environment."""
    if os.name == "nt":
        raise OSError("I have not tested any of this on Windows")
    if "HOME" not in os.environ:
        raise OSError("$HOME not set in current shell")


def parse_argv() -> argparse.Namespace:
    """Parse command line arguments (i.e. sys.argv)"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c",
        "--configs",
        nargs="+",
        default=[],
        help="Configuration files",
    )
    parser.add_argument(
        "-i",
        "--input",
        type=Path,
        help="Inputs",
    )
    parser.add_argument(
        "-o",
        "--odir",
        type=Path,
        help="Directory for saving all outputs",
    )
    parser.add_argument(
        "-l",
        "--log-level",
        choices=("CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"),
        help="Root logging level",
    )
    parser.add_argument(
        "--log-file",
        type=Path,
        help="Logging output file",
    )
    parser.add_argument(
        "--log-cli-level",  # log_cli_level
        choices=("CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"),
        help="Console logging level (if stricter than root level)",
    )
    return parser.parse_args()


def override_config(cfg: dict, args: argparse.Namespace, copy: bool = True) -> dict:
    """Override configuration settings with command line arguments."""
    if copy:
        cfg = deepcopy(cfg)
    if args.input:
        cfg["inputs"]["image_dir"] = str(args.input)
    if args.odir:
        cfg["outputs"]["dir"] = str(args.odir)
    log_cfg = cfg["outputs"]["logging"]
    if args.log_level:
        if "level" in log_cfg:
            log_cfg["level"] = args.log_level
    if args.log_file:
        if "filename" in log_cfg:
            log_cfg["filename"] = str(args.log_file)
    return cfg


def reformat_config(cfg: dict) -> dict:
    """Reformat and/or update configuration.

    I generally recommend avoiding this if possible as it obscures the
    relationship between the input configuration file layout and the
    configuration dictionary that gets used in the code. Ideally,
    configuration settings adhere to three principles:

    1) The layout of the file matches the layout of the dictionary anywhere it
    is used in the code
    2) The configuration parameters are uncoupled as far as the user knows
    (e.g. they don't have to think about if changing one parameter requires
    changing another).
    3) The configuration dictionary is not passed throughout the code as a
    single argument (e.g. `run_stuff(cfg)`). Instead only the relevant
    parameters are passed, preferably as kwargs instead of a dictionary of
    kargs (e.g. `run_stuff(**cfg['run_stuff_kwargs'])`)

    While the above is ideal, if it's unclear how to refactor the code to
    keep the configuration organized or time is limited, at least put all
    the reformatting in one place so developers know where to look when
    things are not behaving as they expect.
    """

    # Configuration parameters in one section may need to be shared in
    # other sections. YAML does have anchors and aliases to accomplish this but,
    # apart from simple use-cases, I find this logic is better handled in the
    # code, especially if users want to merge multiple configuration files.
    cfg["scoring"]["new_kwarg"] = cfg["preprocessing"]["kwarg2"]

    # Default configuration parameters may need to change depending on other
    # configuration options set by the user. Good design of the configuration
    # should prevent this coupling when possible, allowing the code to handle it
    # downstream instead.
    if cfg["inputs"]["image_suffix"] != ".png":
        cfg["preprocessing"]["kwarg1"] = 9

    return cfg


def validate_config(cfg: dict) -> None:
    """Validate values in configuration now before they cause problems
    later."""
    # NOTE: It is not important to check for every error but often there are
    # some common user errors that may lead to confusing error messages or not
    # cause issues until later in the program (e.g. typo in an output path). For
    # long-running programs, it can be much more convenient to notice these
    # errors right away and provide helpful errors messages.

    # Check for valid paths
    if cfg["inputs"]["image_dir"] is None:
        log.error("Input directory not set")
        sys.exit()
    idir = Path(cfg["inputs"]["image_dir"])
    if not idir.is_dir():
        raise FileNotFoundError(idir)

    if cfg["outputs"]["dir"] is None:
        log.error("Output directory not set")
        sys.exit()
    odir = Path(cfg["outputs"]["dir"])
    if not odir.parent.is_dir():
        raise FileNotFoundError(odir.parent)

    # Check for valid values
    valid_color_modes = ("RGB", "BGR", "GRAYSCALE", "UNCHANGED")
    if cfg["inputs"]["color_mode"] not in valid_color_modes:
        cm = cfg["inputs"]["color_mode"]
        raise ValueError(f"color_mode {cm}. Choose from {valid_color_modes}")

    # Check for valid types
    if not isinstance(cfg["outputs"]["overwrite"], bool):
        t = type(cfg["outputs"]["overwrite"])
        raise TypeError(f"Overwrite flag must be bool: {t}")


if __name__ == "__main__":
    main()
