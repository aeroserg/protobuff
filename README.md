# gRPC Glossary Microservices

Два gRPC‑сервиса для глоссария терминов ВКР: хранение словаря и выдача семантического графа (mindmap). Код и контейнеры готовы к развёртыванию через `docker-compose`.

## Репозиторий
Загрузите текущую папку в GitHub (например, `https://github.com/<username>/grpc-glossary-dictionary`) — структура и Dockerfile уже подготовлены.

## Архитектура
- `GlossaryService` — CRUD/поиск терминов на gRPC, хранение в YAML (персистентность внутри тома контейнера).
- `MindmapService` — обращается к Glossary по gRPC и строит граф (nodes/edges) для фронтендов визуализации.
- Протоколы описаны в `proto/glossary.proto`, генерация stub выполняется в Dockerfile или `make proto`.

## Быстрый старт (локально через Docker)
```bash
docker-compose build
docker-compose up -d
```
Порты: Glossary `50051`, Mindmap `50052`.

Проверка через `grpcurl` (подходит `buf curl` или любой gRPC клиент):
```bash
grpcurl -plaintext localhost:50051 list glossary.GlossaryService
grpcurl -plaintext -d '{"query":"API"}' localhost:50051 glossary.GlossaryService/SearchTerms
grpcurl -plaintext localhost:50052 glossary.MindmapService/GetGraph
```

## Ручной запуск (без Docker)
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
make proto
PYTHONPATH=services python services/glossary_server.py --data data/terms.yaml
PYTHONPATH=services python services/mindmap_server.py --glossary_addr localhost:50051
```

## Добавление термина (пример)
```bash
grpcurl -plaintext -d '{"term": {"id":"term-4","title":"GraphQL","definition":"API over schemas","sources":["https://graphql.org"],"relations":[{"target_id":"term-2","type":"alternative_to"}]}}' \
  localhost:50051 glossary.GlossaryService/AddTerm
```

## Что ещё
- Подробный отчёт по развёртыванию и сценариям — `REPORT.md`.
- Исследовательская подборка сравнений REST/gRPC/GraphQL — `docs/research.md`.
- Тестовый клиент — `services/client_example.py` (после `make proto`).

Публикация на удалённый сервер: достаточно установить Docker, скопировать репозиторий и выполнить `docker-compose up -d`; при наличии публичного IP откройте 50051/50052 или заверните в HTTPS через reverse-proxy.
