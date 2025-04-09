FROM python:3.9-slim

WORKDIR /app

<<<<<<< HEAD
=======
# 安装系统依赖（为 opencv, deepface 等做准备）
RUN apt-get update && apt-get install -y \
    build-essential \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    ffmpeg \
    libgl1 \
    libgtk2.0-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip setuptools wheel
# 复制 requirements.txt 并安装 Python 依赖
>>>>>>> js-2
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install numpy==1.23.5
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"] 
