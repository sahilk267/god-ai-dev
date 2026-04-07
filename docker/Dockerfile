FROM python:3.11-slim as builder

WORKDIR /app
COPY requirements.txt .

RUN apt-get update && apt-get install -y gcc portaudio19-dev
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.11-slim

WORKDIR /app
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY backend/ ./backend/
COPY workspace/ ./workspace/

ENV PYTHONPATH=/app
EXPOSE 8000

CMD ["gunicorn", "backend.api.routes:app", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]