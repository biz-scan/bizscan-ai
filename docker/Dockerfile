FROM python:3.13-slim

WORKDIR /app

# 시스템 패키지 최소
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# uv 설치
RUN curl -Ls https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.cargo/bin:${PATH}"

# 의존성 설치 (lock/pyproject 기반)
COPY pyproject.toml uv.lock* ./
RUN uv sync --frozen || uv sync

# 앱 복사
COPY . .

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]