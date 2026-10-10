# ADR-05: Selection of Redis 7 for In-Memory Caching, Rate Limiting, and Task Broker

## 1. Status
**Approved** (2026-10-10)

## 2. Context
Ritucast must achieve $P_{95} \le 500\text{ ms}$ response latency on mobile advisory queries, prevent API scraping abuse, and queue scheduled background data ingestion tasks without database lock contention.

We considered:
1. *Memcached (pure key-value cache)*
2. *RabbitMQ + Redis*
3. *Redis 7 (Alpine) Multi-Purpose (Selected)*

## 3. Decision
We adopt **Redis 7 (Alpine)** to fulfill three consolidated roles:
1. In-memory cache-aside store for pre-computed upazila advisory JSON payloads ($6\text{h}$ TTL).
2. Distributed task queue broker and results backend for Celery background workers.
3. Token-bucket sliding-window rate limiter ($60\text{ req/min}$ per client IP).

## 4. Rationale & Trade-Offs
- **Sub-20ms Read Latency**: Pre-rendered upazila advisory payloads are served directly from RAM in $<20\text{ ms}$, shielding PostgreSQL from high read concurrency during morning farming hours.
- **Tool Consolidation**: Using Redis for both caching and Celery task queueing eliminates the operational and financial overhead of running a separate RabbitMQ cluster.
- **Graceful Degradation**: If Redis is temporarily unreachable, the FastAPI backend catches the connection exception and falls back directly to PostgreSQL queries without dropping user requests.

## 5. Revisit Triggers
This decision will be revisited if:
- Ingestion job volume exceeds $10,000\text{ tasks/minute}$, requiring dedicated message brokers (e.g., RabbitMQ or Google Cloud Pub/Sub).
