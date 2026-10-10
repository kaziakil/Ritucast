# Ritucast: Non-Functional Requirements Specification (NFR)

## 1. Specification Framework

Non-functional requirements define the operational qualities, architectural constraints, safety boundaries, and performance budgets for Ritucast. Every requirement is assigned a stable identifier (`NFR-XXX-##`) and explicit testable verification thresholds.

---

## 2. Requirements Matrix by Category

---

### Category 1: Usability & Comprehensibility

#### `NFR-USE-01`: Low Digital Literacy Ergonomics
- **Definition**: The user interface must employ a card-based visual hierarchy requiring zero training for farmers and extension officers. Primary action cards must be readable without horizontal or vertical scrolling on standard 720p mobile viewports.
- **Priority**: **P0 (Foundational)**
- **Verification Method**: Structured usability testing with 10 SAAOs and lead farmers.
- **Target Threshold**: $\ge 85\%$ task success on initial exposure without moderator assistance.

#### `NFR-USE-02`: Agronomic Terminology Consistency (Bangla)
- **Definition**: All Bangla terminology must strictly align with Department of Agricultural Extension (DAE) and Bangladesh Rice Research Institute (BRRI) official extension glossaries. Technical English jargon (e.g., *albedo, evapotranspiration, raster, NDVI*) is strictly prohibited on farmer-facing screens.
- **Priority**: **P0 (Foundational)**
- **Verification Method**: Review of UI copy by an agronomist and native Bangla agricultural translator.
- **Target Threshold**: 100% compliance with DAE standard vocabulary (e.g., *"মাটির আর্দ্রতা"*, *"ফসলের পানির চাহিদা"*, *"সেচ স্থগিতকরণ"*).

#### `NFR-USE-03`: Explainability Discoverability
- **Definition**: The "কেন এই পরামর্শ?" (Why this advice?) button must be prominently displayed directly on every active advisory card and open in $<200\text{ms}$.
- **Priority**: **P1 (Essential)**
- **Verification Method**: Automated UI interaction latency audit.
- **Target Threshold**: Drawer opening animation $<200\text{ms}$ on low-end mobile devices.

---

### Category 2: Accessibility & Inclusivity

#### `NFR-ACC-01`: High-Contrast Outdoor Legibility (Sunlight Readability)
- **Definition**: Since farmers and SAAOs use devices outdoors in direct sunlight, all text and UI elements must maintain high contrast ratios compliant with WCAG 2.1 AA.
- **Priority**: **P0 (Foundational)**
- **Verification Method**: Automated Lighthouse Accessibility audits and outdoor contrast meter tests.
- **Target Threshold**: Contrast ratio $\ge 4.5:1$ for normal body text; $\ge 3.0:1$ for large text and alert banners.

#### `NFR-ACC-02`: Non-Color-Only Hazard Communication
- **Definition**: All risk and advisory states (Emergency Alert, Postpone Irrigation, Safe Window) must never rely solely on color (red, amber, green) to convey meaning. They must pair distinct SVG iconography and clear bold text badges.
- **Priority**: **P0 (Foundational / Safety)**
- **Verification Method**: Grayscale / color-blindness simulation testing (Protanopia, Deuteranopia).
- **Target Threshold**: 100% of risk cards identifiable in complete grayscale mode.

#### `NFR-ACC-03`: Font Legibility on Budget Displays
- **Definition**: Use modern, clean Unicode Bangla fonts (e.g., Noto Sans Bengali or Tiro Bangla) optimized for low-DPI 720p screens. Minimum body font size must be $16\text{px}$ to prevent eye strain.
- **Priority**: **P1 (Essential)**
- **Verification Method**: Multi-device physical screen inspection.
- **Target Threshold**: Zero overlapping glyphs or broken conjuncts (*যুক্তবর্ণ*).

---

### Category 3: Performance & Resource Budgets

#### `NFR-PERF-01`: Initial Client Bundle Size Budget
- **Definition**: The total compressed JavaScript and CSS payload transmitted to the client for the initial dashboard render must not exceed $1.5\text{MB}$.
- **Priority**: **P0 (Foundational)**
- **Verification Method**: Webpack / Vite build bundle analyzer in CI/CD pipeline.
- **Target Threshold**: $\text{Total Gzipped Asset Bundle} \le 1.5\text{MB}$.

#### `NFR-PERF-02`: Time-to-Interactive (TTI) on Throttled 3G
- **Definition**: The application must reach Time-to-Interactive (TTI) within $3.5\text{ seconds}$ under a simulated slow 3G cellular network ($400\text{Kbps}$ down, $400\text{ms}$ RTT).
- **Priority**: **P1 (Essential)**
- **Verification Method**: Automated Google Lighthouse CI tests on every build.
- **Target Threshold**: $\text{TTI} \le 3.5\text{s}$; $\text{First Contentful Paint (FCP)} \le 1.8\text{s}$.

#### `NFR-PERF-03`: Client-Side Memory Footprint on 2GB RAM Devices
- **Definition**: The browser runtime memory heap allocated by the application must remain lightweight to avoid OS kills on low-RAM (2GB–3GB) Android phones.
- **Priority**: **P1 (Essential)**
- **Verification Method**: Chrome DevTools Memory Profiler on low-end device emulator.
- **Target Threshold**: Peak memory heap $\le 45\text{MB}$ during active map interactions and drawer transitions.

---

### Category 4: Reliability & Data Degradation

