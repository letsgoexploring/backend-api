FROM python:3.6-slim-stretch

# Extra python env
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app
CMD ["python", "example.py"]

RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential tk-dev && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --require-hashes --no-cache-dir -r requirements.txt

COPY . ./
