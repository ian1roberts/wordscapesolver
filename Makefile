# This makefile will not be used in production - only for building, testing, running locally, and publishing
SHELL := /bin/bash

# this is essential to enable BuildKit features, like --ssh default
export DOCKER_BUILDKIT=1

# import deploy config
ifneq ($(wildcard deploy.env),)
    deployfile=deploy.env
    include $(deployfile)
    export $(shell sed 's/=.*//' $(deployfile))
    APP_NAME = $(ECR_REPOSITORY_NAME)
endif

PKG_SRC = wordscapesolver
TESTS_SRC = tests
TAG = $(shell git describe --abbrev=0 --tags --exact-match 2>/dev/null || true)

.PHONY: clean build test docker-clean docker-login docker-build docker-push

ifeq ($(strip $(TAG)),)
        VERSION_TARGET=.bump2version-patch
else
        VERSION_TARGET=.bump2version-set
endif

define get_version
	$(shell cat setup.py | grep "version" | cut -d'"' -f4 | xargs )
endef

tox:
	tox

lint:
	black --check --diff $(PKG_SRC) $(TESTS_SRC) setup.py
	flake8 $(PKG_SRC) $(TESTS_SRC)
	mypy --ignore-missing-imports --no-warn-no-return --show-error-codes --allow-redefinition $(PKG_SRC)
	pylint $(PKG_SRC) $(TESTS_SRC) setup.py
	shellcheck bin/*.sh

black:
	black $(PKG_SRC) $(TESTS_SRC) setup.py

test:
	pytest -s --cov=$(PKG_SRC) --cov-report xml $(TESTS_SRC)

build:
	python setup.py sdist

version-get:
	@echo $(call get_version)

.bump2version-patch:
	bump2version patch

.bump2version-set:
	bump2version --new-version $(TAG)

bump-version: $(VERSION_TARGET)

docker-login:
	aws ecr get-login-password --region $(ECR_REGION) | docker login --username AWS --password-stdin $(DOCKER_REPO)

docker-bash:
	$(eval VERSION := $(call get_version))
	docker run --rm -it $(APP_NAME):$(VERSION) /bin/bash

docker-build:
	$(eval VERSION := $(call get_version))
	docker build \
		--pull \
		--ssh default \
		--tag $(APP_NAME):$(VERSION) \
		--file $(CURDIR)/docker/Dockerfile \
		$(CURDIR)

docker-run:
	$(eval VERSION := $(call get_version))
	docker run \
		-e AWS_ACCESS_KEY_ID=$(AWS_ACCESS_KEY_ID) \
		-e AWS_SECRET_ACCESS_KEY=$(AWS_SECRET_ACCESS_KEY) \
		--rm -it $(APP_NAME):$(VERSION) \
		./code/bin/example.sh 10

docker-test: docker-build
	$(eval VERSION := $(call get_version))
	docker run --rm -it $(APP_NAME):$(VERSION) /bin/bash -c "pip install -r dev-requirements.txt && pytest /code/tests"

docker-clean:
	docker container prune --force
	docker system prune --force

docker-push:
	$(eval VERSION := $(call get_version))
	@echo 'publish $(VERSION) to $(DOCKER_REPO)'
	docker push $(DOCKER_REPO)/$(APP_NAME):$(VERSION)

clean:
	rm -rf `find . -name __pycache__`
	rm -f `find . -type f -name '*.py[co]' `
	rm -f `find . -type f -name '*~' `
	rm -f `find . -type f -name '.*~' `
	rm -rf `find . -type d -name '*.egg-info' `
	rm -rf `find . -type d -name '*.db' `
	rm -rf `find . -type d -name '.tox' `
	rm -rf `find . -type d -name 'pip-wheel-metadata' `
	rm -rf .cache .pytest_cache .mypy_cache
	rm -rf .coverage .coverage.* htmlcov
	rm -rf *.egg-info build dist
