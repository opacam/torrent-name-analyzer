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

ENV FLASK_APP=torrent_name_analyzer.app
ENV FLASK_ENV=development
ENV FLASK_DEBUG=1

# First we install the dependencies from requirements.txt
WORKDIR /tmp
COPY requirements.txt /tmp
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy in everything else:
WORKDIR /app
COPY . /app/
RUN pip install .

EXPOSE 5000

ENTRYPOINT ["flask", "run", "--host", "0.0.0.0", "--port", "5000"]
