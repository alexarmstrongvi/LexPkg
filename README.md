LexPkg
========
An example packaged python project

# When to consider specific tools and infrastructure
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
    * `pyproject.toml`
    * `setup.cfg` (`setup.py`?)
* The code will be publically available
    * `LICENSE.txt`
    * `MANIFEST.in`
    * `docs/`, `pydoc`, `sphinx`
    * README badges
    * TestPyPI and PyPI, `twine`




# Setup
**Initial environment setup**
```bash
cd path/to/run # path/to/lexpkg also works
path/to/python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
pip install -e path/to/lexpkg
```

**Reoccuring shell setup**
```bash
source .venv/bin/activate
```

# Command line tools
## Testing
Manually run tests
```bash
# PyTest
pytest tests/
# DocTest
python -m unittest -v tests/doctest_runner.py
# Coverage checker
coverage run -m pytest tests/
coverage report
# Import order checker
isort --check ./
# Linter
pylint --recursive y --ignore .venv,.tox,docs ./ | grep -o "Module.*"
flake8 --extend-exclude .venv --format quiet-filename ./
# Autoformatter
black --check ./
# Type checker
mypy --exclude docs ./
MYPYPATH=src mypy tests/ # for running on tests/ only
# Complexity checker
find ./src -name "*py" | xargs -n1 -t python -m mccabe --min 1
# Pre-commit hooks
pre-commit run --all-files
# Environment tests
tox ./
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

# Distributing package
Commands copied from ["Packaging Python Projects"](https://packaging.python.org/en/latest/tutorials/packaging-projects)

## Generating distribution archives
```bash
pip install --upgrade build
python -m build
```
## Uploading distribution archives

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
