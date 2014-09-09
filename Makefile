PUBLISHING_DEPENDENCIES=wheel bumpversion twine

.PHONY: test
test:
	tox

.PHONY: publishing-dependencies
publishing-dependencies:
	pip install -U $(PUBLISHING_DEPENDENCIES)

.PHONY: bump
bump: publishing-dependencies
	$(eval OLD=$(shell python -c "import setup; print setup.__VERSION__"))
	bumpversion minor
	$(eval NEW=$(shell python -c "import setup; print setup.__VERSION__"))
	bzr commit -m "bump version: $(OLD) to $(NEW)"
	bzr tag "v$(NEW)"
	bzr push

.PHONY: update
update:
	python setup.py register

.PHONY: upload
upload: publishing-dependencies
	python setup.py sdist bdist_wheel
	twine upload dist/*

.PHONY: release
release: bump upload


