#dockerfile, docker image, docker container
FROM python:3.9

ADD main.py .

RUN pip install flask

CMD ["python", "./main.py"]