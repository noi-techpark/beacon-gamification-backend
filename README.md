# beacon-gamification-backend

Backend code for the beacon project.

## Table of contents

- [Gettings started](#getting-started)
- [Running tests](#running-tests)
- [Deployment](#deployment)
- [Docker environment](#docker-environment)
- [Information](#information)

## Getting started

These instructions will get you a copy of the project up and running
on your local machine for development and testing purposes.

### Prerequisites

To build the project, the following prerequisites must be met:

- Python 3.6 and up

### Source code

Get a copy of the repository:

```bash
git clone https://github.com/noi-techpark/beacon-gamification-backend.git
```

Change directory:

```bash
cd beacon-gamification-backend/
```

### Install python dependencies

Create a virtualenv:

```bash
python3 -m venv env
```

Activate the virtualenv:

```bash
source env/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### Development

After the installation of dependencies you can follow the [Django documentation](https://docs.djangoproject.com/en/2.2/).
Use the standard development server with `python project/manage.py runserver`.

## Deployment

ToDo: A detailed description about how the application must be deployed.

## Docker environment

For the project a Docker environment is already prepared and ready to use with all necessary prerequisites.

These Docker containers are the same as used by the continuous integration servers.

### Installation

Install [Docker](https://docs.docker.com/install/) (with Docker Compose) locally on your machine.

### Start and stop the containers

Before start working you have to start the Docker containers:

```
docker-compose up --build --detach
```

After finished working you can stop the Docker containers:

```
docker-compose stop
```

### Running commands inside the container

When the containers are running, you can execute any command inside the environment. Just replace the dots `...` in the following example with the command you wish to execute:

```bash
docker-compose exec app /bin/bash -c "..."
```

Some examples are:

```bash
docker-compose exec app /bin/bash -c "python ..."
```

## Information

### Support

ToDo: For support, please contact [info@opendatahub.bz.it](mailto:info@opendatahub.bz.it).

### Contributing

If you'd like to contribute, please follow the following instructions:

- Fork the repository.

- Checkout a topic branch from the `development` branch.

- Make sure the tests are passing.

- Create a pull request against the `development` branch.

A more detailed description can be found here: [https://github.com/noi-techpark/documentation/blob/master/contributors.md](https://github.com/noi-techpark/documentation/blob/master/contributors.md).

### Documentation

More documentation can be found at [https://opendatahub.readthedocs.io/en/latest/index.html](https://opendatahub.readthedocs.io/en/latest/index.html).

### License

The code in this project is licensed under the GNU AFFERO GENERAL PUBLIC LICENSE Version 3 license. See the [LICENSE.md](LICENSE.md) file for more information.
