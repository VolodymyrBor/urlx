test-itself:
	poetry run pytest ./tests -vv ./tests ./urlx --flake8 --mypy \
	--cov ./urlx --cov-branch --cov-fail-under=100

test-cov:
	poetry run pytest --cov ./urlx --cov-report html:.cov_html \
	--cov-report term ./tests/ -vv ./tests ./urlx --cov-branch --flake8 --mypy
