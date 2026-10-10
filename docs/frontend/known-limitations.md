# Frontend Known Limitations and Scope Boundaries

## 1. Geographical Limitations

1. **Dual Pilot Zone Confinement**: Ritucast currently operates exclusively within the High Barind Tract (Godagari, Tanore) and Haor Basin (Tahirpur, Sunamganj Sadar). Selection of administrative areas outside these regions is intentionally disabled until Phase 14 regional calibration is undertaken.
2. **Crop Confinement**: The platform is calibrated specifically for Boro rice (*Oryza sativa L.*). Non-rice crops (e.g., maize, wheat, mustard) are not yet supported by the phenological Kc curve engine.

---

## 2. Technical and Interactive Boundaries

1. **Interactive Geospatial Maps Deferred to Phase 12**:
   - In accordance with the 18-Phase lifecycle and sequential phase gating, full interactive Leaflet/MapLibre vector tile rendering is allocated to **Phase 12: Maps and Geospatial Visualization Layer**.
   - Phase 11 intentionally prioritizes the core UI/UX architecture, contextual gating selectors, indicator dashboards, and advisory cards.
2. **Offline Data Persistence Deferred to Phase 13**:
   - Offline service-worker caching, IndexedDB state synchronization, and SMS fallback packaging are scheduled for Phase 13 (Field Hardening & Offline Resilience).
   - In Phase 11, the app functions as an online PWA with in-memory caching and real-time backend API connectivity.
3. **No Direct Micro-Parcel Calculations (`DEC-06`)**:
   - The UI does not provide sub-acre cadastral parcel yield forecasts or automated pesticide diagnoses, strictly adhering to core governance principles.
