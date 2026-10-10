# ADR-08: Automated Suppression Middleware Service for Scientific Safety

## 1. Status
**Approved** (2026-10-10)

## 2. Context
In smallholder agriculture, delivering stale, corrupted, or highly uncertain predictions as active farming advice risks severe economic damage (e.g., advising a farmer to turn off an irrigation pump before a phantom rain event, causing spikelet sterility). Phase 2 and Phase 4 established non-negotiable safety policies (`DEC-10`, `NFR-REL-03`, `ARC-CON-02`) requiring automated suppression when data is stale or models disagree.

We evaluated:
1. *Client-side suppression logic in React components.*
2. *Ad-hoc suppression checks scattered across individual route handlers.*
3. *Centralized Backend Middleware Service (Selected).*

## 3. Decision
We adopt a centralized **Automated Suppression Middleware Service** integrated into the FastAPI request lifecycle prior to advisory payload serialization:
- Intercepts all advisory generation requests.
- Inspects the ingestion timestamp of the underlying meteorological and hydrological feeds.
- If the latest weather forecast observation is **$>36\text{ hours}$ old**, hard suppression is triggered.
- If multi-model NWP ensemble spread ($S_{\text{spread}}$) between ECMWF IFS and NOAA GFS exceeds **$50\%$** with rain probability between $40\%$ and $60\%$, active postponement cards are withheld.
- Emits a standard localized fallback notice in Bangla directing the user to inspect their field soil manually and consult their local SAAO.

## 4. Rationale & Trade-Offs
- **Zero-Bypass Architecture**: Centralized middleware guarantees that no frontend client or third-party consumer can accidentally receive an un-suppressed, dangerous advisory when data feeds are degraded.
- **Fail-Safe by Default**: If an unexpected exception occurs inside the advisory calculation engine, the middleware catches the error and gracefully falls back to the safe monitoring state rather than returning a 500 server crash or hallucinated advice.
- **Centralized Audit Logging**: Every suppression event is logged with structured metadata, allowing the observability service to alert engineers if more than $20\%$ of upazilas are simultaneously suppressed.

## 5. Revisit Triggers
This decision will be revisited if:
- Advanced local weather radar networks (BMD automated radars in Moulvibazar/Rangpur) are integrated, providing hyper-local real-time observations that reduce the staleness suppression ceiling from 36 hours to 12 hours.
