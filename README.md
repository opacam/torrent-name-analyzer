# torrent-name-analyzer

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

To run our project tests you can use `poetry`:

```
poetry run pytest
```


And if you want to run `pytest` with coverage:

```
poetry run pytest --cov . -n 2
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

## Deployment with heroku

First of all we will use some services:
  - Install heroku app, after creating an [heroku account](https://signup.heroku.com/):

    ```
    curl https://cli-assets.heroku.com/install.sh | sh
    ```
  - You also will need a [semaphore account](https://semaphoreci.com/)

Now we can proceed to our deployment, we will use master branch as the
deploy branch and develop to do our tests before deploying the app/api
to production.


## Built With

* [Python 3](https://docs.python.org/3/) - The programming language
* [Flask](https://flask.palletsprojects.com/en/1.1.x/) - A lightweight WSGI web application framework
* [Connexion](https://connexion.readthedocs.io/en/latest/) - Framework on top of Flask that automagically handles HTTP requests defined using OpenAPI
* [Poetry](https://python-poetry.org/docs/) - Dependency Management

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of
conduct, and the process for submitting pull requests to us.

## Versioning

We use [CalVer](https://calver.org/) for versioning. For the versions available,
see the [tags on this repository](https://github.com/opacam/torrent-name-analyzer/tags).


## Authors

* **Pol Canelles** - *Initial work* - [opacam](https://github.com/opacam)

See also the list of [contributors](https://github.com/opacam/torrent-name-analyzer/contributors)
who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* [Template for README.md](https://gist.github.com/PurpleBooth/109311bb0361f32d87a2)
