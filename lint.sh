poetry run isort --check --profile black . || { echo "ERROR isort"; exit 1; }
poetry run mypy --strict . || { echo ERROR mypy; exit 1; }
poetry run ruff check . || { echo ERROR ruff; exit 1; }
poetry run pylint --recursive=y . || { echo ERROR pylint; exit 1; }
poetry run flake8 . || { echo ERROR flake8; exit 1; }
poetry run black --check . || { echo ERROR black; exit 1; }
echo "SUCCESS"
