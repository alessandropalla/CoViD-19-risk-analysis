
install: python
	echo "Installation completed"

python:
	pip install -r requirements.txt

test:
	echo "Start regression tests"
	python3 -m pytest
