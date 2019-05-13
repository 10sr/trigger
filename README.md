trigger
=======

Push bullets to pushbullet



Run
---

    make migrate
    TRIGGER_SUPERUSER_PASSWORD=XXX make create_admin
    make runserver


### Run Locally

Create file like:

    TRIGGER_PUSHBULLET_TOKEN=XXX
    TRIGGER_SUPERUSER_PASSWORD=YYY
    TRIGGER_ENV=local




Run with Docker
---------------

    make docker-build
    make docker-run

