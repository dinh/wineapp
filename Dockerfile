FROM python:3.10-slim-bullseye

WORKDIR /wine

COPY requirements.txt /wine
RUN python -m pip install --upgrade pip && pip install --no-cache-dir --upgrade -r requirements.txt

COPY app /wine/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "9090"]