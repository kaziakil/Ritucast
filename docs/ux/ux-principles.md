# Ritucast UX Design Principles

## 1. Purpose and Governance

The Ritucast User Experience (UX) Design Principles define the fundamental interaction standards, cognitive models, and ethical guidelines that govern how agricultural intelligence is organized and presented.

Every screen, flow, card, and interaction pattern designed in [Phase 6: Information Architecture](file:///Users/kazi/Projects/RITUCAST/docs/phases/phase-06/phase-plan.md) and styled in Phase 7 must comply with these 12 binding principles.

---

## 2. The 12 UX Design Principles

### 2.1 Farmer-Centered
- **Definition**: Prioritize practical, immediate farming operational questions over data science, remote sensing terminology, or academic abstractions.
- **In Practice**: Use plain Bangla agricultural idioms (e.g., *"মাটিতে রসের ঘাটতি"*, *"সেচ দেওয়া প্রয়োজন"*) rather than raw sensor metrics (e.g., *"Volumetric Soil Water Content $0.18\text{ m}^3/\text{m}^3$*"). Lead with what the condition means for today's crop management.
- **Compliance Evaluation**: Can a farmer identify the immediate farming implication within 5 seconds of viewing the card without technical assistance?

### 2.2 Action-Oriented
- **Definition**: Connect every environmental observation to a clear, actionable operational next step or verified reason for holding.
- **In Practice**: Never present an observation in isolation (e.g., "35mm rain expected") without connecting it to farming operations (e.g., "Postpone pump irrigation for 48 hours; clear drainage channels").
- **Compliance Evaluation**: Does every insight card feature a primary action badge, operational suggestion, or a documented reason why no action is needed?

### 2.3 Evidence-Based
- **Definition**: Strictly separate empirical sensor observations, derived physical indicators, probabilistic model forecasts, and operational recommendations into visual tiers.
- **In Practice**: Adhere to the Four-Tier Information Taxonomy (`DEC-08`). Clearly label whether a value is an empirical reading from a ground station/satellite (Tier 1), a calculated water balance index (Tier 2), a multi-model forecast (Tier 3), or synthesized operational advice (Tier 4).
- **Compliance Evaluation**: Are the four information tiers rendered with distinct visual containers, typographic treatments, and category headers?

### 2.4 Scientifically Responsible
- **Definition**: Never present uncertain, unverified, or coarse-resolution data as a definitive field-level fact.
- **In Practice**: Enforce the "Do No Harm" agronomic policy (`DEC-10`). Avoid banned terms like *"১০০% নিশ্চিত"* or *"ফলনের নিশ্চয়তা"*. Include mandatory field-verification copy: *"সেচ বন্ধ করার আগে জমির আইল এবং মাটির রস নিজে হাত দিয়ে পরীক্ষা করুন।"*
- **Compliance Evaluation**: Does any text promise guaranteed yield or field-level certainty? (Must be zero instances). Is the mandatory field verification copy present on all Tier 4 cards?

### 2.5 Accessible
- **Definition**: Ensure the interface is operable by users across varying digital literacy, visual acuity, language proficiency, device specifications, and physical abilities.
- **In Practice**: Meet WCAG 2.2 Level AA requirements. Enforce minimum 48x48px touch targets, 4.5:1 text contrast ratios, high-legibility Bangla Unicode typography, and non-color-only state indicators (pair colors with clear iconography and text labels).
- **Compliance Evaluation**: Can all critical tasks be completed via keyboard navigation and screen readers? Do all interactive elements meet touch-target and contrast thresholds?

### 2.6 Geographically Relevant
- **Definition**: Reflect Bangladesh's verified administrative divisions (Upazilas) and agro-ecological zones (AEZs) accurately.
- **In Practice**: Anchor user context strictly to supported administrative boundaries (e.g., Godagari, Tanore in Barind; Sunamganj Sadar, Tahirpur in Haor). Never show generic national weather as localized advice.
- **Compliance Evaluation**: Is the active administrative Upazila clearly visible and easily switchable at the top of every advisory screen?

### 2.7 Transparent
- **Definition**: Show data sources, observation timestamps, processing latency, and limitations openly.
- **In Practice**: Include an expandable "তথ্যসূত্র ও বিস্তারিত" (Sources & Details) section on every indicator card displaying the sensor origin (e.g., BMD, NASA POWER, Sentinel-1 SAR), observation timestamp, and data freshness.
- **Compliance Evaluation**: Can a user verify the exact source and observation age of every displayed metric within one tap?

### 2.8 Responsive
- **Definition**: Optimize the user experience seamlessly across budget Android mobile smartphones (primary), tablets, and desktop workstations.
- **In Practice**: Mobile-first layout prioritizing stacked cards on 360px–420px viewport widths. Multi-column grid expansions on desktop for agricultural officers and researchers.
- **Compliance Evaluation**: Does the entire advisory interface function flawlessly on a 360px wide screen without horizontal scrolling or overlapping elements?

### 2.9 Consistent
- **Definition**: Use predictable navigation models, standard terminology, recurring card layouts, and uniform status patterns across the entire product.
- **In Practice**: Reusable card templates across all modules (Header, Metric/Status, Plain Bangla Explanation, Action Badge, Source Footer). Identical iconography and color coding for severity across Barind and Haor modules.
- **Compliance Evaluation**: Do all module cards adhere to the standardized 5-section card architecture?

### 2.10 Progressively Disclosed
- **Definition**: Present essential operational summaries first; provide deep technical and scientific details on demand without cluttering the primary view.
- **In Practice**: The primary dashboard presents high-level operational advice (Tier 4) and critical alerts. Detailed soil water depletion curves, evapotranspiration math, and raw satellite metadata are tucked into expandable drawers or dedicated diagnostic tabs.
- **Compliance Evaluation**: Can a farmer complete their daily decision flow without viewing complex equations or raw remote sensing parameters?

### 2.11 Trustworthy
- **Definition**: Avoid false precision, arbitrary risk scores, and hidden algorithmic bias. Build long-term farmer confidence through honesty.
- **In Practice**: Display satellite resolutions accurately (e.g., note that satellite soil moisture reflects regional 10km grid trends, not sub-acre plot boundaries). Automatically suppress advisories and display safe fallback notices when forecast confidence drops (`DEC-10`).
- **Compliance Evaluation**: When upstream forecast uncertainty exceeds 50%, does the interface gracefully suppress advice and display the safe manual-verification message?

### 2.12 Extensible
- **Definition**: Design navigation and information structures that accommodate new crops, regions, and environmental layers without requiring a complete redesign.
- **In Practice**: Use modular card grids and dynamic filter selectors rather than hardcoded dual-zone tabs. Ensure the information architecture can accommodate future coastal salinity or floodplains modules seamlessly.
- **Compliance Evaluation**: Can a new crop (e.g., Wheat, Mustard) or a new Upazila be introduced into the navigation model without breaking the layout?

---

## 3. Compliance & Governance Matrix

| UX Principle | Primary Enforcer | Audit Milestone | Automated vs Manual |
| :--- | :--- | :--- | :--- |
| **Farmer-Centered** | UX Architect / SAAO Review | Phase 6 & Phase 14 | Manual (User comprehension testing) |
| **Action-Oriented** | Product Manager | Phase 6 (Page Specs) | Manual (Card audit) |
| **Evidence-Based** | Science Lead | Phase 6 & Phase 9 | Automated (Schema validation) & Manual |
| **Scientifically Responsible** | Scientific Advisory Board | Phase 6 & Phase 13 | Automated (Linguistic linting for banned terms) |
| **Accessible** | Frontend Lead | Phase 7 & Phase 11 | Automated (axe-core / Lighthouse WCAG audit) |
| **Geographically Relevant** | Geospatial Architect | Phase 6 & Phase 10 | Automated (Upazila context gating check) |
| **Transparent** | Data Platform Lead | Phase 6 (Card Specs) | Automated (Pydantic provenance validation) |
| **Responsive** | Frontend Lead | Phase 7 & Phase 11 | Automated (Viewport testing across breakpoints) |
| **Consistent** | Design System Lead | Phase 7 (Design System) | Manual (Design token review) |
| **Progressively Disclosed** | Interaction Designer | Phase 6 (User Journeys) | Manual (Click-depth analysis) |
| **Trustworthy** | Science Lead | Phase 6 & Phase 15 | Automated (Suppression test suite) |
| **Extensible** | Full-Stack Architect | Phase 6 (Sitemap) | Manual (Architecture review) |
