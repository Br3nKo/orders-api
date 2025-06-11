FROM python:3.12

WORKDIR /app

RUN apt-get update && apt-get install -y postgresql-client

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

ENV PYTHONPATH=/app

EXPOSE 8000

CMD ["sh", "-c", "until pg_isready -h db -p 5432; do echo 'Waiting for DB...'; sleep 2; done; \
    cd app && alembic upgrade head && \
    uvicorn app.main:app --host 0.0.0.0 --port 8000"]