# ADR-03: Selection of React 18, TypeScript, and Vanilla CSS for Client PWA

## 1. Status
**Approved** (2026-10-10)

## 2. Context
Rural smallholders and extension workers in Bangladesh access Ritucast on budget Android phones (Android 8+, 2GB RAM, 720p screens) over variable 3G cellular connections (`DEC-09`, `ASM-01`). The frontend must meet strict performance targets:
- Initial production bundle size $\le 1.5\text{MB}$ uncompressed.
- Time-to-Interactive $\le 3.5\text{s}$ on 3G.
- Peak client heap memory $\le 45\text{MB}$.
- Offline operation via Service Workers.

We evaluated:
1. *Next.js (SSR / App Router)*
2. *Vue 3 / Svelte*
3. *React 18 + TypeScript + Vite + Vanilla CSS (Selected)*

## 3. Decision
We adopt **React 18** with **TypeScript**, bundled with **Vite 5**, styled with handcrafted **Vanilla CSS (Design Tokens)**, state-managed with **Zustand (1.5KB)**, and offline-enabled via **Workbox v7**.

## 4. Rationale & Trade-Offs
- **Zero Framework Server Overhead**: Unlike Next.js which requires a Node.js server runtime, Vite builds a pure static Single-Page Application (SPA) that deploys directly to Google Cloud CDN edge nodes for instantaneous delivery.
- **Strict Adherence to Styling Rules**: In strict alignment with system operating rules, Tailwind CSS is avoided in favor of Vanilla CSS design tokens (`index.css`). This eliminates CSS utility bloat, reduces CSS footprint to $<35\text{KB}$, and guarantees predictable styling.
- **Micro-State Footprint**: Zustand provides React hooks-based state management at just $1.5\text{KB}$ minified, avoiding Redux Toolkit's $35\text{KB}$ overhead.
- **Offline Capability**: Workbox Service Workers cache the App Shell and latest upazila data in IndexedDB, ensuring full offline functionality in low-lying Haor basins and remote Barind villages.

## 5. Revisit Triggers
This decision will be revisited if:
- SEO requirements for public search engine indexing require server-side pre-rendering, at which point static site generation (SSG) via Astro or Vite-SSG can be evaluated.
