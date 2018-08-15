.PHONY: install uninstall reinstall test clean

install:
	pip install .

uninstall:
	pip uninstall wick -y

reinstall: uninstall install

test:
	python -m unittest discover -s tests

clean:
	find . -name "*.pyc" -delete
