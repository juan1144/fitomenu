SHELL := /bin/bash
.SHELLFLAGS := -eu -o pipefail -c
MAKEFLAGS += --no-builtin-rules
#MAKEFLAGS += --warn-undefined-variables

PROJECT_ROOT := $(shell basename ${PWD})
VENV := venv
PYTHON := $(VENV)/bin/python

BOLD := \033[1m
RED := \033[31m
GREEN := \033[32m
YELLOW := \033[33m
BLUE := \033[34m
RESET := \033[0m

.DEFAULT_GOAL := help

.PHONY: help
help:  ## Show this help
	@grep -Eh '\s##\s' $(MAKEFILE_LIST) | \
	awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# ------------------:  ## virtual environment ------------------------------------------
# Todo: use pip

# ------------------:  ## django -------------------------------------------------------
migrations:  ## Make migrations for all apps
	$(PYTHON) manage.py makemigrations

migrate:  ## Run migrations for all apps
	$(PYTHON) manage.py migrate

checkmigrations:  ## Check migrations without running them
	$(PYTHON) manage.py makemigrations --check --no-input --dry-run

superuser:  ## Create a super user
	$(PYTHON) manage.py createsuperuser

run:  ## Run the Django server
	$(PYTHON) manage.py runserver

messages:  ## Collect messages to be translated from the source code
	$(PYTHON) manage.py makemessages -l es

translate:  ## Compile translated messages
	$(PYTHON) manage.py compilemessages -l es

statics:  ## Collect statics (for production)
	$(PYTHON) manage.py collectstatic

clearcache:
	$(PYTHON) manage.py shell \
	--command="from django.core.cache import cache; cache.clear()"

shell:  ## Start the Python interactive interpreter
	$(PYTHON) manage.py shell

celery:  ## Start the celery beat service
	celery -A config.celery worker -l INFO

beat:  ## Start the celery beat service
	celery -A config.celery beat -l INFO


# ------------------:  ## misc ---------------------------------------------------------
dockerup:  ## Start the docker stack
	docker compose up -d

dockerstop:  ## Start the docker stack
	docker compose stop

pcupdate:  ## Update pre-commit hooks
	pre-commit autoupdate
