# Run isort to sort imports
poetry run isort .

# Run autopep8 to fix code
poetry run black .

# Check other requirements of PEP8
poetry run flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics --ignore=E203,W503 --exclude venv/

# Exit-zero treats all errors as warnings.
poetry run flake8 . --count --exit-zero --max-complexity=15 --max-line-length=79 --statistics --exclude venv/

# Check autopep8 was run
poetry run autopep8 --recursive --aggressive --exclude venv --diff .

# Check mypy
poetry run mypy --ignore-missing-imports . --exclude venv/

# Fail if total coverage is below 95%
poetry run pytest --cov=src/ --cov-fail-under=95 --cov-report term-missing tests/
