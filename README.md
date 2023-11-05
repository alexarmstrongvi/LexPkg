LexPkg
================================================================================

An example packaged python project

![Build Status](https://github.com/alexarmstrongvi/LexPkg/actions/workflows/build_test.yml/badge.svg)
![Code Covrage](https://codecov.io/gh/alexarmstrongvi/LexPkg/branch/main/graph/badge.svg)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/alexarmstrongvi/LexPkg)
![GitHub issues](https://img.shields.io/github/issues/alexarmstrongvi/LexPkg)
![GitHub license](https://img.shields.io/github/license/alexarmstrongvi/LexPkg)
![Stars](https://img.shields.io/github/stars/alexarmstrongvi/LexPkg)

Contents
================================================================================
* [Usage](#usage)
* [Installation](#installation)
* [Development](#development)
* [Python Package Basics](#python-package-basics)
* [Conventions and Style Guide](#conventions-and-style-guide)


<a name="usage"></a>

Usage
================================================================================

Several CLI tools are available after installation
```sh
lexpkg
lexscript
```

The package can be run as a script
```sh
python -m lexpkg
```

The package has example variables, functions, classes, modules, and subpackages
that can be imported
```python
>>> import lexpkg
>>> lexpkg.MY_VARIABLE
'module-scoped variable'
>>> from lexpkg.subpkg import multiply
>>> multiply.multiply_by_six(3)
18
```

The source code includes developer scripts
```sh
./LexPkg/bin/lexscript/dev_script.py
```

## Using as a template

This package can be copied and used as a template for other projects. In that
case, note the following things that should probably be removed:
* Many comments, usually prefixed by "`NOTE:`", that are there purely as
  explanations to users unfamiliar with python package features.
* Many files and source code objects, usually prefixed by "`my_`" or "`My`",
  that are there purely as examples and do not represent actual naming
  conventions.

<a name="installation"></a>

Installation
================================================================================

This package is only available on TestPyPI, if it is available at all:
```sh
pip install --index-url https://test.pypi.org/simple/ --no-deps lexpkg
```

<a name="installation"></a>

Development
================================================================================

```sh
PKG_PATH="path/to/LexPkg"
git clone git@github.com:alexarmstrongvi/LexPkg.git "$PKG_PATH"
pip install --editable "$PKG_PATH"
pip install -r "$PKG_PATH/requirements-dev.txt"
```

<a name="python-package-basics"></a>

Python Package Basics
================================================================================
<a href="#top">back to top of page</a>

## When to consider specific tools and infrastructure
* Your code is a single use script with no 3rd party dependencies
    * No tools needed
* Your code has 3rd party dependencies
    * Package manager and virtual environments: `pip`, `venv`, `.venv`, `requirements.txt` (or `conda` and `environment.yml`)
* Your code is not single use (e.g. others or your future self will look at it and possibly use it)
    * Version control: `git`, `.gitignore`
    * `README.md` (`.txt`, `.rst`)
    * Testing: `tests/`, `pytest`, `doctest`, `unittest`
    * Linting: `pylint`; `flake8`
    * Formatting: `isort`; `black`
    * Complexity Checker: `mccabe`
    * Type Checking: `mypy`
    * Coverage: `coverage`
* Several developers will be adding to the code
    * `pre-commit` and `.pre-commit-config.yaml`
    * `tox`, `tox.ini`
    * CI/CD: GitHub Actions, `.github/workflows`
    * CodeCov
* The code will be used (i.e. installed) by other projects
    * `pyproject.toml`, `setup.cfg`, and/or `setup.py`
    * `MANIFEST.in`
* The code will be publically available
    * `LICENSE.txt`
    * `docs/`, `pydoc`, `sphinx`
    * README badges
    * TestPyPI and PyPI, `twine`

## Setup

### Python developer workspace layout
The following workspace directory structure is recommended and assumed below:
```
└── WORKSPACE_DIR - top level project directory
    ├── src
    │   ├── LexPkg
    │   └── ...other source code, cloned repos, etc.
    ├── bin - scripts and binaries. Helpful to add bin to PATH
    ├── build - outputs from building source code
    ├── outputs - any output files created by running programs
    └── ...data, notebooks, .venv, .git, setup_shell.sh, etc.
```

Most of what goes in WORKSPACE_DIR is personal preference but the layout is
recommended because it nicely supports:
* adding multiple repos in `src/` for development under a common virtual
  environment
* separating files for version control. For example, WORKSPACE_DIR can be a git
  repo that tracks scripts in `bin/` while ignoring files in `build/` and
  `outputs/`.

Instructions below assume the current working directory is `WORKSPACE_DIR`

### Initial environment setup

```bash
cd "$WORKSPACE_DIR"
python -m venv .venv --prompt my_venv_name
source .venv/bin/activate
pip install --upgrade pip
pip install --editable src/LexPkg
pip install -r src/LexPkg/requirements-dev.txt
```

### Reoccuring shell setup
When opening up a new terminal shell, activate the python virtual environment
```bash
source .venv/bin/activate
```

**TIP**: If shell setup becomes more complicated than above, then it is useful to
put all shell setup commands in a bash script `setup_shell.sh`. For example,
```bash
# Virtual Environment
source .venv/bin/activate

# Environment variables
WORKSPACE_DIR='path/to/workspace'
PATH="$PATH:$WORKSPACE_DIR/bin"
PATH="$PATH:$WORKSPACE_DIR/src/LexPkg/bin"
PYTHONPATH="$WORKSPACE_DIR/tools"

# Project specific aliases
alias cdws="cd $WORKSPACE_DIR"
```

## Testing
Manually run tests
```bash
# PyTest
ptest "$LEXPKG_PATH"
# Coverage checker
coverage run -m pytest "$LEXPKG_PATH"
coverage report
# Import order checker
isort --check "$LEXPKG_PATH"
# Linter
pylint "$LEXPKG_PATH" | grep -o "Module.*"
flake8 --extend-exclude .venv --format quiet-filename "$LEXPKG_PATH"
# Autoformatter
black --check "$LEXPKG_PATH"
# Type checker
mypy --exclude docs "$LEXPKG_PATH"
MYPYPATH=src mypy tests/ # for running on tests/ only
# Complexity checker
find ./src -name "*py" | xargs -n1 -t python -m mccabe --min 1
# Pre-commit hooks [THIS WILL MODIFY CODE]
pre-commit run --all-files
# Environment tests
tox "$LEXPKG_PATH"
```

To followup on a specific file
```bash
pytest               path/to/file.py
python -m doctest -v path/to/file.py
coverage report -m   path/to/file.py
isort --check --diff path/to/file.py
pylint               path/to/file.py
flake8               path/to/file.py
black --check --diff path/to/file.py
mypy                 path/to/file.py
python -m mccabe     path/to/file.py
# pre-commit N/A
```
## Documentation
To generate and view the documentation:
```bash
cd docs
make html
open build/html/index.html
```
This is currently not working.

## Distributing package
Commands copied from ["Packaging Python Projects"](https://packaging.python.org/en/latest/tutorials/packaging-projects)

### Generating distribution archives
```bash
pip install --upgrade build
python -m build
```
### Uploading distribution archives

**Initial upload to TestPyPI**
```bash
pip install --upgrade twine
twine upload --repository testpypi dist/*
Enter your username: __token__
Enter your password: <your api token>
```
**Installing package**
```bash
pip install --index-url https://test.pypi.org/simple/ --no-deps lexpkg
```

**Manually publish a new release**

TODO

**Initial upload to PyPI**

TODO

<a name="conventions-and-style-guide"></a>

Conventions and Style Guide
================================================================================
<a href="#top">back to top of page</a>

## Logging

Meaning/Goal of logging levels
* `CRITICAL`
    * Indicates an error occurred that the program cannot gracefully handle
    * **Should never occur**
* `ERROR`
    * Indicates an error occurred that the program will try to handle but
      results may be impacted.
    * **Should never occur in common use cases**
* `WARNING`
    * Indicates something undesirable happened that the program should be able
      to handle without significantly impacting results.
    * **Should never occur in common use cases** but does not require issues
      and can be permanent for unsupported uses cases to discourage users.
* `INFO`
    * Indicates the program is progessing as expected
    * **Should occur frequently enough** so the user knows the program is not
      frozen (e.g. 1/sec) but not so frequently that they are unreadble.
* `DEBUG`
    * Catch all for anything not fitting in the other categories that developers
      need to debug

General guidelines
* With the expection of DEBUG,
    * try to avoid logging so frequently that messages are pushed off screen
      before they can be read
    * try to keep log messages identical for repeated runs to support regression
      testing (e.g. avoid timing and memory usage information)
* For long running programs, provide INFO level messages at least every few
  seconds so the user knows the program is running as expected
* Reserve the use of `print()` for stdout messages that the user may want piped
  to other unix utilities. `logging` defaults to stderr and `print()` defaults
  to stdout for this reason (among others).
