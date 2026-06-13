FROM python:3.13-slim

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN pip install --no-cache-dir uv

RUN uv sync

COPY . .

EXPOSE 8501

CMD ["uv", "run", "streamlit", "run", "app/main.py", "--server.address=0.0.0.0", "--server.port=8501"]