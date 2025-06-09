FROM python:3.11-slim

WORKDIR /app
COPY IDPLig_app/ /app
RUN pip install --no-cache-dir -r requirements.txt


CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"]
