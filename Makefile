-include env.secret

# TODO: How to make sure that ENV is actually set to prod on deployment?
TRIGGER_ENV ?= local
TRIGGER_PORT ?= 8900
# 0.0.0.0 is required when run inside of docker container
TRIGGER_HOST ?= 0.0.0.0
TRIGGER_SQLITE3 ?= $(CURDIR)/db.sqlite3
TRIGGER_SECRET_KEY ?=
export TRIGGER_ENV
export TRIGGER_SQLITE3
export TRIGGER_PUSHBULLET_TOKEN
export TRIGGER_SUPERUSER_PASSWORD
export TRIGGER_SECRET_KEY  # Currently this variable is used only when TRIGGER_ENV == prod

pipenv := pipenv
python3 := $(pipenv) run python3

npm := npm


check: app-test check-format check-type

installdeps:
	$(pipenv) install --dev --deploy
	$(npm) install


runserver-viamanager: create_superuser
	$(python3) manage.py runserver "$(TRIGGER_HOST):$(TRIGGER_PORT)"

runserver: create_superuser
	$(pipenv) run gunicorn \
		--bind "$(TRIGGER_HOST):$(TRIGGER_PORT)" \
		--workers 2 \
		--capture-output \
		--enable-stdio-inheritance \
		--access-logfile - \
		--reload \
		proj.wsgi:application

migrate:
	$(python3) manage.py $@

create_superuser:
	$(python3) manage.py $@

app-test:
	$(python3) manage.py makemigrations --dry-run --check
	# TODO: Fix warnings
	# https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/
	TRIGGER_ENV=prod TRIGGER_SECRET_KEY=fakekey $(python3) -Wa manage.py check --deploy
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
