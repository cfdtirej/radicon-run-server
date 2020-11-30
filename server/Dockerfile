FROM python:latest

WORKDIR /src

# RUN apt-get update && apt-get upgrade -y

# RUN apt-get install -y vim

COPY ./requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY ./src/ .

EXPOSE 5000

CMD ["python", "app.py"]