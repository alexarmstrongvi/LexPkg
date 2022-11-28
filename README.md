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
    * Linting: `pylint` and `.pylintrc`; `flake8`
    * Formatting: `isort`; `black`
    * Complexity Checker: `mccabe`
    * Type Checking: `mypy`
    * Coverage: `coverage`
* Several developers will be adding to the code
    * `pre-commit` and `.pre-commit-config.yaml`
    * `tox`, `tox.ini`
    * CI/CD: GitHub Actions, CodeCov
* The code will be used (i.e. installed) by other projects
    * `pyproject.toml`
    * `setup.cfg` (`setup.py`?)
* The code will be publically available
    * `LICENSE.txt`
    * `MANIFEST.in`
    * `docs/`, `pydoc`, `sphinx`
    * README badges
    * TestPyPI and PyPI

# Command line tools

## Testing
Manually run tests
```bash
# PyTest
pytest tests/
# DocTest
python -m unittest -v tests/doctest_runner.py
# Import order checker
isort --check --skip .env ./
# Linter
pylint --recursive y --ignore .env ./ | grep -o "Module.*"
# Autoformatter
black --check ./
# Type checker
mypy src/
```
To followup on a specific file
```bash
pytest               path/to/file.py
python -m doctest -v path/to/file.py
isort --check --diff path/to/file.py
pylint ./            path/to/file.py
black --check --diff path/to/file.py
mypy                 path/to/file.py
```
## Documentation
To generate and view the documentation:
```bash
cd docs
make html
open build/html/index.html
```
This is currently not working.
