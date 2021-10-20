## TaskTracker is a task management web app with JWT-based authenitification, written with Django REST

![This is an image](https://github.com/an4urkin/TaskTracker/blob/master/my_project_visualized_all.png)

- Allows to register a new user and login with user credentials.
- User authentification is required for any actions with the tasks.
- Task can be defined by admin user with name, description, creation date, state, priority and owner.
- Task description can be updated.
- Task state can be user-changed with any of (TODO, IN PROGRESS, READY).
- Setting task state COMPLETED is restricted for admin-only.
- Task is automatically rejected (deleted) if it's not started in configurable amount of time.
- Tasks can be sorted by all applicable fields (id, priority, state, date).

### Requirements

- PostgreSQL 13
- Python 3.9.6
- Django 3.2.6 
- RabbitMQ Server 3.9.3 and other dependencies from the `requirements.txt`

### Install&Run
## Docker
- [Install](https://docs.docker.com/get-docker/) and start Docker service on your system
- Create Docker container:
```
docker-compose up -d --build
```

## Local

- Clone repo
- Start RabbitMQ service
- Launch virtual environment:
```
pip install --user pipenv
pipenv shell
```
- Install dependencies:
```
pip install -r requirements.txt
```
- Create Postgres database
- Specify database access in the `settings.py` like so:
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': <database>,
        'USER': <username>,
        'PASSWORD': <password>,
        'HOST': 'localhost',
        'PORT': '5432',
    }
```
- Apply migrations:
```
python3 manage.py makemigrations
python3 manage.py migrate
```
- Create admin:
```
python3 manage.py createsuperuser
```
- Run the main app:
```
python3 manage.py runserver
```
- Run celery worker in separate command prompt (Windows):
```
celery -A apis worker -l info -P gevent
```
- Run celery scheduler in another separate command prompt:
```
celery -A apis beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
```
- Run listener:
```
python3 recieve_notification.py
```
### Access the app

You can use Postman or access Browsable API via http://127.0.0.1:8000/apis/v1/tasks/

### Run tests

- Launch virtual environment:
```
pipenv shell
```
- Run tests:
```
python3 manage.py test --settings=config.settings
```
