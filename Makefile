
clean:
	python3 setup.py clean
	rm -f .coverage *.snap *.tar.bz2
	rm -rf build/ dist/ prime/ stage/ htmlcov/ venv/
	rm -rf *.eggs/ *.egg-info/ .pytest_cache/ .tox/
	@find . -regex '.*\(__pycache__\|\.py[co]\)' -delete

install:
	python3 setup.py install

publish:
	rm -rf dist/
	python3 setup.py sdist
	pip install twine
	twine upload dist/*

test:
	isort lp_fork
	black .
	flake8 --max-line-length=88 lp_fork setup.py
	@echo -e '\xe2\x9c\x85 \xe2\x9c\x85 \xe2\x9c\x85'


venv:
	virtualenv .venv
	.venv/bin/pip install -Ur requirements.txt -Ur requirements-test.txt
	@echo "Now run the following to activate the virtual env:"
	@echo ". .venv/bin/activate"

.PHONY: clean install publish test venv
