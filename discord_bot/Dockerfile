FROM python:3.11-slim

WORKDIR /src

RUN pip install uv

COPY requirements.txt .

RUN uv add -r requirements.txt

COPY ./app ./app

CMD ["python", "-m", "app.main"]

