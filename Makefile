install:
	pip install --upgrade pip &&\
	pip install -r requirements.txt

lint:
	pylint --disable=R,C dq_app.py

test:
	python -m pytest -vv --cov=dq_app test_dq_app.py

format:
	black *.py

all:
	install lint format test
