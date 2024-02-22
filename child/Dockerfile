FROM python:3.12-slim-bullseye

RUN mkdir -p /app/files

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]