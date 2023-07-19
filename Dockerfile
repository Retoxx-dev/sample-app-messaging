FROM python:3.9

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY app/ ./app/

WORKDIR /app

CMD ["python", "main.py"]