-include env.secret

TRIGGER_PORT ?= 8900
TRIGGER_SQLITE3 ?= $(CURDIR)/db.sqlite3
export TRIGGER_SQLITE3
export TRIGGER_PUSHBULLET_TOKEN
export SUPERUSER_PASSWORD

pipenv := pipenv
python3 := $(pipenv) run python3


check: black-check


runserver: create_superuser
	$(python3) manage.py $@ $(TRIGGER_PORT)

migrate:
	$(python3) manage.py $@

create_superuser:
	$(python3) manage.py $@




#########
# black

black:
	${pipenv} run black .

black-check:
	${pipenv} run black --check .
