FROM python:3.11-slim

RUN apt-get update && apt-get install -y python3-dev gcc libc-dev

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN pip install --upgrade pip

ADD requirements.txt /app/
RUN pip install -r requirements.txt


RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libjpeg-dev \
    zlib1g-dev && \
    pip install Pillow && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*


COPY . /app
EXPOSE 8000
RUN mkdir -p /vol/app/static && \
    mkdir -p /vol/app/media
RUN chmod +x /app/server-entrypoint.sh
RUN chmod +x /app/worker-entrypoint.sh
RUN chmod +x /app/beat-entrypoint.sh
