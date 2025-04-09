FROM python:3.10-slim

# 安装构建 numpy wheel 所需的基本依赖
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    build-essential \
    python3-dev \
    libatlas-base-dev \
    gfortran \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app

# 升级 pip + setuptools + wheel，强制安装 numpy
RUN pip install --upgrade pip setuptools wheel

# 👇 关键点：单独提前装 numpy，避免它参与 pyproject.toml 编译
RUN pip install "numpy==1.23.5" --no-deps

# 然后再装其他依赖
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install "numpy==1.23.5" --no-deps

# ✅ 依赖健康检查
RUN python -c "from deepface import DeepFace; import cv2; print('✅ all dependencies loaded')"

EXPOSE 5000
CMD ["python", "app/main.py"]

