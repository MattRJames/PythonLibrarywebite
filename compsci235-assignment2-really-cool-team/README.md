# Library Knihovna

It's a library.

## Installation

Unix
```shell
git clone https://github.com/UoA-CS-Urschler-Teaching-CS235-S1-2021/compsci235-assignment2-really-cool-team.git
cd compsci235-assignment2-really-cool-team
python -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
```

Windows
```shell
git clone https://github.com/UoA-CS-Urschler-Teaching-CS235-S1-2021/compsci235-assignment2-really-cool-team.git
cd compsci235-assignment2-really-cool-team
python -m venv venv
venv\Scripts\activate.bat
python -m pip install -r requirements.txt
```

This will clone the git repository, create a virtual environment and install all the project's dependencies inside it.

## Environment variables

You can optionally change environment variables inside `.env`.
Change `FLASK_ENV` from `development` to `production` to allow HTTP caching.
Change `REPOSITORY` from `database` to `memory` to use an in-memory non-persistent repository.

## Testing

From the project directory and inside the virtual environment, run this command:
```shell
python -m pytest -v tests
```

To test the database repository, run:
```shell
python -m pytest -v tests_db
```

## Running

From the project directory and inside the virtual environment, run this command:

```shell
flask run
```

A webserver will be spawned and the website will be accessible at `http://127.0.0.1:5000`.
