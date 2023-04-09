# python-project

A Python project for the course Advanced Programming with Python.

## Group members

Name                |    ID    |       GitHub Profile
--------------------|----------|-----------------------------
Dao Tuyet Ngan      | BI12-311 | https://github.com/Peachy72
Nguyen Pham Quoc An | BI12-009 | https://github.com/j1nxie
Nguyen Le Minh Duc  | BI12-092 | https://github.com/menhhduc
Nguyen The Kien     | BI12-225 | https://github.com/Delnegend
Dao Duy Manh Ha     | BI12-141 | https://github.com/R1verrrr

## Requirements

- Python 3.10+.
- Dependencies: `pipenv`, `typing_extensions`, `option`, `pymongo`, `pydantic`.
- MongoDB: you can either use an Atlas instance or a locally installed instance.

## Usage

This repository uses `pipenv` to manage its dependencies and Python interpreter.
If you don't already have `pipenv` installed:

```shell
$ pip install --user pipenv
```

Afterwards, you can automatically setup the virtual environment by running:

```shell
$ pipenv install
```

Everything else can be ran under the environment managed by `pipenv` by:

```shell
$ pipenv run <command>
```

Fill out `.env` using `.env.example` as a base.

Afterwards, either use:

```shell
$ pipenv run python main.py
```

or:

```shell
$ pnpm launch
```

to start the program.

## Contributing

Check out the [Contributing Guide](CONTRIBUTING.md) to get started.
