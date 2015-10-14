PUBLISHING_DEPENDENCIES=wheel bumpversion twine
TOX=$(shell which detox || which tox)


.PHONY: test
test: lint
	$(TOX)

.PHONY: lint
lint:
	flake8 localmail tests twisted

.PHONY: publishing-dependencies
publishing-dependencies:
	pip install -U $(PUBLISHING_DEPENDENCIES)

.PHONY: bump
bump: publishing-dependencies
	$(eval OLD=$(shell python -c "import setup; print setup.__VERSION__"))
	bumpversion minor
	$(MAKE) __finish_bump OLD=$(OLD)

__finish_bump:
	$(eval NEW=$(shell python -c "import setup; print setup.__VERSION__"))
	bzr commit -m "bump version: $(OLD) to $(NEW)"
	bzr tag "v$(NEW)"

.PHONY: update
update:
	python setup.py register

.PHONY: upload
upload: publishing-dependencies
	python setup.py sdist bdist_wheel
	twine upload dist/*

.PHONY: release
release: bump upload


