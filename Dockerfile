FROM python:3.9
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt

RUN pip install Flask==2.2.2 mariadb==1.0.11

COPY ./app /code/app
COPY ./static /code/static
COPY run.py /code/

CMD ["python", "run.py"]