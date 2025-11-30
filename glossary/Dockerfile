FROM python:3.11-slim
WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY proto proto
COPY services services
COPY data data

RUN python -m grpc_tools.protoc -I proto --python_out=services/gen --grpc_python_out=services/gen proto/glossary.proto

ENV PYTHONPATH=/app/services
EXPOSE 50051
CMD ["python", "services/glossary_server.py", "--host", "0.0.0.0", "--port", "50051", "--data", "/app/data/terms.yaml", "--bootstrap", "/app/data/terms.yaml"]
