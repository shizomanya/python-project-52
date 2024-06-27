MANAGE := poetry run python manage.py
lint:
	poetry run flake8 task_manager

test:
	poetry run coverage run manage.py test .test


test-coverage:
	make test
	poetry run coverage xml
	poetry run coverage report

install:
	poetry install

selfcheck:
	poetry check

check: selfcheck test-coverage lint

dev:
	poetry run python manage.py runserver

migrate:
	poetry run python manage.py makemigrations
	poetry run python manage.py migrate

PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) task_manager.wsgi

shell:
	poetry run python manage.py shell_plus --ipython

makemessages:
	django-admin makemessages --ignore="static" --ignore=".env" -l ru

compilemessages:
	django-admin compilemessages
