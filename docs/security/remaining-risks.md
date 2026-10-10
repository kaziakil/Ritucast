# Remaining Risks and Post-Phase 15 Security Follow-Up — Ritucast

## 1. Overview

While Phase 15 successfully remediated all identified critical, high, and medium application vulnerabilities, certain residual operational risks, architectural trade-offs, and external dependencies remain. This document transparently records these residual risks, explains their mitigating controls, and outlines follow-up actions for future phases.

---

## 2. Residual Risk Register

| Risk ID | Category | Summary & Description | Residual Severity | Mitigating Factors & Controls | Follow-up Phase / Action |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `RSK-SEC-01` | Infrastructure | In-memory rate limiting is node-local; autoscaling multiple Cloud Run instances scales effective threshold per instance | Low | Average traffic is well within Cloud Run single-instance capacity (concurrency: 80); Cloud Armor or API Gateway can enforce edge rate limits if public traffic spikes | Phase 16 / Cloud Armor edge configuration |
| `RSK-SEC-02` | Supply Chain | Starlette 0.46.2 transitive advisories flagged by pip-audit (multipart/websockets) | Low | Affected code paths (file uploads, WebSockets, Range static serving) are not implemented in Ritucast | Monitor FastAPI minor releases (`0.116.0+`) for updated Starlette pin |
| `RSK-SEC-03` | Scientific / Data | Upstream NASA POWER or Open-Meteo API outages lasting $>36\text{ hours}$ trigger advisory suppression | Low | Automatic suppression protects agronomic safety (`DEC-10`); daily smoke cron (`live-data-smoke.yml`) monitors source availability | Phase 17 (Ground-truth sensor calibration with BMD) |
| `RSK-SEC-04` | Usability / Adoption | Low-literacy smallholders may overlook field soil moisture verification disclaimer | Medium | Plain-language Bengali typography, high-contrast visual status cards, and SAAO extension agent mediation | Phase 16 (Usability, Accessibility & SAAO Field Testing) |
| `RSK-SEC-05` | Geospatial | Regional Upazila mean indicators may diverge from micro-climatic or soil-texture anomalies within an Upazila | Medium | Mandatory field verification copy; clear labeling as Upazila regional average (`উপজেলা গড়`); non-parcel disclaimer | Phase 17 (Empirical validation against field soil samples) |

---

## 3. Operational Monitoring & Escalation

1. **Vulnerability Alerts**: Dependabot and GitHub Actions CI security scanning alert the engineering team when new CVEs are published affecting direct dependencies.
2. **Cloud Run Logging**: Abnormal 429 rate limit rejections or 413 payload rejections generate operational logs in Google Cloud Logging with structured severity labels.
3. **Emergency Advisory Halt**: If an upstream meteorological bug causes erroneous weather inputs, administrators can toggle `MAX_WEATHER_AGE_HOURS=0.0` or deploy an updated Parquet manifest to immediately suppress all active advisories without code modification.

Related documentation:
- [`docs/security/security-findings-register.md`](file:///Users/kazi/Projects/RITUCAST/docs/security/security-findings-register.md)
- [`docs/security/security-remediation-record.md`](file:///Users/kazi/Projects/RITUCAST/docs/security/security-remediation-record.md)
- [`docs/responsible-ai/appropriate-use-and-misuse-prevention.md`](file:///Users/kazi/Projects/RITUCAST/docs/responsible-ai/appropriate-use-and-misuse-prevention.md)
