test-itself:
	poetry run pytest ./tests -vv ./tests ./cleanurl --flake8 --mypy \
	--cov ./cleanurl --cov-branch --cov-fail-under=100

test-cov:
	poetry run pytest --cov ./cleanurl --cov-report html:.cov_html \
	--cov-report term ./tests/ -vv ./tests ./cleanurl --cov-branch --flake8 --mypy
