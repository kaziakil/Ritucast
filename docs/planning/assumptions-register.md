# Ritucast: Project Assumptions Register

## 1. Governance & Classification Standard

Every assumption underlying the Ritucast platform is tracked and classified into one of three statuses:
- **Unverified (UV)**: A hypothesis without empirical confirmation; high risk if wrong.
- **Partially Supported (PS)**: Backed by preliminary literature, analog platforms, or institutional reports, but not yet verified within the specific Ritucast context.
- **Validated (VAL)**: Empirically verified through rigorous field testing, direct dataset validation, or direct user research.

---

## 2. Master Assumption Inventory

| ID | Assumption Description | Category | Status | Evidence Base | Validation Requirement to Upgrade | Owner / Phase |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **ASM-01** | SAAOs and lead farmers possess Android smartphones capable of running modern PWA web apps. | User & Hardware | **Partially Supported (PS)** | DAE digital agriculture reports indicate >85% of SAAOs use smartphones for daily reporting (BAMIS/WhatsApp). | Field inventory of device models and RAM across 20 SAAOs in pilot upazilas during Phase 2. | Product Lead (Phase 2) |
| **ASM-02** | Rural 3G/4G cellular coverage in Barind and Haor pilot upazilas is reliable enough for periodic data synchronization. | Infrastructure | **Partially Supported (PS)** | BTRC coverage maps show 4G across union headquarters; anecdotal reports note dead zones in low-lying haors. | Network latency and bandwidth testing during Phase 2 field reconnaissance. | Tech Lead (Phase 2) |
| **ASM-03** | Free public satellite streams (NASA POWER, Sentinel-1, GPM, SMAP) maintain uninterrupted, zero-cost API availability for Bangladesh. | Data Feasibility | **Validated (VAL)** | Empirically verified in Phase 3 via live curl tests to NASA POWER, CMR (GPM/SMAP), and ESA CDSE OData API. | Live endpoint benchmarking complete in Phase 3 verification log. | Data Architect (Phase 3) |
| **ASM-04** | SMAP 9km–36km soil moisture downscaled with precipitation/ET can provide actionable root-zone moisture trend estimates for regional upazila blocks. | Scientific | **Partially Supported (PS)** | Phase 4 analysis proved L-band saturates over flooded paddies (`RSK-13`), but validly tracks regional upland terrace drying. Supplemented by mass-balance water deficit model ($D_t$). | Ground-truth sensor comparison against BMDA soil moisture network in Phase 15. | Science Lead (Phase 4/15) |
| **ASM-05** | Sentinel-1 C-band SAR reliably maps surface standing water through heavy clouds with near-real-time latency on CDSE. | Scientific | **Validated (VAL)** | Empirically verified in Phase 3 via CDSE OData API: confirmed S1A GRD products published within 2h 05m of sensing over Bangladesh. | Revisit interval gap (6–12d) coupled with upstream GPM rainfall in Phase 4. | Remote Sensing Lead (Phase 3) |
| **ASM-06** | Lead farmers will alter irrigation pumping schedules if presented with clear weather forecast and moisture advisories. | Behavioral & Adoption | **Unverified (UV)** | Behavioral economic studies (e.g., CIMMYT, IRRI) show farmers often pump preemptively out of risk aversion. | Structured interviews and participatory advisory simulation during Phase 2 user research. | Ag Strategist (Phase 2) |
| **ASM-07** | Upazila-level crop calendars published by BRRI/BARI are sufficiently accurate across pilot districts without requiring field-by-field sowing surveys. | Agronomic | **Validated (VAL)** | BRRI/BARI published phenological duration tables provide verified baseline; Phase 4 coupled calendar with SAAO in-app stage confirmation (`FR-LOC-03`). | SAAO participatory field validation during Phase 14/17 pilot. | Agronomist (Phase 4) |
| **ASM-08** | A card-based, explainable Bangla user interface will achieve $>85\%$ task comprehension without in-person training. | UX & Design | **Unverified (UV)** | User testing in similar rural digital initiatives shows text-heavy interfaces fail; visual icons and audio clips improve comprehension. | Usability testing with interactive mockups during Phase 6/7. | UX Lead (Phase 6) |
| **ASM-09** | HTML5 Web Share API and Canvas card export functions reliably across $>80\%$ of budget Android browsers in Bangladesh. | Technical & UX | **Partially Supported (PS)** | Modern Chromium-based mobile browsers (Chrome Android, Opera Mini with WebKit) support Web Share API L1; legacy Android WebViews may lack navigator.share. | Cross-browser compatibility testing across Xiaomi, Symphony, and Walton devices during Phase 11/14. | Frontend Lead (Phase 11) |
| **ASM-10** | DAE Upazila Agriculture Officers (UAOs) will officially endorse SAAOs using Ritucast advisories during village courtyard meetings. | Institutional | **Partially Supported (PS)** | SAAOs are mandated under AMISDP/DAE e-extension policy to utilize digital weather tools. Formal project MoU strengthens adoption. | Consultative review and demonstration with DAE Rajshahi and Sylhet regional directors during Phase 4/16. | Project Lead (Phase 4) |
| **ASM-11** | Transboundary 48h rainfall over Meghalaya ($\ge 100\text{mm}$) is strongly coupled with downstream river surge in Sunamganj with a 24–48h lead time. | Hydrology | **Partially Supported (PS)** | Supported by BWDB FFWC 2017 & 2022 historical flood reports; steep escarpment generates rapid runoff into the Surma basin. | Detailed hydrometric lag calibration (`GAP-01`) against hourly BWDB gauge data in Phase 9/15. | Science Lead (Phase 4/9) |

---

## 3. Assumptions Retirement Process

1. Assumptions will be systematically reviewed at the start and conclusion of each roadmap phase.
2. An assumption cannot be marked **Validated (VAL)** without documenting empirical proof in the corresponding phase validation report.
3. If an assumption is invalidated, an immediate risk entry must be generated in the [Risk Register](file:///Users/kazi/Projects/RITUCAST/docs/planning/risk-register.md) and escalated to the project lead.
