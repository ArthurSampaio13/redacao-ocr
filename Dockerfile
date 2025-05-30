FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app/

RUN pip install --no-cache-dir -e .

EXPOSE 8000

CMD ["uvicorn", "redacao_detector.api.main:app", "--host", "0.0.0.0", "--port", "8000"]