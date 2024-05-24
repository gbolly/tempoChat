FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN chmod +x build.sh
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

ENV PYTHONUNBUFFERED=1


CMD ["./build.sh", "gunicorn", "tempoChat.asgi:application", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
