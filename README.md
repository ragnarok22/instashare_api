# InstaShare API
InstaShare API

![Django CI](https://github.com/ragnarok22/instashare_api/actions/workflows/django-test.yml/badge.svg)
![Codecov](https://img.shields.io/codecov/c/github/ragnarok22/instashare_api)
[![GitHub license](https://img.shields.io/github/license/ragnarok22/instashare_api)](https://github.com/ragnarok22/instashare_api/blob/main/LICENSE)
![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/ragnarok22/instashare_api)
![GitHub repo size](https://img.shields.io/github/repo-size/ragnarok22/instashare_api)
![GitHub commit activity](https://img.shields.io/github/commit-activity/w/ragnarok22/instashare_api)

## License
Distributed under the terms of the [MIT](LICENSE) license.

## Running in development mode
This project was built using:
- [Python](https://python.org)
- [Django](https://djangoproject.com)
- [Django Rest Framework](https://django-rest-framework.org)
- [Docker](https://docker.com)
- [Poetry](https://python-poetry.org) (not required)

### create an isolation environment

(This step is not required if you use poetry)

```shell
python -m venv .venv
```

### install dependencies

```shell
pip install .
```

or use poetry:

```shell
poetry install
```

### Activate the local environment

```shell
source .venv/bin/activate
```

or use poetry:

```shell
poetry shell
```

Then run the development server

```shell
python manage.py runserver
```

## Deploy

This project uses [Docker](https://www.docker.com) for deployment

### environment variables

You must create .env file with the next variables:

- `DJANGO_SETTINGS_MODULE`: project settings. (set `config.settings.develop`).
- `SECRET_KEY`: used to provide cryptographic signing.
- `DB_HOST`: postgres database host.
- `DB_PORT`: postgres database port.
- `DB_USER`: postgres database user.
- `POSTGRES_PASSWORD`: postgres database password.
- `POSTGRES_DB`: postgres database name.
- `ALLOWED_HOSTS`: A list of strings representing the host/domain names that this Django site can serve.
- `REDIS_URL`: The redis url. (Ex: redis://localhost:6379)

[Here](.env-example) you have an example

### deploy the application

You must have installed Docker and Docker Compose to run the application:

```shell
docker-compose up -d
```

### Set Nginx

Here set an example for a nginx configuration and with the certbot to manage the ssl.
This project is set to only run in secure protocol (https)

    server {
        server_name instashare-api.ragnarok22.dev;

        location / {
            proxy_pass http://localhost:8000;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header Host $host;
            proxy_redirect off;
        }

        listen [::]:443 ssl ipv6only=on; # managed by Certbot
        listen 443 ssl; # managed by Certbot
        ssl_certificate /etc/letsencrypt/live/instashare-api.ragnarok22.dev/fullchain.pem; # managed by Certbot
        ssl_certificate_key /etc/letsencrypt/live/instashare-api.ragnarok22.dev/privkey.pem; # managed by Certbot
        include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
        ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot
    }

    server {
        if ($host = instashare-api.ragnarok22.dev) {
            return 301 https://$host$request_uri;
        } # managed by Certbot

        listen 80;
        listen [::]:80;

        server_name instashare-api.ragnarok22.dev;
        return 404; # managed by Certbot
    }

## Running tests
For running test

```
coverage run manage.py test apps
coverage report
```

## API Documentation
Run the project:

```shell
python manage.py runserver
```
And then go to http://localhost:8000/docs/
