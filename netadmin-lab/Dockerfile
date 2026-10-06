FROM python:3.11-alpine

RUN apk add --no-cache iputils

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

RUN echo "TUGA{k0mut_3nj3ks1y0nu_v3_r00t_3r1s1m1}" > /flag2.txt

EXPOSE 5000

CMD ["python", "app.py"]
