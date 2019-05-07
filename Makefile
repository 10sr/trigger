-include env.secret

TRIGGER_ENV ?= local
TRIGGER_PORT ?= 8900
# 0.0.0.0 is required when run inside of docker container
TRIGGER_HOST ?= 0.0.0.0
TRIGGER_SQLITE3 ?= $(CURDIR)/db.sqlite3
export TRIGGER_ENV
export TRIGGER_SQLITE3
export TRIGGER_PUSHBULLET_TOKEN
export SUPERUSER_PASSWORD

pipenv := pipenv
python3 := $(pipenv) run python3

npm := npm


check: app-test check-format check-type

installdeps:
	$(pipenv) install --dev --deploy
	$(npm) install


runserver-viamanager: create_superuser
	$(python3) manage.py $@ "$(TRIGGER_HOST):$(TRIGGER_PORT)"

runserver: create_superuser
	$(pipenv) run gunicorn \
		--bind "$(TRIGGER_HOST):$(TRIGGER_PORT)" \
		--workers 2 \
		--log-level debug \
		--reload \
		proj.wsgi:application

migrate:
	$(python3) manage.py $@

create_superuser:
	$(python3) manage.py $@

app-test:
	$(python3) manage.py makemigrations --dry-run --check
	$(python3) -Wa manage.py test


# Docker ###################

docker-build:
	docker build . -t local/trigger

docker-run: docker-stop
	docker run \
		--name trigger01 \
		--rm \
		-p '$(TRIGGER_PORT):$(TRIGGER_PORT)' \
		--env-file env.secret \
		local/trigger

docker-stop:
	docker stop trigger01 || true



# Formatter ##################

check-format: black-check isort-check

# black

black:
	$(pipenv) run black .

black-check:
	$(pipenv) run black --check .

# isort

isort:
	$(pipenv) run isort -rc trigger proj

isort-check:
	$(pipenv) run isort -rc trigger proj -c -vb



# Type Checks #################

check-type: mypy
# check-type: mypy pyright pyre pytype

mypy:
	$(pipenv) run mypy --config-file .mypy.ini -p trigger -p proj -p tests
# TODO: This really works?
#	$(poetry) run mypy --config-file .mypy.ini .

pyright:
	$(npm) run -- pyright -p .

pyre:
	$(pipenv) run pyre check

pytype:
	$(pipenv) run pytype --config=./.pytype.cfg trigger proj tests
