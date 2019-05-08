FROM python:3

ENV PIPENV_VERSION 2018.11.26

ENV TRIGGER_PORT 8900

WORKDIR /root/app

RUN pip3 install pipenv==$PIPENV_VERSION

COPY Pipfile Pipfile.lock ./
RUN env -u PIPENV_VERSION pipenv install --deploy # --system

COPY trigger trigger
COPY proj proj
COPY Makefile manage.py ./

EXPOSE $TRIGGER_PORT

# TODO: Pass via build argument
#RUN git rev-parse HEAD >git_commit_hash.txt

# Django not work without this!
ENV PYTHONUNBUFFERED 1
CMD ["make", "migrate", "create_superuser", "runserver"]
