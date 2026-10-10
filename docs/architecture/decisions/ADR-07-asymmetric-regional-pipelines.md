# ADR-07: Asymmetric Regional Processing Pipelines for Barind and Haor Zones

## 1. Status
**Approved** (2026-10-10)

## 2. Context
Bangladesh encompasses extreme agro-ecological divergence. The High Barind Tract (Rajshahi) suffers from deep groundwater deficit and dry clay terraces requiring daily evapotranspiration and soil water balance modeling. Conversely, the Haor Basin (Sunamganj) is a low-lying tectonic wetland facing catastrophic transboundary flash floods requiring multi-sensor catchment precipitation accumulation and river stage tracking (`DEC-03`, `DEC-11`, `ARC-CON-01`).

Attempting to run a single monolithic processing pipeline across all upazilas introduces unnecessary computation, false alerts, and maintenance friction.

## 3. Decision
We formally decouple the backend data processing into two specialized, asymmetric pipelines executed by independent Celery worker tasks:
1. **Barind Irrigation & Evapotranspiration Pipeline**:
   - Executes daily at $02:00\text{ UTC}$ ($08:00\text{ BST}$).
   - Ingests NASA POWER solar radiation, humidity, and wind speed; computes daily FAO-56 Penman-Monteith $ET_0$ (`EQN-ET0-01`); evaluates dynamic $K_c$ (`EQN-ETC-01`); and computes root-zone soil water deficit $D_t$ (`EQN-SWD-01`) for Boro rice and upland crops in Godagari and Tanore.
2. **Haor Flash-Flood Hydrology Pipeline**:
   - Executes every 6 hours ($00:00, 06:00, 12:00, 18:00\text{ UTC}$).
   - Scrapes BWDB Surma/Kushiyara river gauge stages; aggregates GPM IMERG 48h rainfall over the transboundary Meghalaya catchment box ($25.10–25.45^\circ\text{N}, 91.10–92.00^\circ\text{E}$); checks for Sentinel-1 SAR inundation masks; and evaluates the composite hazard index $I_{\text{flood}}$ (`IDX-FLD-01`) for Sunamganj Sadar and Tahirpur.

## 4. Rationale & Trade-Offs
- **Agronomic Fit**: Prevents the Haor pipeline from executing irrelevant deep-tubewell water balance calculations, and prevents the Barind pipeline from calculating transboundary flash-flood indices over elevated terraces.
- **Cadence Optimization**: Flash-flood indicators require rapid 6-hourly updates, whereas soil water balance operates on a 24-hour daily cycle. Decoupling avoids wasting compute cycles running hourly water balance models.
- **Fault Isolation**: An API outage at the BWDB hydrometric portal has zero impact on Barind irrigation advisories.

## 5. Revisit Triggers
This decision will be revisited if:
- Future expansion (Phase 18) introduces new agro-ecological zones (e.g., Coastal Saline Zone AEZ 13), requiring a third specialized pipeline.
