install: pyproject.toml
	pip install --upgrade pip &&\
	TMPDIR=/home/ec2-user/pip_cache pip install --cache-dir=/home/ec2-user/pip_cache --editable . &&\
	pip install --editable .[cli] &&\
	pip install --editable .[api] &&\
	pip install --editable .[test]
	
lint:
	pylint --disable=R,C src/dq_app/*.py &&\
	# pylint --disable=R,C src/dq_app/*/*.py &&\
	pylint --disable=R,C tests/*.py

test:
	python -m pytest -vv --cov=src/dq_app tests

format:
	black src/dq_app/*.py &&\
	# black src/dq_app/*/*.py &&\
	black tests/*.py

all:
	install lint format test
