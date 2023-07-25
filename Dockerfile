FROM python:3.9-slim

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY app/ ./app/

WORKDIR /app

EXPOSE 80

CMD ["uvicorn app:app --host 0.0.0.0 --port 80"]