# ADR-06: Selection of MapLibre GL JS v3 for Vector Map Visualizations with Leaflet Fallback

## 1. Status
**Approved** (2026-10-10)

## 2. Context
Ritucast requires interactive map visualizations to display upazila hazard zones, Barind moisture deficit anomalies, and Haor satellite radar inundation masks (`FR-DSH-02`, `FR-ENV-04`). However, client devices operate with limited RAM ($\le 2\text{GB}$, Android 8+), where heavy map libraries cause out-of-memory crashes (`RSK-06`).

We evaluated:
1. *Mapbox GL JS v2+*
2. *OpenLayers*
3. *Leaflet (pure raster)*
4. *MapLibre GL JS v3 with Lazy-Loading (Selected)*

## 3. Decision
We adopt **MapLibre GL JS v3** as the primary vector map rendering engine, utilizing **PMTiles** for serverless vector tile streaming, paired with **Leaflet** as a low-memory fallback for legacy devices:
- MapLibre GL JS is **dynamically imported (lazy-loaded)** only when the user explicitly taps "মানচিত্র দেখুন" (View Map).
- On initial page load, the map library is **not bundled into the primary JS bundle**, preserving the $\le 1.5\text{MB}$ payload ceiling (`DEC-09`).

## 4. Rationale & Trade-Offs
- **Permissive Open-Source Licensing**: Mapbox GL JS v2+ enforces proprietary token billing and user tracking. MapLibre GL JS is 100% open-source under BSD-3-Clause with zero tracking or per-map-view fees.
- **Serverless Vector Tiles (PMTiles)**: Vector tiles are stored as single archive files on Google Cloud Storage and queried via HTTP Range Requests through Cloud CDN, completely eliminating the need for expensive map tile servers (e.g., GeoServer or TileServer GL).
- **RAM Protection via Strict Teardown**: The React map component strictly unmounts and deletes the WebGL context when navigating away, keeping peak browser heap memory well below the $45\text{MB}$ ceiling (`NFR-PER-03`).

## 5. Revisit Triggers
This decision will be revisited if:
- WebGL 2.0 hardware acceleration is unsupported on $>20\%$ of field devices during Phase 14 field usability testing, prompting Leaflet raster tiles to become the default.
