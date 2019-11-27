# pygrader
Simple Python Grader based on Django

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

## Author
Sarun Gulyanon