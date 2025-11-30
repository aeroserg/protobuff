# Отчёт по gRPC-глоссарию

## Цель
Создать глоссарий терминов ВКР, предоставить gRPC API и контейнеризацию для быстрого развёртывания, а также сервис mindmap для визуализации связей.

## Состав репозитория
- `proto/glossary.proto` — описание контрактов gRPC.
- `services/` — реализации Glossary и Mindmap, вспомогательное хранилище, CLI-клиент.
- `data/terms.yaml` — базовые термины для загрузки.
- `glossary/Dockerfile`, `mindmap/Dockerfile`, `docker-compose.yml` — контейнеры и оркестрация.
- `docs/research.md` — исследовательская часть по сравнению REST/gRPC/GraphQL.

## Развёртывание
1. Установить Docker/Docker Compose.
2. Собрать и запустить:
   ```bash
   docker-compose build
   docker-compose up -d
   ```
3. Проверить, что сервисы поднялись:
   ```bash
   docker ps --filter "name=glossary" --filter "name=mindmap"
   ```

## Примеры запросов
- Список терминов:
  ```bash
  grpcurl -plaintext localhost:50051 glossary.GlossaryService/ListTerms
  ```
- Поиск по подстроке:
  ```bash
  grpcurl -plaintext -d '{"query":"gRPC"}' localhost:50051 glossary.GlossaryService/SearchTerms
  ```
- Добавление нового термина:
  ```bash
  grpcurl -plaintext -d '{"term":{"id":"term-4","title":"GraphQL","definition":"API over schema","sources":["https://graphql.org"],"relations":[{"target_id":"term-2","type":"alternative_to"}]}}' localhost:50051 glossary.GlossaryService/AddTerm
  ```
- Построение графа связей:
  ```bash
  grpcurl -plaintext localhost:50052 glossary.MindmapService/GetGraph
  ```

## Развёртывание на публичном сервере
- Скопировать репозиторий, выполнить команды из раздела выше.
- Открыть порты 50051 и 50052 в брандмауэре/SG.
- (Опционально) Поднять reverse-proxy (Nginx/Traefik) с TLS и пробросом gRPC (`grpc_pass`).
- Для CI/CD: можно запушить в GitHub и настроить GitHub Actions, публикуя образы в GHCR, затем тянуть их на сервере.

## Итоги
- Два gRPC-сервиса со схемой protobuf и совместимыми Docker-образами.
- Mindmap потребляет Glossary и отдаёт готовый граф для визуализаций.
- Пример данных и пошаговая инструкция присутствуют.
