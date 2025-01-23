FROM python:3.11-slim-bookworm

WORKDIR /app

COPY ./src/* .
RUN pip install -r requirements.txt

ENTRYPOINT [ "python", "main.py" ]
