# Ritucast: Project-Wide Agent Operating Instructions (AGENTS.md)

## 1. Project Identity & Mission

**Ritucast** is an evidence-based agricultural intelligence and decision-support platform designed to transform satellite observations, numerical weather predictions, and soil-moisture data into localized, actionable, and explainable farming advice for smallholders and extension workers in Bangladesh.

All AI agents, engineers, and researchers operating in this repository must strictly adhere to the policies set forth in this document.

---

## 2. Core Governance Principles

### 2.1 The 18-Phase Governed Engineering Lifecycle
- Ritucast is engineered across an **18-phase sequential lifecycle** documented in [roadmap.md](file:///Users/kazi/Projects/RITUCAST/docs/planning/roadmap.md).
- **Sequential Phase Gating**: An agent may only execute the single phase explicitly requested by the user. Never prematurely execute subsequent phases.
- **Zero Premature Implementation**: Architecture, database schemas, API code, data pipelines, and UI prototyping are restricted to their assigned phases.
- **Quality Gates**: Every phase must conclude with a formal `validation-report.md` evaluating all acceptance criteria, an updated `deliverables-checklist.md`, and a formal `handoff-to-phase-XX.md`.

### 2.2 Dual-Zone Pilot Focus & Scope Boundaries
- **Geographic Testbeds**: The platform's initial release focuses exclusively on two representative pilot testbeds:
  1. **High Barind Tract** (Rajshahi Division: Godagari, Tanore Upazilas) for drought monitoring, groundwater deficit, and irrigation scheduling.
  2. **Haor Basin** (Sylhet Division: Sunamganj Sadar, Tahirpur Upazilas) for pre-monsoon transboundary flash floods and early harvest alerts.
- **Anchor Crop**: Boro rice (*Oryza sativa L.*).
- **Strict Non-Goals (`DEC-06`)**:
  - NO sub-acre parcel-level yield predictions (`MOD-YLD-01`).
  - NO automated chemical pesticide diagnoses from satellite data (`MOD-DIS-01`).
  - NO direct remote hardware actuators for tubewell pumps.
  - NO commercial brand endorsements or proprietary financial data ingestion.

---

## 3. Scientific Integrity & Agronomic Safety

### 3.1 Four-Tier Information Taxonomy (`DEC-08`)
All system outputs must be categorized and visually separated into:
1. **Tier 1: Empirical Observations (পর্যবেক্ষণ)**: Direct sensor readings (e.g., NASA solar radiation, BMD rainfall, Sentinel-1 SAR backscatter).
2. **Tier 2: Derived Agronomic Indicators (হিসাবকৃত সূচক)**: Physical transformations (e.g., FAO-56 Penman-Monteith $ET_0$, daily soil water deficit $D_t$, Haor flash-flood hazard index $I_{\text{flood}}$).
3. **Tier 3: Probabilistic Predictions (পূর্বাভাস)**: Model forecasts with explicit probabilities and confidence bands (e.g., 48h rainfall probability, temperature range).
4. **Tier 4: Actionable Recommendations (পরামর্শ)**: Synthesized operational guidance (e.g., postpone irrigation, prepare emergency harvest) with plain-language explanations.

### 3.2 Mandatory Contextual Gating (`DEC-17`)
No recommendation card may be generated without verified confirmation of:
1. Administrative Upazila.
2. Active Crop.
3. Active Phenological Growth Stage.

### 3.3 Automated Suppression Policy (`DEC-10`)
Advisories must be automatically suppressed and a safe fallback notice displayed whenever:
- Weather forecast or satellite data is $>36\text{ hours}$ old (`NFR-REL-03`).
- Multi-model NWP ensemble spread exceeds $50\%$ with rain probability between $40\%$ and $60\%$.
- Input variables violate physical range checks.

### 3.4 Anti-Overconfidence Linguistic Standards
- Banned terms: *"১০০% নিশ্চিত"*, *"নিশ্চিত বৃষ্টি"*, *"ফলনের নিশ্চয়তা"*.
- Mandatory field verification copy must accompany every advisory: *"সেচ বন্ধ করার আগে জমির আইল এবং মাটির রস নিজে হাত দিয়ে পরীক্ষা করুন।"*

---

## 4. Engineering & Technical Standards

### 4.1 Client Hardware & Payload Budgets (`DEC-09`)
- Rural target users operate budget Android smartphones (2GB–3GB RAM, Android 8+) on variable 3G cellular networks.
- Initial client JS/CSS bundle size: $\le 1.5\text{MB}$.
- Time-to-Interactive (TTI) on 3G: $\le 3.5\text{s}$.
- Peak client heap memory: $\le 45\text{MB}$.
- Zero direct browser querying of external upstream APIs; all traffic flows through an intermediate caching backend.

### 4.2 Documentation & Link Conventions
- **Clickable File Links**: Every reference to a project file must use the GitHub markdown link syntax with the `file://` scheme and absolute paths:
  - Example: `[roadmap.md](file:///Users/kazi/Projects/RITUCAST/docs/planning/roadmap.md)`
- **Traceable Identifiers**: Maintain consistent stable IDs across all phases:
  - Functional Requirements: `FR-LOC-01`, `FR-ENV-01`, `FR-ADV-01`, `FR-DSH-01`, `FR-UX-01`
  - Non-Functional Requirements: `NFR-USE-01`, `NFR-PER-01`, `NFR-REL-01`, `NFR-SEC-01`, `NFR-SCI-01`
  - Datasets: `DATA-MET-01`, `DATA-FCST-01`, `DATA-PCP-01`, `DATA-SAR-01`, `DATA-SMC-01`, `DATA-AGR-01`, `DATA-BND-01`, `DATA-HYD-01`
  - Rules & Equations: `RULE-IRR-01`, `RULE-FLD-01`, `EQN-ET0-01`, `EQN-SWD-01`, `IDX-FLD-01`
  - Risks & Assumptions: `RSK-01` to `RSK-18`, `ASM-01` to `ASM-11`, `DEC-01` to `DEC-18`

### 4.3 Git & Change Management
- Maintain atomic, conventional commits (e.g., `docs(phase-X): description`).
- Never force-push, rewrite Git history, or reset `main`.
- Never commit raw geospatial satellite files (`.tif`, `.nc`, `.parquet`) or credentials/secrets.
