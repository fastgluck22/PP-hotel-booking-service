FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VERSION=1.8.2 \
    POETRY_VIRTUALENVS_CREATE=false

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /app

COPY pyproject.toml /app/

RUN pip install --no-cache-dir django django-extensions psycopg2-binary

COPY . /app/

CMD ["python", "src/manage.py", "runserver", "0.0.0.0:8000"]
