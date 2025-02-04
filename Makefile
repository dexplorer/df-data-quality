install: requirements.txt
	pip install --upgrade pip &&\
	pip install -r requirements.txt

setup: 
	# python setup.py install
	pip install . 

lint:
	pylint --disable=R,C *.py &&\
	pylint --disable=R,C dq_app/*.py &&\
	pylint --disable=R,C dq_app/tests/*.py

test:
	python -m pytest -vv --cov=dq_app dq_app/tests

format:
	black *.py &&\
	black dq_app/*.py &&\
	black dq_app/tests/*.py

all:
	install setup lint format test
