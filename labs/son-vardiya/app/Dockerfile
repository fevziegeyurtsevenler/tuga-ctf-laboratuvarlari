FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DB_PATH=/data/lab.db

WORKDIR /app

COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/app.py .
COPY app/templates/ templates/
COPY app/static/ static/
COPY database/init.sql .

# Uygulama root olmayan bir kullanıcı ile çalışır (container hijyeni için;
# lab'ın kendi zafiyetlerini etkilemez, sadece container'ın kendisini sağlamlaştırır).
RUN useradd --create-home --uid 1000 appuser \
    && mkdir -p /data \
    && chown -R appuser:appuser /app /data

USER appuser

EXPOSE 5000

CMD ["python", "app.py"]
