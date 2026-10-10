# Release Notes Template and Generation SOP: Ritucast

## 1. Overview

Clear, user-centered release notes are vital for maintaining trust with extension workers (SAAOs), lead farmers, and institutional agronomists.

This document provides the standard release notes template, guidelines, and distribution procedures for Ritucast releases.

---

## 2. Release Notes Standard Template

```markdown
# Ritucast Release vX.Y.Z (YYYY-MM-DD)

## Summary
Brief 2-3 sentence executive overview of what this release delivers and why it matters to agricultural users.

## 🌾 Agronomic & Decision Support Updates
- **High Barind Tract**: Description of changes to irrigation scheduling, AWD thresholds, or soil moisture deficit calculations.
- **Haor Basin**: Description of updates to flash-flood hazard score weights, Surma river danger marks, or early harvest alerts.

## 💻 Software & Interface Improvements
- **Frontend & UX**: User-visible UI changes, Bangla copy refinements, performance improvements.
- **Backend & APIs**: New endpoints, schema updates, latency optimizations.

## 🛡️ Security, Reliability & Quality Gates
- Security audits, dependency upgrades, or container hardening updates.
- Test pass summary: Pytest results, Vitest results, bundle payload measurements.

## ⚠️ Known Limitations & Field Verification Notes
- Explicit field notice: "সেচ বন্ধ করার আগে জমির আইল এবং মাটির রস নিজে হাত দিয়ে পরীক্ষা করুন।"
- Any temporary data service dependencies or unverified geographical boundaries.

## 📦 Artifact References
- Release Tarball: `ritucast-vX.Y.Z.tar.gz`
- OpenAPI Schema: `openapi.json`
- Backend Container: `asia-south1-docker.pkg.dev/PROJECT_ID/ritucast/backend:vX.Y.Z`
- Frontend Container: `asia-south1-docker.pkg.dev/PROJECT_ID/ritucast/frontend:vX.Y.Z`
```

---

## 3. Communication Guidelines
1. **Plain Language Bangla for Field Notices**: Never use purely academic English jargon when describing farming impact.
2. **Anti-Overconfidence Compliance**: Never state "১০০% নিশ্চিত" or "ফলনের নিশ্চয়তা" in release copy.
3. **Traceability**: Link every bug fix to its specific GitHub issue or stable requirement identifier.
