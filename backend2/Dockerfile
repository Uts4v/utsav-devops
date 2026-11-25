# ---- Stage 1: builder ----
FROM python:3.11-slim AS builder

WORKDIR /app

RUN python -m venv /opt/venv
ENV PATH=/opt/venv/bin:$PATH

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---- Stage 2: final runtime image ----
FROM python:3.11-slim

WORKDIR /app

COPY --from=builder /opt/venv /opt/venv
ENV PATH=/opt/venv/bin:$PATH

RUN useradd --create-home --uid 10001 app && chown -R app:app /app
COPY --chown=app:app app.py .

USER app

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--access-logfile", "-", "--error-logfile", "-", "app:app"]
