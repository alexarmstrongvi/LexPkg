LexPkg
========
An example packaged python project

# Documentation
To generate the documentation:
```bash
cd docs
make html
open build/html/index.html
```

# Testing
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
