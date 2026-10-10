# Ritucast: Performance & Resource Management Standards

## 1. Client Hardware & Network Budgets (`DEC-09`)

Rural Bangladeshi farmers operate budget Android smartphones (2GB–3GB RAM, Android 8+) over intermittent 3G cellular data connections.

### Operational Constraints:
- **Maximum API Response Size**: $\le 15\text{KB}$ uncompressed ($\le 3.5\text{KB}$ gzip compressed).
- **Target Response Latency**: $\le 50\text{ms}$ on server side ($\le 350\text{ms}$ over 3G cellular network).
- **Client Heap Footprint**: $\le 45\text{MB}$.
- **Zero Third-Party Upstream Calls from Client**: The frontend never connects directly to external APIs (NASA, BMD, Open-Meteo); all traffic is served by the backend cache.

---

## 2. Server Resource Management (`DEC-41`)

### 2.1 In-Memory Parquet Table Caching
- Parquet feature tables are read lazily upon first request and retained in the repository's `_cache` dictionary.
- Heap memory overhead for cached pilot tables:
  - `meteorology_daily_upazila.parquet`: $\approx 1.2\text{MB}$
  - `forecast_hourly_pilot.parquet`: $\approx 850\text{KB}$
  - `catchment_rainfall_daily.parquet`: $\approx 420\text{KB}$
  - `hydrology_river_stage.parquet`: $\approx 310\text{KB}$
- Total backend resident memory remains well under $60\text{MB}$, easily fitting into free-tier cloud container instances (e.g. 512MB RAM).

### 2.2 Algorithm Execution Complexity
- **FAO-56 Penman-Monteith (`EQN-ET0-01`)**: $O(1)$ arithmetic evaluation completed in $<0.2\text{ms}$.
- **Crop Water Demand (`EQN-ETC-01`)**: $O(1)$ dictionary lookup and interpolation completed in $<0.05\text{ms}$.
- **Soil Water Deficit Step (`EQN-SWD-01`)**: $O(1)$ daily step completed in $<0.1\text{ms}$.
- **Multi-Rule Evaluation**: Evaluating all 5 Phase 9 rules completes in $<1.5\text{ms}$.

---

## 3. Concurrency & Thread Safety

- The FastAPI application runs asynchronously on Uvicorn.
- The `AgriculturalDataRepository` performs read-only operations on cached data frames and immutable configuration dictionaries, ensuring complete thread safety under concurrent incoming HTTP requests without lock contention.

---

## 4. Related Documentation

- Architecture: [phase-10-backend-architecture.md](file:///Users/kazi/Projects/RITUCAST/docs/backend/phase-10-backend-architecture.md)
- Integration Contract: [phase-9-integration-contract.md](file:///Users/kazi/Projects/RITUCAST/docs/backend/phase-9-integration-contract.md)
