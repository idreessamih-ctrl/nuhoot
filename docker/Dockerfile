FROM python:3.12-slim AS builder

WORKDIR /build
COPY pyproject.toml ./
RUN pip install --no-cache-dir build && pip wheel --no-cache-dir -w /wheels .

FROM python:3.12-slim

RUN useradd -m -s /bin/bash nuhoot

WORKDIR /app
COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir /wheels/*.whl && rm -rf /wheels

COPY --chown=nuhoot:nuhoot . .
USER nuhoot

EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "nuhoot.main:app", "--host", "0.0.0.0", "--port", "8000"]
