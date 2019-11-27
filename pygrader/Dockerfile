FROM python:3.8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_ENV dev

RUN mkdir /code
WORKDIR /code

COPY pygrader/requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/

EXPOSE 8000