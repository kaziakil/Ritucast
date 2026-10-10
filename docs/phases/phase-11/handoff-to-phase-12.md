# Handoff to Phase 12: Maps and Geospatial Visualization Layer

## 1. Phase Status & Readiness

Phase 11 (Frontend Application and User Experience) is complete and formally verified. The application shell, design system, API integration, contextual gating controls, analytical views, and Vitest test suite are operating cleanly with zero errors.

---

## 2. Verified Assets Delivered to Phase 12

1. **Frontend Application Shell**:
   - Location: `frontend/`
   - Framework: React 19 + TypeScript 6 + Vite 8.
   - Styling: Pure Vanilla CSS Design System with CSS Custom Properties in `frontend/src/index.css`.
2. **API Client Layer**:
   - Centralized client in `frontend/src/services/apiClient.ts` communicating with all 12 Phase 10 REST endpoints.
   - Geo-metadata endpoints ready: `/api/v1/upazilas` and `/api/v1/upazilas/{id}` providing canonical BBS GeoCodes, lat/lon centroids, AEZ codes, and boundary references.
3. **Contextual Gating Architecture**:
   - `ContextSelector.tsx` component ready to bind map selection interactions back to the global application state.
4. **Performance & Payload Headroom**:
   - Current wire bundle: 88.6 kB gzip, leaving over 1.4 MB of bandwidth headroom for geospatial vector tile or GeoJSON rendering libraries in Phase 12 (`DEC-09`).

---

## 3. Scope & Mandate for Phase 12 (From Roadmap)

Per `[roadmap.md](file:///Users/kazi/Projects/RITUCAST/docs/planning/roadmap.md)`, **Phase 12: Maps and Geospatial Visualization Layer** is tasked with:
- Implementing interactive map components (e.g. Leaflet or lightweight MapLibre vector tiles) within the Phase 11 frontend shell.
- Visualizing administrative boundaries of High Barind Tract (Godagari, Tanore) and Haor Basin (Tahirpur, Sunamganj Sadar).
- Rendering spatial indicator overlays: Sentinel-1 SAR surface water inundation masks, rainfall distribution gradients, and root-zone soil moisture deficit maps.
- Synchronizing map click events with the `ContextSelector` and updating analytical cards without page reloads.
- Respecting `DEC-06` non-goals: ensuring map layers do not falsely imply sub-acre cadastral precision.

---

## 4. Instructions for Phase 12 Agent

1. Do NOT recreate the frontend project or introduce Tailwind CSS (`ADR-03`, `DEC-20`).
2. Integrate map components directly into the existing `frontend/` directory structure.
3. Use the established `apiClient` and typed interfaces in `frontend/src/types/api.ts`.
4. Ensure geospatial libraries and vector tiles remain within the $\le 1.5\text{MB}$ bundle budget (`DEC-09`).
