import argparse
import asyncio
from pathlib import Path
import logging

import grpc
import yaml

from gen import glossary_pb2, glossary_pb2_grpc
from storage import GlossaryStore

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


class GlossaryService(glossary_pb2_grpc.GlossaryServiceServicer):
    def __init__(self, store: GlossaryStore):
        self.store = store

    async def AddTerm(self, request, context):
        term = request.term
        if not term.id:
            await context.abort(grpc.StatusCode.INVALID_ARGUMENT, "id is required")
        saved = self.store.add_term(term)
        return glossary_pb2.TermResponse(term=saved)

    async def GetTerm(self, request, context):
        term = self.store.get(request.id)
        if not term:
            await context.abort(grpc.StatusCode.NOT_FOUND, "term not found")
        return glossary_pb2.TermResponse(term=term)

    async def ListTerms(self, request, context):
        return glossary_pb2.ListTermsResponse(terms=self.store.all_terms())

    async def SearchTerms(self, request, context):
        results = self.store.search(request.query or "")
        return glossary_pb2.ListTermsResponse(terms=results)


def load_bootstrap_terms(store: GlossaryStore, bootstrap_file: Path) -> None:
    if not bootstrap_file.exists():
        return
    data = yaml.safe_load(bootstrap_file.read_text()) or []
    for item in data:
        relations = [
            glossary_pb2.Relation(target_id=rel.get("target_id", ""), type=rel.get("type", ""))
            for rel in item.get("relations", [])
        ]
        term = glossary_pb2.Term(
            id=item.get("id", ""),
            title=item.get("title", ""),
            definition=item.get("definition", ""),
            sources=item.get("sources", []),
            relations=relations,
        )
        if term.id and not store.get(term.id):
            store.add_term(term)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="gRPC glossary service")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", default=50051, type=int)
    parser.add_argument("--data", default="data/terms.yaml")
    parser.add_argument(
        "--bootstrap", default="data/terms.yaml", help="YAML with initial terms"
    )
    return parser.parse_args()


async def serve() -> None:
    args = parse_args()
    store = GlossaryStore(Path(args.data))
    load_bootstrap_terms(store, Path(args.bootstrap))

    server = grpc.aio.server()
    glossary_pb2_grpc.add_GlossaryServiceServicer_to_server(GlossaryService(store), server)
    listen_addr = f"{args.host}:{args.port}"
    server.add_insecure_port(listen_addr)
    logging.info("GlossaryService listening on %s", listen_addr)
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    asyncio.run(serve())
