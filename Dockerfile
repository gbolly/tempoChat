FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

ENV PYTHONUNBUFFERED=1

CMD ["gunicorn", "tempoChat.asgi:application", "--bind", "0.0.0.0:8000"]
