# Frontend Information Architecture & Navigation

## 1. Overview

Ritucast's information architecture is structured to facilitate rapid operational decision-making by farmers and extension officers under variable field and connectivity conditions. Rather than overwhelming users with raw geospatial raster layers or dense tables, the UI translates scientific data into prioritized, action-oriented views anchored by the **Contextual Selection Gate** (`DEC-17`).

---

## 2. Navigation Structure

The application features a single-page view structure organized into 5 primary operational sections:

```
RITUCAST WEB APPLICATION
│
├── [Sticky Context Bar] (Location + Crop + Phenological Stage Selection)
│
├── 1. পরামর্শ কেন্দ্র (Advisory Hub - Default View)
│    ├── Automated Suppression Banner (Conditional - DEC-10)
│    ├── Primary Action Recommendation (Tier 4 Directive)
│    ├── Mandatory Field Verification Copy (AGENTS.md)
│    ├── Multi-Tier Supporting Evidence (Tier 1 Observation, Tier 2 Index, Tier 3 Forecast)
│    └── Physical Hazard Assessment Grid (DEC-06 Compliant)
│
├── 2. আবহাওয়া পূর্বাভাস (Weather & Climate Feed)
│    ├── Yesterday's Observed Meteorology (Tier 1 - NASA POWER / BMD)
│    └── 72-Hour Ensemble Forecast Cards (Tier 3 - ECMWF IFS / GFS)
│
├── 3. মাটির আর্দ্রতা (Soil Water Balance & AWD Scheduling)
│    ├── Alternate Wetting and Drying (AWD) Status Banner
│    ├── Root-Zone Water Deficit Progress Gauge ($D_t$ vs RAW/TAW)
│    └── FAO-56 Penman-Monteith Evapotranspiration Cards ($ET_0$, $K_c$, $ET_c$)
│
├── 4. হাওড় বন্যা ঝুঁকি (Haor Flash Flood Hazard & Early Harvest)
│    ├── Emergency Early Harvest Warning Banner (RULE-FLD-01)
│    ├── Flash Flood Hazard Index Gauge ($I_{\text{flood}}$)
│    └── Non-Applicability Advisory for High Barind Tract
│
└── 5. স্বচ্ছতা ও তথ্যসূত্র (System Transparency & Data Provenance)
     ├── Ingested Datasets Freshness & Latency Table
     ├── Scientific Equations & Methodologies Catalog
     └── Explicit Scope Boundaries & Non-Goals (`DEC-06`)
```

---

## 3. Screen Inventory & State Mapping

### 3.1 Global Sticky Context Bar (`ContextSelector.tsx`)
- **Purpose**: Enforces `DEC-17` contextual gating across all application views.
- **Fields**:
  - *উপজেলা (Upazila)*: Dropdown of supported pilot administrative units (Godagari, Tanore, Tahirpur, Sunamganj Sadar).
  - *ফসল (Crop)*: Supported calibrated crops (Boro Rice).
  - *বৃদ্ধির পর্যায় (Growth Stage)*: Dynamic stages per crop (Tillering, Booting, Flowering, Dough, Maturity).
  - *হালনাগাদ বাটন (Refresh Button)*: Allows manual re-triggering of data synchronisation.
  - *অঞ্চল মেটাডাটা (Zone Metadata)*: Renders active Agro-Ecological Zone (AEZ-26 Barind vs AEZ-21 Haor) and primary hazard domain.

### 3.2 Advisory Hub (`AdvisoryHubView.tsx`)
- **Primary Use Case**: Farmers checking whether to run diesel irrigation pumps today or prepare for early crop harvest.
- **States**:
  - *Loading*: Renders pulse skeletons (`data-testid="advisory-loading-skeleton"`).
  - *Active Advisory*: Displays prominent Tier 4 card with economic savings (e.g. ৳৪৫০ / ৪.৫L diesel) and action checklist.
  - *Suppressed Advisory*: Renders warning alert when multi-model spread exceeds 50% or telemetry is stale.
  - *Error*: Renders actionable error box with retry trigger.

### 3.3 Water Balance & AWD View (`WaterBalanceView.tsx`)
- **Primary Use Case**: Checking root-zone soil water depletion against Readily Available Water (RAW) to maximize AWD fuel savings.
- **Key Indicators**:
  - Reference Evapotranspiration ($ET_0$): FAO-56 Penman-Monteith (mm/day).
  - Crop Evapotranspiration ($ET_c$): Stage-adjusted $K_c \times ET_0$.
  - Soil Deficit ($D_t$): Visual progress gauge indicating safe AWD range ($D_t < \text{RAW}$) vs critical deficit ($D_t \ge \text{RAW}$).

### 3.4 Haor Flash Flood View (`FloodHazardView.tsx`)
- **Primary Use Case**: Monitoring transboundary runoff in Sunamganj to trigger emergency Boro harvest before submergence.
- **Key Indicators**:
  - Flash Flood Hazard Index ($I_{\text{flood}}$): Normalized metric between 0.00 and 1.00.
  - Early Harvest Trigger: Activates when $I_{\text{flood}} \ge 0.65$ and crop is in maturity stage ($\ge 80\%$ ripe).
  - High Barind Notice: Prominently explains that flash flood tracking is non-applicable to AEZ-26.

### 3.5 Provenance & Transparency View (`ProvenanceView.tsx`)
- **Primary Use Case**: Extension agents, agronomists, and researchers auditing data freshness, latency, and scientific algorithms.
- **Content**:
  - Live dataset latency status (NASA POWER, BMD, Sentinel-1, BMD Hydrology).
  - Reference equations catalog (`EQN-ET0-01`, `EQN-SWD-01`, `IDX-FLD-01`).
  - Documented non-goals (`DEC-06`): No sub-acre parcel predictions, no chemical diagnoses, no hardware pump actuators.
