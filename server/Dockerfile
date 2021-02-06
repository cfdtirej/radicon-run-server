FROM python:3.8

WORKDIR /usr/src

RUN apt-get update && apt-get install -y vim

COPY ./requirements.txt /usr/src

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8

EXPOSE 5000

CMD ["python", "app.py"]