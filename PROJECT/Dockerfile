FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
COPY chroma_db/* .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8001

CMD ["fastmcp", "run", "main.py", "--transport", "http", "--port", "8001"]