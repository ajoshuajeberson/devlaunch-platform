FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY app.py .

RUN useradd --system --uid 10001 appuser
USER 10001

EXPOSE 8000

CMD ["python", "app.py"]
