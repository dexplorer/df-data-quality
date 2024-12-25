install:
	pip install --upgrade pip &&\
	pip install -r requirements.txt

lint:
	pylint --disable=R,C *.py
	# pylint --disable=R,C dq_rule.py

test:
	python -m pytest -vv --cov=dq_app tests/test_dq_app.py &&\
	python -m pytest -vv --cov=dq_rule tests/test_dq_rule.py

format:
	black *.py

all:
	install lint format test
