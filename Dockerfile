# ========= BUILD STAGE =========

FROM python:3.10 AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps -r requirements.txt -w /wheels

# ========= RUNTIME STAGE =========

FROM python:3.10-slim

WORKDIR /app

COPY --from=builder /wheels /wheels
RUN pip install --no-cache /wheels/*

COPY . .

EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
