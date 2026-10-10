# ADR-09: Selection of Celery and Cloud Scheduler for Asynchronous Data Ingestion

## 1. Status
**Approved** (2026-10-10)

## 2. Context
Ritucast must periodically pull data from 5 external remote sensing and weather providers (NASA POWER, Open-Meteo, NASA CMR GPM, ESA CDSE Sentinel-1, BWDB FFWC), transform coordinates, execute raster zonal statistics across upazila polygons, and refresh caches. NASA POWER enforces a soft rate limit of 30 requests/minute per IP (`RSK-14`).

These heavy, multi-minute ingestion workloads cannot run synchronously inside user-facing HTTP request handlers.

We evaluated:
1. *Synchronous In-Process Cron (APScheduler inside FastAPI)*
2. *Cloud Functions triggered by Cloud Pub/Sub*
3. *Celery Worker Containers with Redis Broker & Cloud Scheduler (Selected)*

## 3. Decision
We adopt **Celery 5.3** running in dedicated worker containers, backed by **Redis 7** as the task broker, triggered periodically by **Google Cloud Scheduler**:
- Cloud Scheduler dispatches signed HTTP webhook triggers every 6 hours ($00:00, 06:00, 12:00, 18:00\text{ UTC}$).
- The webhook enqueues ingestion tasks in Redis.
- Celery worker processes execute tasks with strict concurrency controls (`--concurrency=2`), staggered polling intervals ($1\text{ req/2s}$ for NASA POWER), automated retries with exponential backoff (max 3 retries), and dead-letter queueing.

## 4. Rationale & Trade-Offs
- **Rate-Limit Compliance**: Celery token-bucket rate limiting ensures that batch queries to NASA POWER never exceed the 30 req/min threshold, preventing IP blocking (`RSK-14`).
- **Heavy Dependency Containment**: All heavy C-libraries (GDAL, Rasterio, GEOS) are contained within the worker container image; the user-facing FastAPI image remains lean and fast.
- **Task Visibility & Retries**: Celery provides native task state tracking (`PENDING`, `STARTED`, `SUCCESS`, `FAILURE`) and automatic retries for transient HTTP timeouts without dropping data updates.

## 5. Revisit Triggers
This decision will be revisited if:
- Event-driven streaming architectures (e.g., Apache Kafka / Google Cloud Pub/Sub) become necessary when scaling to national real-time IoT sensor telemetry in Horizon 3.
