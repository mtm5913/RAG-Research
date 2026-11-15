FROM python:3.13-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY app /app/app
COPY scripts/ask-photography.py /app/scripts/ask-photography.py
COPY docs/public/photography-evaluation-round-3.json /app/docs/public/photography-evaluation-round-3.json
COPY .local-corpus.json /app/.local-corpus.json
EXPOSE 8765
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8765/healthz', timeout=3)"
CMD ["python", "app/server.py", "--live", "--bind", "0.0.0.0", "--port", "8765", "--public-host", "fieldlight.megan373lab.xyz", "--noninteractive"]
