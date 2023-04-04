FROM python:3.11-slim-buster
RUN \
    apt-get update --allow-unauthenticated \
    && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /

# Dependencies
ENV PYTHONPATH=.
COPY requirements.txt requirements.txt
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt
COPY . .
