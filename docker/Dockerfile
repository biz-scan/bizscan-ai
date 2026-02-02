FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml ./
COPY uv.lock ./

RUN pip install --no-cache-dir uv \
  && uv sync --frozen

COPY app ./app

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]