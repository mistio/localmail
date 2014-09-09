
.PHONY: test
test:
	tox

.PHONY: register
register:
	python setup.py register

.PHONY: upload
upload:
	python setup.py register sdist upload
	python setup.py bdist_wheel upload

