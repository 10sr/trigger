TRIGGER_PORT ?= 8900
TRIGGER_SQLITE3 ?= $(CURDIR)/db.sqlite3
export TRIGGER_SQLITE3

pipenv := pipenv
python3 := $(pipenv) run python3


run:
	$(python3) manage.py runserver $(TRIGGER_PORT)
