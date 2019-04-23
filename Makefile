-include env.secret

TRIGGER_PORT ?= 8900
TRIGGER_SQLITE3 ?= $(CURDIR)/db.sqlite3
export TRIGGER_SQLITE3
export TRIGGER_PUSHBULLET_TOKEN

pipenv := pipenv
python3 := $(pipenv) run python3


runserver:
	$(python3) manage.py $@ $(TRIGGER_PORT)

migrate:
	$(python3) manage.py $@
