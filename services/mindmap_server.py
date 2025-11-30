import argparse
import asyncio
import logging
import os

import grpc

from gen import glossary_pb2, glossary_pb2_grpc

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Mindmap gRPC service")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=50052)
    parser.add_argument(
        "--glossary_addr",
        default=os.getenv("GLOSSARY_ADDR", "localhost:50051"),
        help="Glossary gRPC endpoint",
    )
    return parser.parse_args()


class MindmapService(glossary_pb2_grpc.MindmapServiceServicer):
    def __init__(self, glossary_stub: glossary_pb2_grpc.GlossaryServiceStub):
        self.stub = glossary_stub

    async def GetGraph(self, request, context):
        response = await self.stub.ListTerms(glossary_pb2.ListTermsRequest())
        nodes = [glossary_pb2.GraphNode(id=term.id, label=term.title) for term in response.terms]
        edges = []
        for term in response.terms:
            for rel in term.relations:
                edges.append(
                    glossary_pb2.GraphEdge(
                        source=term.id,
                        target=rel.target_id,
                        type=rel.type,
                    )
                )
        return glossary_pb2.GraphResponse(nodes=nodes, edges=edges)


async def serve() -> None:
    args = parse_args()
    async with grpc.aio.insecure_channel(args.glossary_addr) as channel:
        stub = glossary_pb2_grpc.GlossaryServiceStub(channel)
        server = grpc.aio.server()
        glossary_pb2_grpc.add_MindmapServiceServicer_to_server(MindmapService(stub), server)
        listen_addr = f"{args.host}:{args.port}"
        server.add_insecure_port(listen_addr)
        logging.info(
            "MindmapService listening on %s; glossary backend %s",
            listen_addr,
            args.glossary_addr,
        )
        await server.start()
        await server.wait_for_termination()


if __name__ == "__main__":
    asyncio.run(serve())
