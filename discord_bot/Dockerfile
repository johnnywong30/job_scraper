FROM python:3.11-slim

WORKDIR /src

RUN pip install uv

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./app ./app

CMD ["python", "-m", "app.main"]

