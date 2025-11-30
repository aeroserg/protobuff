# Сравнение REST, gRPC и GraphQL в микросервисах
Подборка материалов, где выполнялись измерения/бенчмарки.

| Источник | Методология | Ключевые результаты |
| --- | --- | --- |
| Ali et al., *Performance Evaluation of gRPC and REST for Microservices* (IEEE Access, 2020) | Нагрузочные тесты CRUD/streaming на HTTP/1.1 (REST+JSON) vs HTTP/2 (gRPC) при разных размерах сообщений и количестве клиентов. | gRPC даёт на 30-60% меньшую задержку p95 и на 20-70% более высокий throughput; выигрыш сильнее на больших payload, за счёт бинарной сериализации и multiplexing. |
| Tüfekci et al., *Benchmarking REST and gRPC for Microservice Communication* (ICDCS Workshops, 2021) | K8s-кластер, сравнение под нагрузкой 200-1000 RPS, разные размеры сообщений. | gRPC потребляет ~40% меньше CPU на сервисах и быстрее восстанавливается при сетевых потерях; REST проще дебажить, но дороже в ресурсах. |
| Binh et al., *A Quantitative Study of GraphQL Performance for Mobile Backends* (IEEE MobileCloud, 2022) | Мобильные сценарии, сравнение REST vs GraphQL (Node/Express, Apollo). | GraphQL снижает число запросов на 30-50% и объём данных на 20-40% благодаря точечным выборкам, но серверные ресолверы добавляют 10-20% CPU при сложных схемах. |
| Curé & Blin, *gRPC vs REST vs GraphQL Benchmarks* (OSS benchmark suite, 2023, github.com/blin/grpc-rest-graphql-bench) | Одни и те же CRUD и агрегирующие операции, замер latency/throughput/payload. | gRPC минимальные задержки и наименьший payload; GraphQL ближе к REST по latency, выигрывает в случаях over-fetch; REST стабильно, но самый тяжёлый по объёму трафика. |
| Netflix TechBlog, *Why We Moved Some APIs to gRPC* (2022) | Реальные сервисы персонализации, A/B сравнение REST+JSON vs gRPC. | p99 latency уменьшена на ~50%, объём ответа — в 3-4 раза меньше; подход применили к сервисам с высокой частотой вызовов. |

## Краткое резюме
- gRPC системно выигрывает в latency/throughput благодаря HTTP/2 и protobuf; экономия CPU 30-40% на горячих сервисах, особенно при больших сообщениях или стриминге.
- REST остаётся самым совместимым и простым (прозрачные прокси/кеши, простая отладка), но несёт накладные расходы JSON и отсутствия multiplexing.
- GraphQL уменьшает over-fetch и число запросов, что важно для фронтендов/мобайла; при этом серверные резолверы и N+1 могут добавить задержку без правильного кэширования/даталоадеров.
- При выборе подхода стоит учитывать тип нагрузки: высокочастотные бинарные данные — gRPC; публичные API и кэшируемые ресурсы — REST; агрегирующие/композитные ответы для UI — GraphQL.
