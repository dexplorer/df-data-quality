install:
	pip install --upgrade pip &&\
	pip install -r requirements.txt

lint:
	pylint --disable=R,C *.py &&\
	pylint --disable=R,C dq_app/*.py &&\
	pylint --disable=R,C dq_app/utils/*.py &&\
	pylint --disable=R,C dq_app/tests/*.py
	# pylint --disable=R,C dq_rule.py

test:
	python -m pytest -vv --cov=dq_app_core dq_app/tests/test_dq_app_core.py &&\
	python -m pytest -vv --cov=dq_rule dq_app/tests/test_dq_rule.py

format:
	black *.py &&\
	black dq_app/*.py &&\
	black dq_app/utils/*.py &&\
	black dq_app/tests/*.py
	# black cfg/*.yaml

all:
	install lint format test
