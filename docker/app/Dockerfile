# -------------------------------------------------------------------
FROM python:3.12-slim AS builder

WORKDIR /build

RUN apt-get update && apt-get install -y build-essential libpq-dev

COPY pyproject.toml setup.cfg setup.py .
RUN pip install --upgrade pip setuptools wheel

COPY . .
RUN pip wheel --wheel-dir dist/ .[dist]

# -------------------------------------------------------------------
FROM python:3.12-slim

WORKDIR /app

COPY --from=builder /build/dist/*.whl /tmp/
RUN pip install /tmp/*.whl

COPY . .

COPY docker/app/files/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
