# Threat Model & Risk Assessment — Ritucast

## 1. System Context & Overview

**Ritucast** provides localized agro-meteorological advisories across the High Barind Tract and Haor Basin testbeds in Bangladesh. To evaluate and manage security risks effectively, this threat model utilizes the STRIDE methodology (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege) tailored to Ritucast's serverless micro-architecture and public decision-support scope.

---

## 2. Assets Inventory

Only assets genuinely stored, processed, or exposed by Ritucast are included:

| Asset ID | Asset Name | Description | Confidentiality | Integrity | Availability |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `AST-01` | **Application Source Code** | Python backend, React frontend, analytics algorithms, rules | Public / Open | High | High |
| `AST-02` | **Runtime Configuration** | Environment variables, `.env.production`, CORS rules | High | High | High |
| `AST-03` | **API Service Endpoints** | FastAPI routes under `/api/v1/`, health probes | Low (Public) | High | High |
| `AST-04` | **Processed Parquet Tables** | Pre-computed Upazila daily meteorology, forecast tables | Low (Open Data) | High | High |
| `AST-05` | **Advisory Algorithms & Rules** | Phase 9 agronomic rules (`RULE-IRR-01` to `RULE-TMP-02`) | Low (Documented) | Critical | High |
| `AST-06` | **Client Application Bundle** | Compiled SPA static assets served via NGINX | Low (Public) | High | High |
| `AST-07` | **Deployment Credentials** | GCP Service Account keys, GitHub Actions Secrets | Critical | Critical | High |
| `AST-08` | **Agricultural Advice Outputs** | 4-Tier decision-support payloads consumed by farmers | Public | Critical | High |

---

## 3. Threat Actors & Scenarios

| Actor ID | Actor Category | Motivation & Capability | Likely Vectors |
| :--- | :--- | :--- | :--- |
| `ACT-01` | **Automated Script / Web Crawler** | High-volume scraping, endpoint abuse, resource exhaustion | Rapid-fire GET requests, DoS against Cloud Run container |
| `ACT-02` | **Malicious API Client** | Malformed payloads, SQL/command injection, path traversal | POST payloads to `/evaluate`, traversal sequences in URLs |
| `ACT-03` | **Compromised Upstream Service** | Data corruption, out-of-range sensor readings | Corrupted precipitation or radiation data from external APIs |
| `ACT-04` | **Third-Party Site / Phishing** | Clickjacking, cross-origin request forging (CSRF/CORS) | Embedding Ritucast inside unauthorized iframes, cross-origin fetch |
| `ACT-05` | **Agronomic Misinterpreter** | Misapplying regional estimates to parcel decisions | Treating regional satellite index as single-field sensor reading |

---

## 4. STRIDE Threat Analysis Matrix

