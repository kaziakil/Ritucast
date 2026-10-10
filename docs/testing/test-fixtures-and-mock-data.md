# Test Fixtures and Mock Data — Ritucast System Validation

## 1. Separation of Test Fixtures vs Live Data

In adherence to [AGENTS.md](file:///Users/kazi/Projects/RITUCAST/AGENTS.md) and Phase 12 guidelines, test fixtures and mock data are strictly isolated from production data structures:

- **Deterministic Fixtures**: Stored under `data/sample/` in version-controlled JSON, GeoJSON, and Parquet formats.
- **Production / Ingested Data**: Stored under `data/processed/` and `data/raw/` (git-ignored for heavy binary satellite tiles).
- **No Mock Leakage in Production**: The application backend does not automatically fall back to mock data in normal production mode. Fallback is explicitly controlled via repository flags and reported in metadata provenance (`provenance.is_sample = true`).

---

## 2. Inventory of Test Fixtures

| Fixture File Path | Content & Format | Pilot Scope | Purpose |
| :--- | :--- | :--- | :--- |
| `data/sample/bangladesh_pilot_upazilas.geojson` | GeoJSON FeatureCollection | 4 Upazilas (Godagari, Tanore, Tahirpur, Sunamganj Sadar) | Boundary rendering and spatial intersection tests. |
| `data/sample/pilot_upazilas.json` | JSON Array | 4 Upazilas | Administrative metadata, centroids, AEZ codes. |
| `data/sample/pilot_crops.json` | JSON Array | Boro Rice | Crop phenology stages, base Kc values, rooting depth. |
| `data/sample/pilot_seasons.json` | JSON Array | Rabi / Boro season | Crop calendar dates, target planting/harvest windows. |
| `data/sample/weather_pilot_sample.json` | JSON Object | Time series weather | Deterministic Penman-Monteith ET0 input tests. |
| `data/sample/soil_moisture_pilot_sample.json` | JSON Object | Soil moisture records | Antecedent soil moisture saturation ($f_M$) tests. |
| `data/sample/hydrology_pilot_sample.json` | JSON Object | BWDB water levels | Surma river stage ($f_S$) and Meghna rainfall ($f_P$). |

---

## 3. Mock Data Guidelines

1. **Clear Provenance Flagging**:
   - Every mock object in tests must declare its synthetic or sample nature.
   - Mock response generators must never construct synthetic values disguised as actual satellite sensor readings.
2. **Strict Schema Conformance**:
   - All mock objects used in frontend Vitest suites conform 100% to TypeScript schemas defined in [frontend/src/types/api.ts](file:///Users/kazi/Projects/RITUCAST/frontend/src/types/api.ts).
   - All Python mock objects conform to Pydantic models in [api/schemas/](file:///Users/kazi/Projects/RITUCAST/api/schemas/).
