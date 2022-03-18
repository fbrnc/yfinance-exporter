FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt /requirements.txt

RUN pip install --no-cache-dir --upgrade pip &&\
    pip install --no-cache-dir --trusted-host pypi.python.org -r /requirements.txt

COPY main.py config.dist.json /app/

CMD ["python", "main.py"]