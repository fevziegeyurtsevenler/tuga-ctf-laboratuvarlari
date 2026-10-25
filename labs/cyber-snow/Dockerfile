# Hafif ve kararlı Python 3.11 taban imajı
FROM python:3.11-slim

# Konteyner içi çalışma dizini
WORKDIR /app

# Gecikmesiz log akışı ve bytecode önbelleğini kapatma
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Önce bağımlılıkları kopyala ve yükle (Docker cache optimizasyonu)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Projenin kalan tüm dosyalarını konteyner içine aktar
COPY . .

# Flask ve Gunicorn için dinlenecek portu belirt
EXPOSE 5000

# Gunicorn ile 4 iş parçacıklı (worker) WSGI sunucusunu 5000 portunda başlat
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app:app"]