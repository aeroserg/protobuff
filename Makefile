PYTHON=python3
PROTO_DIR=proto
GEN_DIR=services/gen

.PHONY: proto run-glossary run-mindmap

proto:
	mkdir -p $(GEN_DIR)
	$(PYTHON) -m grpc_tools.protoc -I $(PROTO_DIR) --python_out=$(GEN_DIR) --grpc_python_out=$(GEN_DIR) $(PROTO_DIR)/glossary.proto

run-glossary:
	PYTHONPATH=services:services/gen $(PYTHON) services/glossary_server.py

run-mindmap:
	PYTHONPATH=services:services/gen $(PYTHON) services/mindmap_server.py --glossary_addr localhost:50051
