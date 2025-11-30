"""Simple CLI client to interact with the glossary service."""
import argparse
import asyncio
import json

import grpc

from gen import glossary_pb2, glossary_pb2_grpc


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Glossary client")
    parser.add_argument("--addr", default="localhost:50051", help="Glossary service address")
    parser.add_argument("--search", default=None, help="Query string to search terms")
    return parser.parse_args()


async def main() -> None:
    args = parse_args()
    async with grpc.aio.insecure_channel(args.addr) as channel:
        stub = glossary_pb2_grpc.GlossaryServiceStub(channel)
        if args.search:
            resp = await stub.SearchTerms(glossary_pb2.SearchTermsRequest(query=args.search))
        else:
            resp = await stub.ListTerms(glossary_pb2.ListTermsRequest())
        print(json.dumps([{ "id": t.id, "title": t.title, "definition": t.definition } for t in resp.terms], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
