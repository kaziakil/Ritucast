# Data Inventory and Privacy Classification — Ritucast

## 1. Overview

Ritucast is committed to the principles of data minimization and purposeful processing. This document inventories every data element processed, stored, or transmitted by the system, accompanied by its sensitivity classification and privacy impact assessment.

---

## 2. Comprehensive Data Element Inventory

| Data Element | Source | Storage Location | Sensitivity Tier | PII Status | Retention Period | Description & Purpose |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Upazila Identifier** | Client Query Parameter | In-memory query | **Public** | Non-PII | Ephemeral | Administrative BBS code (e.g. `BD-50-20-30`) selected from dropdown to filter regional data. |
| **Crop Name** | Client Query Parameter | In-memory query | **Public** | Non-PII | Ephemeral | Target crop (e.g. `Boro Rice`) for agronomic coefficient ($K_c$) lookup. |
| **Growth Stage** | Client Query Parameter | In-memory query | **Public** | Non-PII | Ephemeral | Phenological stage (e.g. `Tillering`, `Flowering`) for contextual gating (`DEC-17`). |
| **Client IP Address** | TCP / HTTP Connection | In-memory sliding window ([`RateLimitMiddleware`](file:///Users/kazi/Projects/RITUCAST/api/middleware/security.py)) | **Internal Operational** | Low / Transient | 60 seconds (ephemeral) | Used strictly for sliding-window rate limiting; purged automatically after 60 seconds. |
| **Daily Meteorology** | NASA POWER / BMD | Local Parquet table (`meteorology_daily_upazila.parquet`) | **Public** | Non-PII | Permanent | Upazila-aggregated historical temperature, solar radiation, humidity, precipitation. |
| **Hourly Forecasts** | Open-Meteo NWP | Local Parquet table (`forecast_hourly_pilot.parquet`) | **Public** | Non-PII | Permanent | 48-hour to 7-day quantitative precipitation, temperature, and ensemble spread metrics. |
| **Hydrological Water Levels** | BWDB Gauging Stations | In-memory fixtures | **Public** | Non-PII | Permanent | River water levels and danger thresholds ($8.25\text{m}$) for Haor flash-flood monitoring. |
| **Upazila Boundary GeoJSON** | BBS / GADM | Local GeoJSON (`bangladesh_pilot_upazilas.geojson`) | **Public** | Non-PII | Permanent | Administrative boundary polygons and centroid coordinates. |
| **Generated Advisories** | Recommendation Engine | Response Payload | **Public** | Non-PII | Ephemeral | 4-tier decision-support cards synthesized from agronomic rules. |

---

## 3. Privacy Posture & Non-PII Verification

### 3.1 Zero PII Ingestion
- **No Personal Identifiers**: Ritucast does **not** collect farmer names, national identity numbers (NID), phone numbers, email addresses, or account credentials.
- **No User Accounts or Passwords**: System operates as a public, read-only decision-support tool.
- **No Precise GPS Coordinates**: The application operates strictly at the administrative Upazila level (Level 3 administrative boundary, average area $250\text{--}450\text{ km}^2$). It does **not** collect, store, or query parcel-level GPS coordinates, cadastral survey plots, or homestead locations (`DEC-06`).

### 3.2 Zero Tracking & Telemetry
- **No Third-Party Analytics**: No Google Analytics, Facebook Pixel, Mixpanel, or telemetry beacons are included in the frontend bundle.
- **No Cookies**: Application uses zero tracking or advertising cookies.
- **No Local Storage Tracking**: The client uses React state only; no sensitive user preferences are persisted to browser `localStorage` or `sessionStorage`.

---

## 4. Privacy Impact Assessment (PIA)

Given that:
1. Zero Personally Identifiable Information is processed or stored.
2. Geographic aggregation is constrained to broad administrative Upazilas.
3. No biometric, financial, or personal communications are ingested.

The overall Privacy Risk for the pilot release of Ritucast is evaluated as **NEGLIGIBLE**.

---

## 5. Future Scope Privacy Requirements

If future phases or commercial pilots expand Ritucast to support farmer SMS alert subscriptions or cooperative member profiles:
1. **Explicit Informed Consent**: Opt-in consent must be recorded prior to storing mobile phone numbers.
2. **Encryption at Rest**: Telephone numbers and personal contact records must be encrypted using AES-256 / KMS.
3. **Right to Deletion**: Automated opt-out and record deletion mechanisms must be established.

Related documentation:
- [`docs/privacy/data-handling-and-retention.md`](file:///Users/kazi/Projects/RITUCAST/docs/privacy/data-handling-and-retention.md)
- [`docs/privacy/external-services-and-data-sharing.md`](file:///Users/kazi/Projects/RITUCAST/docs/privacy/external-services-and-data-sharing.md)
- [`docs/data/dataset-licensing-and-redistribution-review.md`](file:///Users/kazi/Projects/RITUCAST/docs/data/dataset-licensing-and-redistribution-review.md)
