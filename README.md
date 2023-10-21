# Initialize

## Install packages

```shell
python -m pip install pipenv
```
```shell
pipenv install
```
```shell
pipenv sehll
```

## Prepare Develop Environment

```shell
export FLASK_ENV=development
```
```shell
export FLASK_DEBUG=1
```
```shell
export FLASK_APP=urlshort
```

## Start Dev

```shell
flask run
```


## Start Prod

```shell
gunicorn "urlshort:create_app()" -b 0.0.0.0
```
