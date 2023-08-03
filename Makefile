install:
		poetry install

makemigrations:
		python3 manage.py makemigrations

migrate:
		python3 manage.py migrate

start:
		python3 manage.py runserver

lint:
		poetry run flake8 task_manager

test:
		poetry run python3 manage.py test

test-coverage:
		poetry run coverage run manage.py test
		poetry run coverage html
		poetry run coverage report

prep_translations:
		django-admin makemessages --ignore=".env" -l ru

apply_translations:
		django-admin compilemessages
