# Ritucast: Backend Known Limitations & Scope Boundaries

## 1. Explicit Non-Goals (`DEC-06`)

The Ritucast backend explicitly enforces the following non-goals established in earlier phases:
1. **NO Parcel-Level Yield Predictions (`MOD-YLD-01`)**: The platform does not estimate kg/hectare crop yield or financial profits.
2. **NO Automated Chemical Prescriptions (`MOD-DIS-01`)**: The platform does not prescribe fungicides or chemical pesticides from satellite backscatter.
3. **NO Hardware Actuation**: The platform does not directly actuate motorized tubewell pumps or sluice gates.
4. **NO Commercial Brand Endorsements**: The platform does not promote specific commercial fertilizer or seed brands.

---

## 2. Geographic & Agricultural Scope Boundaries

1. **Dual Pilot Zones Only**: Active analytics are strictly calibrated for the two pilot testbeds:
   - High Barind Tract (Godagari, Tanore Upazilas in Rajshahi Division).
   - Haor Basin (Sunamganj Sadar, Tahirpur Upazilas in Sylhet Division).
   Requests for other Upazilas return `404 Not Found`.
2. **Anchor Crop Only**: Active agronomic equations ($K_c$, TAW, RAW) are calibrated exclusively for Boro rice (*Oryza sativa L.*). Other crops return calibration notices.

---

## 3. Operational & Technical Boundaries

1. **In-Memory Caching Boundary**: Processed tables are cached in memory for single-node instances. Distributed cache synchronization (e.g. Redis) is out of scope for Phase 10 MVP.
2. **Synchronous Execution**: All analytics calculations complete within $<5\text{ms}$; asynchronous Celery/Redis task queuing is unnecessary and omitted.
3. **Public Agricultural Advisory Access**: Advisory endpoints do not require user authentication tokens, optimizing for low-friction access by rural farmers and extension agents.

---

## 4. Related Documentation

- Architecture: [phase-10-backend-architecture.md](file:///Users/kazi/Projects/RITUCAST/docs/backend/phase-10-backend-architecture.md)
- Phase 11 Handoff: [handoff-to-phase-11.md](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-10/handoff-to-phase-11.md)
