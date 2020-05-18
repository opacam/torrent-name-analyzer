# Dockerfile with torrent-name-analyzer installed
#
# Build with:
#   - docker build -t torrent-name-analyzer:latest .
#
# Run with:
#   - docker run -it --rm torrent-name-analyzer
FROM python:3.8.2-slim

LABEL Author="Pol Canelles"
LABEL E-mail="canellestudi@gmail.com"
LABEL version="1.0"

ENV BOILERPLATE_ENV=prod

# First we install the dependencies from requirements.txt
WORKDIR /tmp
COPY requirements.txt /tmp
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy in everything else:
WORKDIR /app
COPY . /app/
RUN pip install .

EXPOSE 5000

CMD gunicorn --worker-class gevent --workers 8 --bind 0.0.0.0:5000 torrent_name_analyzer.wsgi:app --max-requests 10000 --timeout 5 --keep-alive 5 --log-level info
