trigger
=======

Push bullets to pushbullet



Run
---

Copy `settings_local.toml` to `settings.toml` and edit that file, then

    make migrate
    make create_superuser
    make runserver



Run with Docker
---------------

    make docker-build
    make docker-run

