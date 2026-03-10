FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN python -c "import asyncio; from main import index_folder; asyncio.run(index_folder('./sample_docs'))"

EXPOSE 8001

CMD ["fastmcp", "run", "main.py:mcp", "--transport", "http", "--host", "0.0.0.0", "--port", "8001"]