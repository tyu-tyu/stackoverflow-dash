#dockerfile, docker image, docker container
FROM python:3.9

ADD main.py .
ADD templates /templates
ADD static /static

RUN pip install flask

CMD ["flask","--app","main","run","--host","0.0.0.0","-p","8080"]