| Threat ID | STRIDE Category | Target Asset | Attack Scenario | Existing & Implemented Controls | Residual Risk |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `TR-01` | **Spoofing** | API Endpoints (`AST-03`) | Attacker spoofs upstream weather data to inject false storm signals | Data validation pipeline ([`pipelines/validation/`](file:///Users/kazi/Projects/RITUCAST/pipelines/validation)) checks physical bounds; API relies on pre-processed signed Parquet | Low |
| `TR-02` | **Tampering** | Parquet Tables (`AST-04`) | Attacker attempts path traversal (`../`) via endpoint parameters to alter or read system files | Strict path traversal guard in [`AgriculturalDataRepository.load_parquet_table`](file:///Users/kazi/Projects/RITUCAST/api/data_access/repository.py#L192) rejects `..`, `/`, `\`; allowlist validation enforced | Low |
| `TR-03` | **Repudiation** | System Actions | Client claims erroneous advisory was issued | Provenance tracking endpoint (`/api/v1/provenance`) records dataset version, algorithm hash, and UTC timestamp | Low |
| `TR-04` | **Information Disclosure** | Config & System (`AST-02`) | Server crashes and leaks full stack traces or environment variables to client | Centralized exception handler in [`api/middleware/error_handlers.py`](file:///Users/kazi/Projects/RITUCAST/api/middleware/error_handlers.py#L109) sanitizes all 500 errors to a generic error envelope | Low |
| `TR-05` | **Information Disclosure** | PII / Farm Data | User location or sensitive farmer identity leaked | Zero PII collected; queries accept only administrative Upazila codes; no user accounts or database | Very Low |
| `TR-06` | **Denial of Service** | API Availability (`AST-03`) | High-frequency bot flood exhausts Cloud Run instance memory or concurrency | [`RateLimitMiddleware`](file:///Users/kazi/Projects/RITUCAST/api/middleware/security.py) (60 req/min sliding window); [`RequestSizeLimitMiddleware`](file:///Users/kazi/Projects/RITUCAST/api/middleware/security.py) (1 MB ceiling) | Low |
| `TR-07` | **Elevation of Privilege** | Container Sandbox | Attacker exploits dependency vulnerability to gain root execution inside container | Multi-stage Dockerfile ([`deploy/docker/Dockerfile.backend`](file:///Users/kazi/Projects/RITUCAST/deploy/docker/Dockerfile.backend)) enforces unprivileged `appuser` (UID 10001); read-only `/app` filesystem | Low |

---

## 5. Qualitative Risk Scoring Methodology

Risks are assessed qualitatively based on Likelihood and Impact:
- **Likelihood**: Rare, Unlikely, Moderate, Likely, Almost Certain.
- **Impact**: Negligible, Minor, Moderate, Major, Catastrophic.
- **Risk Tiers**:
  - **Critical**: Severe application compromise, credential disclosure, or widespread agronomic damage.
  - **High**: Significant operational degradation, unvalidated advice delivery, or supply-chain compromise.
  - **Medium**: Moderate weakness with existing mitigating controls.
  - **Low / Informational**: Minor hardening or documentation improvement.

---

## 6. Responsible AI & Misuse Risk Scenarios

Beyond software security, Ritucast addresses agronomic safety threats:

### 6.1 Overconfidence & Agronomic Hazard (`RSK-AI-01`)
- **Threat**: Farmer blindly follows a "POSTPONE_IRRIGATION" recommendation without checking field soil moisture, resulting in root drought damage during Boro panicle initiation.
- **Control**: Mandatory copy standard (`DEC-10`, `DEC-17`):
  *"সেচ বন্ধ করার আগে জমির আইল এবং মাটির রস নিজে হাত দিয়ে পরীক্ষা করুন।"*
  Prohibition of banned deterministic words: *"১০০% নিশ্চিত"*, *"নিশ্চিত বৃষ্টি"*, *"ফলনের নিশ্চয়তা"*.

### 6.2 Stale Data Hazard (`RSK-AI-02`)
- **Threat**: Satellite soil moisture or numerical weather predictions become $>36\text{ hours}$ old due to upstream API outage, generating out-of-date advice.
- **Control**: Automated Suppression Policy (`DEC-10`) intercepts cards when `data_timestamp_utc` exceeds 36 hours and displays a safe fallback notice.

### 6.3 Misuse in Financial Underwriting (`DEC-06`, `RSK-AI-03`)
- **Threat**: Micro-lenders or commercial crop insurers utilize Ritucast's hazard index (`I_flood`, soil deficit) to deny loans or claim eligibility to individual farmers.
- **Control**: Explicit API response disclaimer:
  *"এই মূল্যায়ন শুধুমাত্র প্রাকৃতিক পরিবেশগত ঝুঁকির নির্দেশক; এটি আর্থিক ক্ষতি বা চূড়ান্ত ফলন হ্রাসের নিশ্চয়তা দেয় না।"*

Related documentation:
- [`docs/security/security-boundaries.md`](file:///Users/kazi/Projects/RITUCAST/docs/security/security-boundaries.md)
- [`docs/security/api-security.md`](file:///Users/kazi/Projects/RITUCAST/docs/security/api-security.md)
- [`docs/responsible-ai/agricultural-recommendation-safeguards.md`](file:///Users/kazi/Projects/RITUCAST/docs/responsible-ai/agricultural-recommendation-safeguards.md)
