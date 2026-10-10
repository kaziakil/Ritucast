# Ritucast UX Success Metrics and Evaluation Framework

## 1. Executive Summary & Measurement Framework

This specification defines the objective, measurable user experience indicators for evaluating the usability, clarity, accessibility, and agronomic trustworthiness of the Ritucast platform.

### Evaluation Philosophy
- **Dual Evaluation Pathway**:
  1. *Laboratory & Field Usability Sessions* (Phase 6, 7, 14): Observational task tests and comprehension interviews with real SAAOs and lead farmers.
  2. *Privacy-Preserving Telemetry* (Phase 16–17): Aggregated, anonymous client metrics with **zero personal data, zero device fingerprints, and zero private farm boundary tracking** (`NFR-SEC-01`, `DEC-14`).

---

## 2. Master UX Success Metrics Table

| Metric ID | Metric Name | Category | Primary Measurement Method | Timing of Measurement | Privacy Impact |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`UX-MET-01`** | **Core Task Completion Rate** | Usability | Moderated task-based usability testing across 10 core tasks. | Phase 14 Usability Trials | Zero (Lab testing) |
| **`UX-MET-02`** | **Time-to-First-Advisory (TTFA)** | Usability / Efficiency | Stopwatch / interaction timestamp from app open to advisory comprehension. | Phase 14 Usability Trials | Zero (Lab testing) |
| **`UX-MET-03`** | **Geographic Selection Success** | Navigation | % of users who successfully select/switch Upazila in $\le 2$ taps without error. | Phase 14 & Analytics | Zero (Aggregated clicks) |
| **`UX-MET-04`** | **Advisory Comprehension Rate** | Cognitive / Safety | Structured interview: can the user accurately explain *what* to do and *why*? | Phase 14 Field Interviews | Zero (Interview) |
| **`UX-MET-05`** | **Limitation & Ail-Check Recall** | Safety / Trust | % of farmers who recall the mandatory reminder to check soil moisture by hand. | Phase 14 Field Interviews | Zero (Interview) |
| **`UX-MET-06`** | **Suppression State Comprehension** | Trust & Transparency | % of users who correctly interpret the amber advisory suppression banner. | Phase 14 Simulation Test | Zero (Lab testing) |
| **`UX-MET-07`** | **Low-End Mobile Crash-Free Rate** | Technical / Hardware | % of sessions without out-of-memory WebGL or browser crashes on 2GB RAM phones. | Phase 11 & Telemetry | Anonymous error logs |
| **`UX-MET-08`** | **Time-to-Interactive (TTI) on 3G** | Performance | Web Vitals performance benchmark over throttled 3G profile. | Phase 11 & CI Pipeline | Synthetic testing |
| **`UX-MET-09`** | **WCAG 2.2 AA Compliance Score** | Accessibility | Automated axe-core / Lighthouse audit + manual screen-reader walkthrough. | Phase 7, 11, and 14 | Zero (Code audit) |
| **`UX-MET-10`** | **Farmer Perceived Trust Score** | Trust & Adoption | 5-Point Likert scale survey on perceived reliability of advice. | Phase 17 Pilot Evaluation | Voluntary survey |

---

## 3. Detailed Metric Formulations & Evaluation Protocols

### UX-MET-01: Core Task Completion Rate
- **What It Measures**: Percentage of test participants who successfully complete a defined task (e.g., "Find whether it will rain tomorrow in Godagari" or "Confirm active crop growth stage") without moderator intervention.
- **Why It Matters**: Verifies whether the information architecture and navigation models are intuitive to users with varied digital literacy.
- **Data Required**: Pass/Fail observation logs across 20 representative users (10 SAAOs, 10 Lead Farmers).
- **Target Threshold**: $\ge 85\%$ unassisted task completion on first attempt.

---

### UX-MET-02: Time-to-First-Advisory (TTFA)
- **What It Measures**: Total elapsed time from the moment the user launches the application until they locate and comprehend today's primary irrigation or flood recommendation.
- **Why It Matters**: Rural users operate with constrained time and battery life; critical advice must be accessible almost immediately.
- **Data Required**: Stopwatch observation in seconds during usability testing.
- **Target Threshold**: Median time $\le 15\text{ seconds}$ on mobile.

---

### UX-MET-04: Advisory Comprehension Rate
- **What It Measures**: The proportion of farmers who, after reading the Tier 4 advisory card, can accurately explain:
  1. The recommended operational action (e.g., "আজ সেচ দেওয়া বন্ধ রাখতে হবে").
  2. The scientific reason (e.g., "কারণ কালকে বৃষ্টি হওয়ার কথা এবং মাটিতে রস আছে").
- **Why It Matters**: Prevents costly misinterpretations and ensures plain-language Bangla copy is clear to rural smallholders.
- **Measurement Method**: Post-task comprehension interview asking: *"এই কার্ডটি দেখে আপনি আজকে কী করবেন এবং কেন করবেন?"*
- **Target Threshold**: $\ge 90\%$ accurate comprehension among tested farmers.

---

### UX-MET-05: Limitation & Field-Check (Ail) Recall Rate
- **What It Measures**: The percentage of farmers who spontaneously recall or acknowledge the mandatory reminder: *"সেচ বন্ধ করার আগে জমির আইল ও মাটির রস নিজে হাত দিয়ে পরীক্ষা করুন।"*
- **Why It Matters**: Critical agronomic safety guardrail (`DEC-10`, `DEC-17`). Verifies that the platform reinforces farmer agency and physical verification rather than blind reliance on algorithms.
- **Measurement Method**: Post-test recall prompt: *"সেচের সিদ্ধান্ত চূড়ান্ত করার আগে কার্ডে কী নির্দেশ দেওয়া হয়েছিল?"*
- **Target Threshold**: $\ge 80\%$ recall among tested farmers.

---

### UX-MET-06: Suppression State Comprehension Rate
- **What It Measures**: The ability of users to recognize that an advisory has been withheld due to high forecast uncertainty, without assuming the app is broken or that zero risk exists.
- **Why It Matters**: Ensures farmers understand that uncertainty is communicated honestly, preserving institutional credibility during erratic weather events.
- **Measurement Method**: Usability simulation presenting the amber suppression state (`ST-08` / `ST-10`) and asking participants to explain the screen.
- **Target Threshold**: $\ge 85\%$ correct interpretation (understands advice is paused, not that rain is guaranteed absent).

---

### UX-MET-09: Accessibility & Contrast Audit Score
- **What It Measures**: Conformance against WCAG 2.2 Level AA accessibility criteria.
- **Why It Matters**: Ensures the platform is usable by color-blind farmers, older farmers with degraded vision, and users relying on screen readers.
- **Measurement Method**: Automated auditing tools (`@axe-core/playwright`, Google Lighthouse) integrated into continuous integration, supplemented by manual TalkBack screen-reader testing on Android.
- **Target Threshold**: Zero critical or serious accessibility violations; 100% compliance on touch target sizes and text contrast.
