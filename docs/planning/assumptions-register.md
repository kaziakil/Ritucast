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
| **ASM-03** | Free public satellite streams (NASA POWER, Sentinel-1, GPM, SMAP) will maintain uninterrupted, zero-cost API availability. | Data Feasibility | **Partially Supported (PS)** | NASA and ESA Copernicus have open data mandates; however, ESA Copernicus Data Space Ecosystem API changes and rate limits occur. | Rigorous API quota, rate-limit, and latency testing in Phase 3. | Data Architect (Phase 3) |
| **ASM-04** | SMAP 9km–36km soil moisture downscaled with precipitation/ET can provide actionable root-zone moisture trend estimates for regional upazila blocks. | Scientific | **Unverified (UV)** | Academic studies (e.g., IWMI, NASA Applied Sciences) show regional correlation, but micro-plot bunding in Bangladesh paddies creates local hydrology decoupling. | Cross-referencing SMAP anomalies with BMDA ground moisture sensors or water table data in Phase 4/15. | Science Lead (Phase 4) |
| **ASM-05** | Sentinel-1 C-band SAR can reliably detect surface standing water through heavy monsoon clouds in the Haor basin within 48h of flood crests. | Scientific | **Partially Supported (PS)** | CEGIS and UN-SPIDER flood mapping protocols routinely use Sentinel-1 SAR GRD in Bangladesh. 6–12 day revisit interval may miss short-lived crests without hydrologic modeling. | Sentinel-1 flood extent correlation with BWDB gauge crest records during historical flood events (Phase 4/15). | Remote Sensing Lead (Phase 4) |
| **ASM-06** | Lead farmers will alter irrigation pumping schedules if presented with clear weather forecast and moisture advisories. | Behavioral & Adoption | **Unverified (UV)** | Behavioral economic studies (e.g., CIMMYT, IRRI) show farmers often pump preemptively out of risk aversion. | Structured interviews and participatory advisory simulation during Phase 2 user research. | Ag Strategist (Phase 2) |
| **ASM-07** | Upazila-level crop calendars published by BRRI/BARI are sufficiently accurate across pilot districts without requiring field-by-field sowing surveys. | Agronomic | **Partially Supported (PS)** | BBS and BRRI maintain standard phenological duration tables for mega-varieties (BRRI dhan28, dhan29, dhan89). Climate shifts cause 7–14 day interannual variance. | Review of recent 3-year DAE sowing date logs in Godagari and Sunamganj (Phase 4). | Agronomist (Phase 4) |
| **ASM-08** | A card-based, explainable Bangla user interface will achieve $>85\%$ task comprehension without in-person training. | UX & Design | **Unverified (UV)** | User testing in similar rural digital initiatives shows text-heavy interfaces fail; visual icons and audio clips improve comprehension. | Usability testing with interactive mockups during Phase 6/7. | UX Lead (Phase 6) |

---

## 3. Assumptions Retirement Process

1. Assumptions will be systematically reviewed at the start and conclusion of each roadmap phase.
2. An assumption cannot be marked **Validated (VAL)** without documenting empirical proof in the corresponding phase validation report.
3. If an assumption is invalidated, an immediate risk entry must be generated in the [Risk Register](file:///Users/kazi/Projects/RITUCAST/docs/planning/risk-register.md) and escalated to the project lead.
