import yaml
from pathlib import Path
from typing import Dict, Iterable, List

from gen import glossary_pb2


class GlossaryStore:
    def __init__(self, data_path: Path):
        self._data_path = Path(data_path)
        self._terms: Dict[str, glossary_pb2.Term] = {}
        self._load()

    def _load(self) -> None:
        if not self._data_path.exists():
            return
        raw_terms = yaml.safe_load(self._data_path.read_text()) or []
        for item in raw_terms:
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
            if term.id:
                self._terms[term.id] = term

    def _persist(self) -> None:
        payload = []
        for term in self._terms.values():
            payload.append(
                {
                    "id": term.id,
                    "title": term.title,
                    "definition": term.definition,
                    "sources": list(term.sources),
                    "relations": [
                        {"target_id": rel.target_id, "type": rel.type} for rel in term.relations
                    ],
                }
            )
        self._data_path.parent.mkdir(parents=True, exist_ok=True)
        self._data_path.write_text(yaml.safe_dump(payload, allow_unicode=True, sort_keys=False))

    def add_term(self, term: glossary_pb2.Term) -> glossary_pb2.Term:
        if not term.id:
            raise ValueError("term.id is required")
        self._terms[term.id] = term
        self._persist()
        return term

    def get(self, term_id: str) -> glossary_pb2.Term | None:
        return self._terms.get(term_id)

    def all_terms(self) -> List[glossary_pb2.Term]:
        return list(self._terms.values())

    def search(self, query: str) -> List[glossary_pb2.Term]:
        needle = query.lower()
        return [
            term
            for term in self._terms.values()
            if needle in term.title.lower() or needle in term.definition.lower()
        ]

    def as_graph(self) -> tuple[list[glossary_pb2.Term], list[glossary_pb2.Relation]]:
        terms = self.all_terms()
        relations: list[glossary_pb2.Relation] = []
        for term in terms:
            for rel in term.relations:
                relations.append(rel)
        return terms, relations


def load_terms(store: GlossaryStore, terms: Iterable[glossary_pb2.Term]) -> None:
    for term in terms:
        store.add_term(term)
