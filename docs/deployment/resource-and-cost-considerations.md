# Resource and Cost Considerations: Ritucast Agricultural Intelligence Platform

## 1. Overview

In accordance with `DEC-09`, `ADR-07`, and Phase 13 mandates, Ritucast is designed for predictable, ultra-low operating expenditure ($\le \$65/\text{month}$ total pilot budget) while delivering robust performance across the High Barind Tract and Haor Basin testbeds.

---

## 2. Empirical Resource Profiling

Local container execution and integration tests established the following empirical runtime measurements:

| Metric | Measured Baseline (Backend) | Measured Baseline (Frontend) | Cloud Run Provisioned Limit | Headroom / Margin |
| :--- | :--- | :--- | :--- | :--- |
| **Startup / Cold Start Time** | $1.8\text{s} - 2.5\text{s}$ | $< 0.2\text{s}$ | 60s timeout | $> 95\%$ safe margin |
| **Idle Memory Consumption** | $\approx 42\text{MB}$ | $\approx 6\text{MB}$ | 1024MB / 256MB | $> 90\%$ safe margin |
| **Peak Active Heap Memory** | $\approx 78\text{MB}$ (during batch ET0) | $\approx 18\text{MB}$ | 1024MB / 256MB | $> 90\%$ safe margin |
| **CPU Utilization (Idle)** | $0.0\%$ | $0.0\%$ | 1 vCPU | Scales to 0 instances |
| **CPU Utilization (Per Request)**| $\approx 4\text{ms}$ CPU time | $< 1\text{ms}$ CPU time | 1 vCPU | Handles 80 concurrent req/instance |
| **Dataset Storage on Disk** | 108 KB | N/A (Static HTML/JS) | Ephemeral container | $< 0.1\%$ container capacity |

---

## 3. Cloud Run Cost Model & Free-Tier Coverage

Google Cloud Run operates on a pay-per-use serverless pricing model with a generous monthly free tier:

| Cloud Resource | Free Tier Monthly Allowance | Estimated Ritucast Pilot Consumption | Expected Billable Amount |
| :--- | :--- | :--- | :--- |
| **HTTP Requests** | 2,000,000 requests | $\approx 150,000$ requests/month | **$0.00** |
| **vCPU Compute** | 360,000 vCPU-seconds | $\approx 45,000$ vCPU-seconds | **$0.00** |
| **Memory Allocation** | 180,000 GiB-seconds | $\approx 45,000$ GiB-seconds | **$0.00** |
| **Egress Bandwidth** | 1 GB / month to worldwide | $\approx 450\text{MB}$ / month (gzipped payloads) | **$0.00** |
| **Artifact Registry Storage** | 0.5 GB / month | $\approx 350\text{MB}$ (1 backend, 1 frontend image) | **$0.00 - $0.10** |
| **Total Monthly Cost** | — | — | **$0.00 to $5.00 / month** |

### Safety Safeguards
1. **Maximum Instance Cap**: Set to `maxScale: 5` in `service-backend.yaml` and `service-frontend.yaml`, guaranteeing that unexpected traffic spikes or automated bots cannot spawn unlimited cloud instances.
2. **Billing Alert**: Set at $10.00/month in Google Cloud Console to immediately alert platform administrators of any anomalies.
3. **Hard Budget Ceiling**: Well below the $65.00/month project governance budget threshold.
