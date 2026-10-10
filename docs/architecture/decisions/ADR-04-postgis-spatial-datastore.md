# ADR-04: Selection of PostgreSQL 16 with PostGIS 3.4 as Primary Spatial Datastore

## 1. Status
**Approved** (2026-10-10)

## 2. Context
Ritucast requires a robust, standards-compliant datastore capable of managing relational application data, complex multi-polygon administrative boundaries (`DATA-BND-01`), meteorological time-series records, and spatial queries (zonal intersections, point-in-polygon lookups).

We considered:
1. *MongoDB with GeoJSON indexes*
2. *Standalone TimescaleDB / InfluxDB + PostGIS*
3. *PostgreSQL 16 with PostGIS 3.4 (Selected)*

## 3. Decision
We adopt **PostgreSQL 16 with PostGIS 3.4** as the primary datastore, partitioned by date ranges for historical meteorological observations.

## 4. Rationale & Trade-Offs
- **Spatial Gold Standard**: PostGIS is the global benchmark for geospatial vector operations. Native spatial GiST indexing provides sub-millisecond point-in-polygon resolution (`ST_Contains`, `ST_Intersects`) across Bangladesh's 495 upazila polygons.
- **ACID Compliance & Reliability**: Eliminates data corruption risks during concurrent daily batch ingestion updates.
- **Partitioning for Time-Series**: PostgreSQL native declarative table partitioning (`PARTITION BY RANGE (obs_date_bst)`) handles millions of daily meteorological rows across seasons without requiring a separate time-series database engine like InfluxDB.
- **Cost & Managed Availability**: Available on managed Google Cloud SQL (`db-f1-micro` / `db-g1-small`) starting at $\sim \$20/\text{month}$, complete with automated daily snapshots and Point-In-Time-Recovery (PITR).

## 5. Revisit Triggers
This decision will be revisited if:
- National expansion across all 64 districts scales historical hourly weather records past $500\text{ million}$ rows, justifying TimescaleDB hypertable extensions.
