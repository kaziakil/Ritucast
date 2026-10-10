# Known Test Limitations — Ritucast System Validation

## 1. Overview

This document explicitly identifies test coverage boundaries, unexecuted workflows, and known limitations discovered during Phase 12 validation.

---

## 2. Inventory of Known Limitations

### 2.1 Headless Browser Automation vs DOM Component Testing
- **Status**: Tested via Vitest + `@testing-library/react` and live proxy inspection (`curl`).
- **Limitation**: Full headless Playwright / Selenium browser test suite was not deployed in Phase 12 due to lightweight client constraints (`DEC-09`).
- **Mitigation**: Vitest user journey tests simulate complete user click flows, tab changes, API calls, and failure banners. Live proxy validation verified browser communication on ports 3000 and 8000.

### 2.2 Live Sentinel-1 Large Granule Ingestion in CI
- **Status**: Tested with localized pilot testbed sample rasters and synthetic backscatter points.
- **Limitation**: Live automated downloading of full 1GB+ Sentinel-1 GRD granules from Copernicus Data Space Ecosystem was excluded from regular test runs to maintain fast, deterministic test execution (<10s).
- **Mitigation**: Dedicated sample GeoTIFF and Parquet tables contain real radar backscatter measurements over Tahirpur.

### 2.3 BMD Ground Station Direct Telemetry
- **Status**: Synthesized with NASA POWER and Open-Meteo feeds.
- **Limitation**: Bangladesh Meteorological Department (BMD) direct real-time telemetry API requires official governmental MOUs not currently provisioned for public automated CI.
- **Mitigation**: Open-Meteo ECMWF/GFS ensemble feeds serve as validated operational NWP inputs, paired with NASA POWER climatology.

### 2.4 Multi-Year Retrospective Cross-Validation
- **Status**: Validated across single-season pilot datasets (Boro Rice 2023–2024).
- **Limitation**: 10-year retrospective hindcast validation across all 64 districts is scheduled for Phase 13 and Phase 14 validation milestones.