#### `NFR-REL-01`: Graceful Offline Operation & Local Caching
- **Definition**: When cellular connectivity drops in rural fields, the Progressive Web App (PWA) must load the most recently fetched Upazila advisory from IndexedDB/localStorage with an explicit "অফলাইন মোড" badge and timestamp.
- **Priority**: **P0 (Foundational)**
- **Verification Method**: Offline network simulation tests (Service Worker offline pass).
- **Target Threshold**: 100% of previously loaded screens navigable without an active network connection.

#### `NFR-REL-02`: Upstream API Degradation & Circuit Breaking
- **Definition**: If an upstream data provider (e.g., NASA POWER, ESA CDSE) fails or times out, the system must not crash or display empty screens. It must serve cached data up to 48 hours old with a prominent data freshness warning.
- **Priority**: **P0 (Foundational)**
- **Verification Method**: Chaos testing by simulating 100% upstream API failure.
- **Target Threshold**: Zero 500-series unhandled errors exposed to end users.

#### `NFR-REL-03`: Data Staleness Hard Ceiling
- **Definition**: If weather or satellite observations are older than 36 hours, the system must automatically suppress definitive operational recommendations (e.g., Postpone Irrigation) and display an advisory: *"তথ্য হালনাগাদ করা সম্ভব হয়নি। সিদ্ধান্ত নেয়ার আগে স্থানীয় উপ-সহকারী কৃষি কর্মকর্তার সাথে যোগাযোগ করুন।"* (Data could not be updated. Consult local SAAO before deciding).
- **Priority**: **P0 (Foundational / Safety)**
- **Verification Method**: Automated unit test with simulated stale pipeline timestamps.
- **Target Threshold**: 100% suppression of stale automated recommendations.

---

### Category 5: Security & Privacy by Design

#### `NFR-SEC-01`: Zero Mandatory Personal Data Collection
- **Definition**: The initial release of Ritucast requires zero user registration, phone number collection, or national identity logging to access agricultural advisories.
- **Priority**: **P0 (Foundational)**
- **Verification Method**: Code audit and privacy compliance review.
- **Target Threshold**: Zero PII (Personally Identifiable Information) captured or transmitted.

#### `NFR-SEC-02`: Secure Transport & Input Sanitization
- **Definition**: All communication must enforce HTTPS/TLS 1.3. All administrative query parameters and geocoding inputs must be validated and sanitized against injection attacks.
- **Priority**: **P0 (Foundational)**
- **Verification Method**: OWASP ZAP automated security scan in CI.
- **Target Threshold**: Zero high or critical security vulnerabilities.

---

### Category 6: Maintainability & Code Quality

#### `NFR-MNT-01`: Decoupled Modular Architecture
- **Definition**: Ingestion pipelines, agronomic analytics, backend APIs, and frontend interfaces must be strictly decoupled through stable, documented API contracts (OpenAPI 3.0).
- **Priority**: **P1 (Essential)**
- **Verification Method**: Architectural code review and contract testing.
- **Target Threshold**: Ingestion engine can be modified without altering frontend client code.

#### `NFR-MNT-02`: Reproducible Development & Containerization
- **Definition**: All services must be fully reproducible via standard Docker containers with zero undocumented host dependencies.
- **Priority**: **P1 (Essential)**
- **Verification Method**: Clean clone and container build test on fresh environment.
- **Target Threshold**: Container build passes in $\le 5$ minutes with zero manual intervention.

---

### Category 7: Scientific Integrity & Attribution

#### `NFR-SCI-01`: Strict Separation of Information Types
- **Definition**: The UI must enforce visual and textual separation between:
  1. *পরিমাপকৃত উপগ্রহ পর্যবেক্ষণ (Measured Observations)*
  2. *গাণিতিক পূর্বাভাস (Forecast Models)*
  3. *কৃষি সিদ্ধান্ত ও পরামর্শ (Synthesized Recommendations)*
- **Priority**: **P0 (Foundational / Safety)**
- **Verification Method**: Agronomic UI audit.
- **Target Threshold**: 100% compliance across all advisory views.

#### `NFR-SCI-02`: Full Provenance Attribution
- **Definition**: Every data card must explicitly cite the data provider mission and update timestamp (e.g., NASA POWER, Sentinel-1 SAR, BMD, BRRI).
- **Priority**: **P1 (Essential)**
- **Verification Method**: Automated snapshot testing of all view templates.
- **Target Threshold**: 100% of data cards contain verified attribution metadata.

#### `NFR-SCI-03`: No False Causal Claims
- **Definition**: The system copy and advisory rules must never claim that following an advisory "guarantees" specific yields or financial windfalls. Language must reflect agronomic risk reduction (e.g., *"ঝুঁকি হ্রাস"*).
- **Priority**: **P0 (Foundational / Safety)**
- **Verification Method**: Legal and agronomic copy review.
- **Target Threshold**: Zero unqualified yield or monetary guarantees.

---

## 3. Summary of NFRs by Category

| Category | Requirement Count | Stable IDs |
| :--- | :---: | :--- |
| **Usability** | 3 | `NFR-USE-01`, `NFR-USE-02`, `NFR-USE-03` |
| **Accessibility** | 3 | `NFR-ACC-01`, `NFR-ACC-02`, `NFR-ACC-03` |
| **Performance** | 3 | `NFR-PERF-01`, `NFR-PERF-02`, `NFR-PERF-03` |
| **Reliability** | 3 | `NFR-REL-01`, `NFR-REL-02`, `NFR-REL-03` |
| **Security & Privacy** | 2 | `NFR-SEC-01`, `NFR-SEC-02` |
| **Maintainability** | 2 | `NFR-MNT-01`, `NFR-MNT-02` |
| **Scientific Integrity** | 3 | `NFR-SCI-01`, `NFR-SCI-02`, `NFR-SCI-03` |
| **Total Non-Functional Requirements** | **19** | |
