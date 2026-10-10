# Phase 3 Plan: Dataset Research and Validation

## 1. Phase Metadata

- **Phase ID**: Phase 03
- **Phase Name**: Dataset Research and Validation
- **Lead Role**: Senior Earth Observation Scientist, Agricultural Data Engineer, Geospatial Analyst, Remote-Sensing Researcher, Data Quality Specialist
- **Status**: **In Progress**
- **Date**: 2026-10-10
- **Preceding Phase**: Phase 02 (Requirements and Product Strategy — PASS)
- **Succeeding Phase**: Phase 04 (Agricultural Knowledge and Scientific Validation Planning)

---

## 2. Work Breakdown Packages (WPs)

```mermaid
flowchart TD
    WP0[WP 0: Readiness Audit & Baseline Extraction] --> WP1[WP 1: Candidate Dataset Inventory across 16 Categories]
    WP1 --> WP2[WP 2: NASA POWER Agrometeorology Deep Dive & API Verification]
    WP2 --> WP3[WP 3: MODIS & Sentinel-2 Vegetation Indices Evaluation]
    WP3 --> WP4[WP 4: SMAP Soil Moisture Analysis & Radiometer Physics Audit]
    WP4 --> WP5[WP 5: GPM IMERG Precipitation Pipeline & Latency Audit]
    WP5 --> WP6[WP 6: Sentinel-1 SAR Cloud-Penetrating Radar Flood Mapping Audit]
    WP6 --> WP7[WP 7: Crop Statistics, Calendars & Administrative Boundaries]
    WP7 --> WP8[WP 8: Additional Environmental Data Sources - Soils, Prices, Forecasts]
    WP8 --> WP9[WP 9: Dataset Comparison Matrix & 3-Tier Initial Stack Selection]
    WP9 --> WP10[WP 10: Data Access, Licensing & Legal Governance]
    WP10 --> WP11[WP 11: Data Quality Validation Protocols & Aggregation Rules]
    WP11 --> WP12[WP 12: Phase Validation Report & Handoff to Phase 4]
```

---

## 3. Strict Boundary Controls

1. **No Code Implementation**: No production backend ingestion services, Celery workers, or database schemas will be constructed.
2. **No Bulk Dataset Storage**: Only tiny sample GeoJSON/JSON responses ($<500\text{KB}$) used to verify schemas will be inspected. No heavy GeoTIFFs, NetCDF, or HDF5 files will be committed to version control.
3. **Primary Source Auditing**: Every technical specification (units, scale factors, coordinate reference systems, fill values) must be validated against primary mission user guides and live API metadata.
