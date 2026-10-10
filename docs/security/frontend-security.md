# Frontend Security and User Input Handling — Ritucast

## 1. Overview

Ritucast's user interface is built as a React 19 / TypeScript single-page application (SPA) optimized for low-bandwidth mobile devices in rural Bangladesh. This document details the client-side security architecture, XSS prevention, error display safety, and Content Security Policy (CSP) enforcement.

---

## 2. Cross-Site Scripting (XSS) Prevention

### 2.1 React JSX Auto-Escaping
- By default, React JSX automatically escapes all rendered string expressions before inserting them into the DOM, converting HTML special characters (`<`, `>`, `&`, `"`, `'`) to safe character entities.
- **Strict Prohibition**: The dangerous React property `dangerouslySetInnerHTML` is **strictly prohibited** across all application components.
- **Verification**: Verified by automated test `verifies absence of dangerouslySetInnerHTML across all TSX components` in [`frontend/src/test/security.test.tsx`](file:///Users/kazi/Projects/RITUCAST/frontend/src/test/security.test.tsx).

### 2.2 Absence of `eval()` and Raw DOM Injections
- No direct DOM string manipulation via `.innerHTML`, `document.write()`, or `eval()` exists in the codebase.
- Verified by automated test `verifies absence of eval and innerHTML direct assignment` in [`frontend/src/test/security.test.tsx`](file:///Users/kazi/Projects/RITUCAST/frontend/src/test/security.test.tsx).

---

## 3. Network Failure & Safe Mock Data Fallback Policy

### 3.1 Anti-Deception Fallback Policy (`DEC-10`, `DEC-17`)
- **Core Principle**: A decision-support system for agriculture must **never silently substitute fake or outdated mock data** when an API call fails. Doing so risks misleading a farmer into executing real-world farming actions (e.g., withholding irrigation) based on synthetic numbers.
- **Implementation**:
  - The API client ([`frontend/src/services/apiClient.ts`](file:///Users/kazi/Projects/RITUCAST/frontend/src/services/apiClient.ts#L49)) throws an explicit `ApiError` with status codes and Bengali error descriptions on any network or server failure.
  - UI views ([`frontend/src/components/AdvisoryHubView.tsx`](file:///Users/kazi/Projects/RITUCAST/frontend/src/components/AdvisoryHubView.tsx), [`frontend/src/components/WaterBalanceView.tsx`](file:///Users/kazi/Projects/RITUCAST/frontend/src/components/WaterBalanceView.tsx)) catch `ApiError` and render a high-visibility error alert banner with a manual retry button.
- **Verification**: Verified in [`frontend/src/test/e2e_user_journey.test.tsx`](file:///Users/kazi/Projects/RITUCAST/frontend/src/test/e2e_user_journey.test.tsx) (`handles backend service failure gracefully without crash`) and [`frontend/src/test/security.test.tsx`](file:///Users/kazi/Projects/RITUCAST/frontend/src/test/security.test.tsx).

---

## 4. Secret & Token Isolation

### 4.1 Client Asset Hygiene
- No private cloud keys (Google Cloud, AWS, GitHub) or server secrets are embedded in the client build.
- Environment variables exposed to the client are strictly limited to public configuration prefixed with `VITE_` (e.g. `VITE_API_BASE_URL`).
- Verified by automated scan `verifies no private server secrets or cloud credentials in frontend source code` in [`frontend/src/test/security.test.tsx`](file:///Users/kazi/Projects/RITUCAST/frontend/src/test/security.test.tsx).

---

## 5. Content Security Policy & Gateway Headers

The NGINX edge gateway ([`deploy/docker/nginx.conf`](file:///Users/kazi/Projects/RITUCAST/deploy/docker/nginx.conf#L30)) enforces strict client headers:

```nginx
# Security Headers (DEC-53)
add_header X-Frame-Options "DENY" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self' data:; connect-src 'self' https: http:;" always;
```

---

## 6. Client Bundle Budget & Performance Integrity (`DEC-09`)

Security protections must not degrade client performance on rural 3G cellular connections:
- **Wire Size Budget**: $\le 1.5\text{MB}$ total bundle.
- **Actual Build Output**:
  - `dist/index.html`: $1.42\text{ kB}$ ($0.71\text{ kB}$ gzip)
  - `dist/assets/index.css`: $13.54\text{ kB}$ ($3.08\text{ kB}$ gzip)
  - `dist/assets/index.js`: $292.54\text{ kB}$ ($85.51\text{ kB}$ gzip)
  - **Total Wire Transfer Size**: $\mathbf{89.3\text{ kB}}$ gzip ($\approx 6\%$ of allowed budget).

Related documentation:
- [`docs/security/api-security.md`](file:///Users/kazi/Projects/RITUCAST/docs/security/api-security.md)
- [`docs/security/secrets-and-dependency-management.md`](file:///Users/kazi/Projects/RITUCAST/docs/security/secrets-and-dependency-management.md)
- [`docs/ci-cd/phase-14-cicd-architecture.md`](file:///Users/kazi/Projects/RITUCAST/docs/ci-cd/phase-14-cicd-architecture.md)
