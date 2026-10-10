# Ritucast: Project Risk Register

## 1. Risk Management Framework

The Ritucast Risk Register identifies, prioritizes, and outlines mitigation pathways across Product, Data, Scientific, Technical, and Operational/Adoption dimensions. 

- **Likelihood**: Low / Medium / High
- **Impact**: Low / Medium / Critical
- **Priority**: Likelihood $\times$ Impact (P1 = Urgent/Critical, P2 = Significant, P3 = Moderate, P4 = Low)

---

## 2. Master Risk Matrix

| Risk ID | Risk Description | Category | Likelihood | Impact | Priority | Mitigation Strategy | Investigation Timing | Approval Required? |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **RSK-01** | **Scope Creep / Over-Ambitious Initial Footprint**: Attempting national coverage and complex disease/yield prediction simultaneously. | Product | High | Critical | **P1** | Enforce Phase 1 boundaries: Dual-zone pilot focus (Barind + Haor); strict exclusion of yield prediction and direct pesticide diagnosis in initial release. | Phase 1 & 2 Quality Gates | Yes (Project Lead) |
| **RSK-02** | **Monsoon Cloud Cover Blinding Optical Sensors**: Optical sensors (MODIS, Sentinel-2) unusable for multi-week stretches during peak Aman season. | Data | High | Critical | **P1** | Architectural mandate: Core flood/waterlogging pipelines must utilize cloud-penetrating Sentinel-1 SAR and microwave rainfall (GPM IMERG), treating optical NDVI as secondary/dry-season auxiliary data. | Phase 3 (Dataset Validation) | No (Technical Consensus) |
| **RSK-03** | **Coarse Spatial Resolution vs Fragmented Smallholder Fields**: Coarse pixels (SMAP 9–36km, IMERG 10km) cannot resolve sub-acre plot boundaries, risking farmer disillusionment if presented with false micro-precision. | Scientific | High | Critical | **P1** | Explicitly frame indicators as *regional agro-climatic and catchment context*, not field-boundary readings. Implement transparent uncertainty disclaimers in UI. | Phase 4 (Knowledge) & Phase 6 (IA) | Yes (Lead Architect) |
| **RSK-04** | **Revisit Interval Latency in Flash-Flood Detection**: Sentinel-1 SAR has a 6–12 day revisit period over Bangladesh; rapid 24h flash floods in Haors could crest and recede between passes. | Scientific / Data | High | High | **P1** | Couple SAR satellite inundation with upstream GPM IMERG real-time precipitation tracking and BWDB river gauge trends to issue predictive hydrologic alerts ahead of satellite passes. | Phase 4 (Scientific Validation) | Yes (Science Lead) |
| **RSK-05** | **Overconfident / False Positive Advisories Eroding Farmer Trust**: Erroneously advising farmers to halt irrigation prior to rain that fails to materialize, resulting in crop moisture stress. | Scientific / Adoption | Medium | Critical | **P1** | Implement probabilistic thresholds; advisories clearly state confidence tiers (*High/Moderate/Low*). Recommendations suggest checking local soil condition and soil wetness directly before shutting pumps down. | Phase 9 (Recommendation Engine) | Yes (Agronomy Advisor) |
| **RSK-06** | **Low-End Android Device Performance & Memory Crashes**: Heavy GIS libraries (Mapbox GL JS, large GeoJSON files) overwhelm 2GB RAM budget phones. | Technical | High | High | **P2** | Architectural limit: Client-side JS bundle $<1.5\text{MB}$. Pre-render maps on backend into lightweight raster/vector tiles; prioritize simple card UI over continuous interactive map rendering. | Phase 5 (Architecture) & Phase 11 | No (Standard Engineering) |
| **RSK-07** | **Intermittent Rural Connectivity in Low-Lying Regions**: High latency or lost cellular signal during field visits prevents fetching live advisories. | Technical / Adoption | Medium | High | **P2** | Progressive Web App (PWA) offline caching with service workers. Cache the latest 3 days of upazila advisories locally on the device upon first connection. | Phase 11 (Frontend) & Phase 14 | No (Standard Engineering) |
| **RSK-08** | **Language, Terminology & Digital Literacy Friction**: Technical remote sensing terminology (e.g., "evapotranspiration", "anomaly") confuses farmers and SAAOs. | Adoption | High | High | **P2** | Co-design UI terminology with DAE field staff. Translate concepts into actionable agrarian idioms (e.g., "মাটির আর্দ্রতার ঘাটতি", "সেচের আবশ্যকতা"). | Phase 6 & Phase 7 | Yes (User Lead) |
| **RSK-09** | **Vendor API Deprecation or Rate-Limiting**: Free NASA / ESA APIs change auth schemas or throttle requests during bulk historical pulls. | Data / Technical | Medium | Medium | **P3** | Implement robust intermediate caching layer (PostGIS / Object Storage) with graceful backoff and retry mechanisms. Avoid direct live browser querying of external upstream APIs. | Phase 8 (Data Pipeline) | No (Engineering) |
| **RSK-10** | **Institutional Disconnect with DAE Extension Workflow**: SAAOs view Ritucast as an additional administrative burden rather than a time-saving decision tool. | Adoption / Operational | Medium | High | **P2** | Involve DAE SAAOs early in Phase 2 user journey mapping; ensure one-click advisory generation that aligns directly with DAE weekly block reporting needs. | Phase 2 & Phase 17 | Yes (Project Lead) |
| **RSK-11** | **Numerical Weather Ensemble Spread Divergence**: High disagreement among global weather models (GFS vs ECMWF vs GEM) leading to erratic 48h rain predictions. | Scientific / Technical | Medium | High | **P2** | Implement automated confidence decay and suppression rules (`FR-ADV-05`, `NFR-REL-03`); suppress recommendation when model spread exceeds 50%. | Phase 9 (Engine) & Phase 15 | Yes (Science Lead) |
| **RSK-12** | **Client-Side Canvas Image Export Failure on Legacy Android**: Older Android WebViews (Android 8–9) failing to render Bangla Unicode conjuncts during social share card generation. | Technical / UX | Medium | Medium | **P3** | Use server-side pre-rendered SVG/PNG card generation fallback or pure text WhatsApp share fallback (`FR-DSH-04`). | Phase 11 (Frontend) | No (Engineering) |

---

## 3. High-Priority Risk Escalation Protocol

1. Any risk evaluated at **P1** requires an explicit mitigation design document approved by the project lead prior to entering Phase 8 (Data Pipeline).
2. Risks that require human approval or involve significant operational trade-offs must be formally reviewed and logged in the [Decision Log](file:///Users/kazi/Projects/RITUCAST/docs/planning/decision-log.md).
