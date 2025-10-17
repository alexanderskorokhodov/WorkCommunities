FROM python:3.11-slim

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

RUN pip install --no-cache-dir --upgrade pip

# ставим зависимости (локальный файл внутри backend/)
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# копируем исходники
COPY app ./app

# чтобы Python видел пакет
ENV PYTHONPATH=/app

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]