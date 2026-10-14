FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && useradd -u 10001 -m agenda && mkdir /data && chown agenda:agenda /data
COPY --chown=agenda:agenda app.py .
COPY --chown=agenda:agenda templates ./templates
COPY --chown=agenda:agenda static ./static
USER agenda
EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "1", "--threads", "4", "app:app"]
