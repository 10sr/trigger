TRIGGER_PORT ?= 8980
# 0.0.0.0 is required when run inside of docker container
TRIGGER_HOST ?= 0.0.0.0

pipenv := pipenv
python3 := $(pipenv) run python3

npm := npm


# FIXME: Pass mypy check
check: app-test check-format # check-type

installdeps:
	$(pipenv) install --dev --deploy
	yes | $(pipenv) run mypy --install-types
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



# Formatter and Linter ##################

# TODO: Use flake8

# FIXME: Pass pydocstyle
check-format: black-check isort-check  # pydocstyle

# black

black:
	$(pipenv) run black .

black-check:
	$(pipenv) run black --check .

# isort

isort:
	$(pipenv) run isort trigger proj

isort-check:
	$(pipenv) run isort trigger proj -c -v

# pydocstyle

pydocstyle:
	$(pipenv) run pydocstyle .



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
