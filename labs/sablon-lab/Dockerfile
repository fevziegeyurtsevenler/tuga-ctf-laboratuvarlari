# Küçük, hızlı ayağa kalkan bir imaj. Kendi labında farklı bir taban kullanabilirsin.
FROM python:3.12-slim

WORKDIR /uygulama
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .

EXPOSE 8080
CMD ["python", "app.py"]
