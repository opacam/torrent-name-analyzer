# torrent-name-analyzer

[![CI](https://github.com/opacam/torrent-name-analyzer/workflows/CI/badge.svg?branch=develop)](https://github.com/opacam/torrent-name-analyzer/actions)
[![codecov](https://codecov.io/gh/opacam/torrent-name-analyzer/branch/develop/graph/badge.svg?token=C65WnnEqQw)](https://codecov.io/gh/opacam/torrent-name-analyzer)
[![Python versions](https://img.shields.io/badge/Python-3.6+-brightgreen.svg?style=flat)](https://www.python.org/downloads/)
[![GitHub release](https://img.shields.io/github/release/opacam/torrent-name-analyzer.svg)](https://gitHub.com/opacam/torrent-name-analyzer/releases/)
[![GitHub tag](https://img.shields.io/github/tag/opacam/torrent-name-analyzer.svg)](https://gitHub.com/opacam/torrent-name-analyzer/tags/)
[![GitHub license](https://img.shields.io/github/license/opacam/torrent-name-analyzer.svg)](https://github.com/opacam/torrent-name-analyzer/blob/master/LICENSE.md)


A REST api to extract all possible media information from a torrent
filename.

## Getting Started

These instructions will get you a copy of the project up and running on your
local machine for development and testing purposes. See deployment for notes on
how to deploy the project on a live system.

### Prerequisites

You also need python >= 3.6 up and running. If you OS does not have the
appropriate python version, you could install [pyenv](https://github.com/pyenv/pyenv) 
and create a virtual environment with the proper python version. Also you will
need an up to date pip installation (version `20.0.2` or greater is our
recommendation). So once you have `pyenv` installed
(see [pyenv install instructions](https://github.com/pyenv/pyenv#installation)), 
make an virtual environment for the project (we will use python version 3.8):

```
pyenv virtualenv 3.8.1 tna-venv
```

Enter inside the python environment we recently created (`tna-venv`):
```
pyenv activate tna-venv
```

Upgrade `pip` package:
```
pip install --upgrade pip
```

Install `poetry` package:
```
pip install poetry
```

### Installing

Once you have the prerequisites installed, you can proceed installing the
project. The project uses an `pyproject.toml` file to manage the installation
(PEP517) and also we will make use of the python package
[poetry](https://github.com/python-poetry/poetry) as our `build-system`
(PEP518). So, to do the install you only need to `cd` to the
project folder:

```
cd torrent-name-analyzer
```

And run the install of the dependencies via `poetry` command:

```
poetry install
```


## Running the tests

To run our project tests you can use `pytest` with coverage:

```
BOILERPLATE_ENV=test PYTHONPATH=. pytest tests/ --cov torrent_name_analyzer/
```

## Docker

This project can be used via docker, the following sections describes
the build/run instructions.

### Build image

You can build the docker image with the command:

```
docker build -t torrent-name-analyzer:latest .
```

---
**TIP**

To update requirements.txt file you can use:

```
poetry export -f requirements.txt -o requirements.txt
```

---

## Run image

To run the image without persistent database changes, use command:

```
docker run --rm torrent-name-analyzer
```

To run the image with persistent database changes, you can mount a
volume inside docker image pointing to host's database folder with
command:

```
docker run --rm -v <absolute-path-to-db-data>:/app/torrent_name_analyzer/db-data torrent-name-analyzer
```

## Deploy Application Locally

You can deploy application locally using multiple configurations, but
if you want the production mode, we recommend to use a wsgi server, we
make use of `gunicorn` for such purpose, so to run it from the root
of the project use:

```
BOILERPLATE_ENV=prod gunicorn --bind 0.0.0.0:5000 torrent_name_analyzer.wsgi:app
```

For developing purposes (don't recommend this method in a production
environment), you can use the flask wsgi integrated server:

```
PYTHONPATH=. ./torrent_name_analyzer/app.py
```

Just noting that if you don't set `BOILERPLATE_ENV` environment variable
it will default to `dev`.

Here you have all supported configurations:

- dev: To be used when developing
- test: to perform the tests
- prod: to use in a production environment

### List of endpoints:

Endpoint to get the web site:

```
http://localhost:5000/
```

Endpoint to get the json response for all stored torrents:

```
http://localhost:5000/v1/torrents
```

Endpoint to to the swagger documentation, where you can check all the
supported endpoints:

```
http://localhost:5000/v1/ui/
```

## Deploy Application on Heroku

First of all we will use some services:
  - Install heroku app, after creating an [heroku account](https://signup.heroku.com/):

    ```
    curl https://cli-assets.heroku.com/install.sh | sh
    ```

*Under construction*


## Built With

* [Python 3](https://docs.python.org/3/) - The programming language
* [Flask](https://flask.palletsprojects.com/en/1.1.x/) - A lightweight WSGI web application framework
* [Connexion](https://connexion.readthedocs.io/en/latest/) - Framework on top of Flask that automagically handles HTTP requests defined using OpenAPI
* [Gunicorn](https://gunicorn.org/#docs/) - A Python WSGI HTTP Server for UNIX
* [Poetry](https://python-poetry.org/docs/) - Dependency Management

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of
conduct, and the process for submitting pull requests to us.

## Versioning

We use [CalVer](https://calver.org/) for versioning. For the versions available,
see the [tags on this repository](https://github.com/opacam/torrent-name-analyzer/tags).


## Authors

* **Pol Canelles** - *API work and updates on top of Giorgio's work* - [opacam](https://github.com/opacam)
* **Giorgio Momigliano** - *Updates on top of Roi's work* - [platelminto](https://github.com/platelminto)
* **Roi Dayan** - *Updates on top of Divij's work* - [roidayan](https://github.com/roidayan)
* **Divij Bindlish** - *Initial work made with python* - [divijbindlish](https://github.com/divijbindlish)
* **Jānis** - *Original idea made with javascript* - [jzjzjzj](https://github.com/jzjzjzj)

See also the list of [contributors](https://github.com/opacam/torrent-name-analyzer/contributors)
who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* [Template for README.md](https://gist.github.com/PurpleBooth/109311bb0361f32d87a2)
