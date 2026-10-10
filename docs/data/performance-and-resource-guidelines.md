# Phase 8: Performance and Resource Management Guidelines

## 1. Executive Summary & Hardware Context

The Ritucast data pipeline is designed to execute smoothly across two key deployment targets:
1. **Developer Workstation**: Apple Silicon MacBook (M1/M2/M3) with 16GB RAM.
2. **Cloud Execution**: Google Cloud Run Container Jobs / Celery Workers with 1 vCPU and $\le 1024\text{MB}$ memory allocation.

To prevent memory crashes, disk exhaustion, and network throttling, the pipeline implements strict resource management constraints.

---

## 2. Resource & Budget Thresholds

| Resource Dimension | Upper Limit | Enforcement Mechanism |
| :--- | :---: | :--- |
| **Peak Worker Heap Memory** | $\le 512\text{MB}$ | Streaming chunk processing; avoidance of full-country in-memory GeoDataFrames. |
| **Raw Disk Cache per Run** | $\le 200\text{MB}$ | Ephemeral scratch storage; immediate aggregation of NetCDF to zonal stats. |
| **Processed Analytical Parquet** | $\le 50\text{MB}$ / month | Snappy columnar compression, dictionary encoding of strings. |
| **NASA POWER API Concurrency** | $1\text{ req} / 2.0\text{s}$ | Token bucket rate limiter preventing IP throttling (`RSK-14`). |
| **Open-Meteo API Calls** | $\le 10,000$ calls / day | Batch coordinate queries and 6-hour cache TTL. |
| **End-to-End Pipeline Runtime** | $\le 3.0\text{ minutes}$ | Efficient vectorized pandas/pyarrow transformations. |

---

## 3. Engineering Optimization Techniques

### 3.1 Avoidance of Heavy C-Extension Binaries
By utilizing `shapely` (v2.1+) with GeoJSON parsing and PostGIS server-side spatial indices, the ingestion pipeline eliminates the need for heavyweight GDAL/OGR runtime bloat in standard API containers (`ADR-01`, `ADR-04`).

### 3.2 Chunked & Filtered Coordinate Queries
Rather than requesting a monolithic global NetCDF raster, adapters query bounded sub-grids or point coordinates centered on Upazila centroids. For NASA POWER, queries specify exact target bounding boxes ($88.0^\circ–92.8^\circ\text{E}, 20.5^\circ–26.7^\circ\text{N}$) or pilot station points.

### 3.3 Columnar Parquet Serialization
Tabular feature sets are serialized using Apache Parquet (`pyarrow` engine) with `snappy` compression. Compared to raw CSV:
- Disk footprint is reduced by **$75–85\%$**.
- Read latency for Phase 9 analytics is reduced by **$10\times$**, as only required columns (e.g. `t2m_max_c`, `precipitation_mm`) are scanned from disk.
