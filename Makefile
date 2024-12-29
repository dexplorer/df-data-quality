install:
	pip install --upgrade pip &&\
	pip install -r requirements.txt

lint:
	pylint --disable=R,C *.py
	# pylint --disable=R,C dq_rule.py

test:
	python -m pytest -vv --cov=dq_app_core tests/test_dq_app_core.py &&\
	python -m pytest -vv --cov=dq_rule tests/test_dq_rule.py

format:
	black *.py &&\
	black tests/*.py
	# black cfg/*.yaml

all:
	install lint format test
