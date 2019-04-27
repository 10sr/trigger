-include env.secret

TRIGGER_ENV ?= local
TRIGGER_PORT ?= 8900
TRIGGER_SQLITE3 ?= $(CURDIR)/db.sqlite3
export TRIGGER_ENV
export TRIGGER_SQLITE3
export TRIGGER_PUSHBULLET_TOKEN
export SUPERUSER_PASSWORD

pipenv := pipenv
python3 := $(pipenv) run python3

npm := npm


check: app-test black-check mypy pyright pyre

installdeps:
	$(pipenv) install --dev
	$(npm) install


# 0.0.0.0 is required when run inside of docker container
runserver: create_superuser
	$(python3) manage.py $@ 0.0.0.0:$(TRIGGER_PORT)

migrate:
	$(python3) manage.py $@

create_superuser:
	$(python3) manage.py $@

app-test:
	$(python3) manage.py makemigrations --dry-run --check
	$(python3) -Wa manage.py test


###########
# Docker

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



#########
# black

black:
	$(pipenv) run black .

black-check:
	$(pipenv) run black --check .

#########
# mypy

mypy:
	$(pipenv) run mypy --config-file .mypy.ini -p trigger -p proj -p tests
# TODO: This really works?
#	$(poetry) run mypy --config-file .mypy.ini .


###########
# pyright

pyright:
	npm run -- pyright -p .


#########
# pyre

pyre:
	$(pipenv) run pyre check
