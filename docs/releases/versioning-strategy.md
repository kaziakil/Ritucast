# Versioning Strategy Specification: Ritucast

## 1. Overview

Ritucast follows **Semantic Versioning 2.0.0** (`MAJOR.MINOR.PATCH`) to communicate compatibility, analytical engine changes, and feature additions clearly to extension workers, researchers, and system maintainers.

---

## 2. Version Increment Rules

The version number format is `vX.Y.Z`:

```
v MAJOR . MINOR . PATCH
    │       │       │
    │       │       └── Backward-compatible bug fixes, threshold calibrations, UI styling
    │       └────────── Backward-compatible new features, new pilot Upazilas, new indicators
    └────────────────── Incompatible API schema changes, model mathematical paradigm shifts
```

### 2.1 Major Version (`X`)
Incremented when:
- Breaking changes are introduced to the REST API endpoints or response envelopes.
- Fundamental architectural shifts occur in the underlying data model (e.g., changing from Upazila polygons to sub-parcel rasters).
- Mathematical formulation breaks backward compatibility in advisory rules.

### 2.2 Minor Version (`Y`)
Incremented when:
- New Upazilas, AEZs, or secondary crops are onboarded.
- New indicators or endpoints are added to the API in a backward-compatible manner.
- New UI views or analytical charts are added to the frontend.

### 2.3 Patch Version (`Z`)
Incremented when:
- Bug fixes are deployed (e.g., path coercion or UI undefined guards).
- Hydrological river stage threshold calibrations (e.g., adjusting Tahirpur danger mark).
- Minor dependency updates and performance optimizations.

---

## 3. Git Tagging Convention

All official releases must be marked with annotated, signed Git tags adhering to the format:
```text
v<MAJOR>.<MINOR>.<PATCH>
```
Example: `v1.0.0`, `v1.0.1`, `v1.1.0`.

Pre-release tags for staging testing use the hyphenated suffix:
```text
v<MAJOR>.<MINOR>.<PATCH>-rc.<N>
```
Example: `v1.0.0-rc.1`.
