　　　　　　　　FastAPI Sample
----

FastAPI, SQLAlchemy, Alembic, Graphene, Amazon Cognito

## Install Dependencies

Install the poetry package manager

* https://github.com/python-poetry/poetry

Install the project dependencies:

```shell
$ poetry install
```

## Local Development

Configure environment variable

```sh
$ cp .env.template .env
$ vi .env
```

Enter a poetry shell

```shell
$ poetry shell
```

Migration

```shell
$ alembic upgrade head
```

Run the live server

```shell
$ uvicorn main:app --reload
```

## Build app's DB container image

```sh
$ docker-compose -f docker-compose.yml up -d db
```