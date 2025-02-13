FROM python:3.11-slim

# フォントパッケージのインストール
RUN apt-get update && \
    apt-get install -y fonts-noto-cjk && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# CMD ["python", "generate_image.py"]
