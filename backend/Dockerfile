FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN python3 -m pip install --upgrade pip

RUN pip3 install -r requirements.txt --no-cache-dir

COPY . .

CMD ["gunicorn",  "--bind", "0:8800", "foodgram.wsgi:application"]