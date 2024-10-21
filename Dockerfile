FROM python:3.10-slim

RUN mkdir /app

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

RUN pip uninstall opencv-python -y

RUN pip install opencv-python-headless==4.10.0.84

COPY . .

CMD ["gunicorn", "main:app", "--workers", "1", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
