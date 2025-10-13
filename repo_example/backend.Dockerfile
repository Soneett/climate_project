FROM python:3.12-slim

RUN mkdir /app
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./models ./models
COPY ./tables ./tables
COPY ./repo ./repo
COPY ./routers ./routers

COPY database.py .
COPY settings.py .
COPY app.py .


EXPOSE 8080

ENTRYPOINT ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]