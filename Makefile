
pipenv := pipenv
python3 := $(pipenv) run python3

PORT := 8900

run:
	$(python3) manage.py runserver $(PORT)
