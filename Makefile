PYTHON=python3
PROTO_DIR=proto
GEN_DIR=services/gen

proto:
	$(PYTHON) -m grpc_tools.protoc -I $(PROTO_DIR) --python_out=$(GEN_DIR) --grpc_python_out=$(GEN_DIR) $(PROTO_DIR)/glossary.proto

run-glossary:
	PYTHONPATH=services $(PYTHON) services/glossary_server.py

run-mindmap:
	PYTHONPATH=services $(PYTHON) services/mindmap_server.py --glossary_addr localhost:50051
