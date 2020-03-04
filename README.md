# pygrader
Simple Python Grader based on Django.

### Features
* Simple CPU and memory limitation using [resources](https://docs.python.org/3/library/resource.html)
* Asynchronous grading using Celery + Redis
* Upload test cases of the problem as zip file (a zip file containing only input and output folders, look at `test_data/stone_pile.zip` as an example)

----
## Production Workflow
`Django` serves the web application. `Celery`, an open source asynchronous task queue, has workers that concurrently performs the grading. They fetches the task (submission) from the message queue to grade. The message queue is provided by `redis`. The `PostgreSQL` database stores the set of `problems` and `submissions`, where `Adminer` is a database management tool. To deploy `Django`, `Gunicorn` is used as a WSGI HTTP server. It is best to use `Gunicorn` behind an HTTP proxy server, `nginx`.

The configuration will be wrapped in the `docker` so the grader can be up and running by typing:
```
docker-compose -f docker-compose.prod.yml up -d --build
```

To stop the docker, type
```
docker-compose down -v
```

----
## Development Workflow
`Django` serves the web application. `SQLite` database is used. To start the web application, type this command (in pygrader/):
```
python manage.py runserver 0.0.0.0:8000
```

`Celery` workers fetches the submission to grade from the message queue, provided by `redis`. To run `redis` through docker, use this command (make sure to install [docker](https://docs.docker.com/install/) first):
```
docker run --name redis -p 6379:6379 -d redis:alpine
```

Then, start a celery worker (in pygrader/):
```
celery -A pygrader worker -l info
```
It is a good idea to run in the virual environment and install all the requirements first
```
pip install -r requirements.txt
```

----
## To-Do
* Setup Django for production/deployment
* Fix resource limitation (right now it use inaccurate amount of CPU and memory)
* Write installation manual
* Add tooltip/tutorial in admin for uploading new problem
* User's code validation when uploading
* Try Docker version (have problems with limiting resources both CPU and memory)

----
## Author
Sarun Gulyanon