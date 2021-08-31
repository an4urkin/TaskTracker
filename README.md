### TaskTracker is a task management web app written with Django REST.

- Allows to define a task with name, description, creation date, state and priority.
- Task description can be updated.
- Task state can be changed with any of (TODO, READY, IN PROGRESS, COMPLETED).
- Task can be automatically rejected (deleted) if it's not started in configurable amount of time.
- Tasks can be sorted by all applicable fields.

### Requirements

- Python 3.9.6
- Django 3.2.6 and other dependencies from the `requirements.txt`

### Install&Run
- Clone repo
- Run virtual environment:
```
pip install --user pipenv
pipenv shell
```
- Install dependencies:
```
pip install -r requirements.txt
```
- Create database:
```
python3 manage.py makemigrations
python3 manage.py migrate
```
- Create admin:
```
python3 manage.py createsuperuser
```
- Run:
```
python3 manage.py runserver
```
### For scheduled rejection of tasks:
- Install and start RabbitMQ service
- Run celery worker in separate command line (Windows):
```
celery -A apis worker -l info -P gevent
```
- Run celery scheduler in another separate command line:
```
celery -A apis beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
```
### Access the app

You can acess Browsable API via http://127.0.0.1:8000/apis/v1/tasks
