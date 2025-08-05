FROM python:3.12-slim as builder

WORKDIR /app

COPY bot bot
COPY db db
COPY utils utils

RUN pip install --no-cache-dir -e bot/
RUN pip install --no-cache-dir -e db/
RUN pip install --no-cache-dir -e utils/

FROM python:3.12-slim

WORKDIR /app
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/bot/src:$PYTHONPATH

COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /app /app

CMD ["python", "bot/src/main.py"]