FROM python:3.10.5-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 7000

CMD ["gunicorn", "--bind", "0.0.0.0:7000", "main:app"]