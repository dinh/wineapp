# builder stage
FROM python:3.10-alpine3.15 AS builder

WORKDIR /app

COPY requirements.txt .

RUN apk add --no-cache build-base \
    && python -m venv /venv \
    && /venv/bin/pip install --upgrade pip \
    && /venv/bin/pip install --no-cache-dir --upgrade -r requirements.txt

COPY app app

# production stage
FROM python:3.10-alpine3.15

WORKDIR /app

COPY --from=builder /venv /venv
COPY --from=builder /app/app app

CMD ["/venv/bin/uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "9090"]
