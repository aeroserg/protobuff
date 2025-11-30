FROM python:3.11-slim
WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY proto proto
COPY services services

RUN python -m grpc_tools.protoc -I proto --python_out=services/gen --grpc_python_out=services/gen proto/glossary.proto

ENV PYTHONPATH=/app/services
EXPOSE 50052
CMD ["python", "services/mindmap_server.py", "--host", "0.0.0.0", "--port", "50052", "--glossary_addr", "glossary:50051"]
