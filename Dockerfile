FROM python:3.14-slim

RUN apt-get update && apt-get install -y curl build-essential \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /app

COPY ./supra ./supra
COPY ./frontend ./frontend

RUN pip install --upgrade pip
RUN pip install -r supra/requirements/universal.txt

WORKDIR /app/frontend
RUN npm install

WORKDIR /app/supra

CMD bash -c "\
    python manage.py makemigrations && \
    python manage.py migrate && \
    python manage.py initialization && \
    python manage.py runserver 0.0.0.0:8000 & \
    cd ../frontend && npm start & \
    wait \
"