# Phase 11 Plan: Frontend Application and User Experience

## 1. Objectives & Scope

Phase 11 implements the user-facing web application for Ritucast, converting validated data ingestion, physical analytics, and backend REST endpoints into an intuitive, high-performance, and responsive user experience for farmers and extension workers in Bangladesh.

### In Scope
- React 19 + TypeScript 6 + Vite 8 SPA application architecture.
- Custom Vanilla CSS Design System with CSS Custom Properties (`index.css`).
- High-contrast outdoor readability tuned for sunlight on budget mobile screens.
- Strict 4-Tier Information Taxonomy presentation (`DEC-08`).
- Contextual Gating Bar enforcing selection of Upazila, Crop, and Growth Stage (`DEC-17`).
- Automated Advisory Suppression Banner display (`DEC-10`).
- Dedicated analytical views:
  - Advisory Hub (Tier 4 actions + economic savings + disclaimers).
  - Weather Feed (Tier 1 NASA/BMD observations + Tier 3 72h forecasts).
  - Water Balance (FAO-56 $ET_0$, $ET_c$, soil deficit $D_t$, AWD status).
  - Flash Flood Hazard (Haor $I_{\text{flood}}$ gauge + early harvest trigger).
  - Provenance & Transparency (Dataset freshness + physical equations).
- Type-safe REST client for all 12 Phase 10 API endpoints.
- Vitest unit and integration test suite.
- Production bundle verification ensuring compliance with payload budgets ($\le 1.5\text{MB}$, `DEC-09`).

### Out of Scope
- Interactive Leaflet/MapLibre map vector tiles (Phase 12).
- Offline service worker caching and SMS fallback (Phase 13).
- User authentication, payments, or cloud deployment automation.
- Sub-acre yield predictions or pesticide advice (`DEC-06`).

---

## 2. Methodology & Work Breakdown

1. **Step 1**: Audit Phase 10 API endpoints and OpenAPI schemas.
2. **Step 2**: Initialize Vite React TypeScript project and configure build/test tooling.
3. **Step 3**: Author design tokens and Vanilla CSS stylesheet (`frontend/src/index.css`).
4. **Step 4**: Implement typed API client (`frontend/src/services/apiClient.ts`).
5. **Step 5**: Build modular React components (`Header`, `ContextSelector`, `AdvisoryHubView`, `WeatherFeedView`, `WaterBalanceView`, `FloodHazardView`, `ProvenanceView`, `Footer`).
6. **Step 6**: Integrate components in root workspace (`App.tsx`).
7. **Step 7**: Write Vitest unit and integration tests.
8. **Step 8**: Verify production build (`npm run build`) and bundle metrics.
9. **Step 9**: Document frontend architecture, design system, and API integration.
10. **Step 10**: Finalize Phase 11 deliverables and author Phase 12 handoff package.
