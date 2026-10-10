# Operational Incident Response Runbook — Ritucast

## 1. Incident Severity Classification Matrix

| Severity Level | Definition | Impact on Farmers & SAAOs | Response Target (MTTA) | Resolution Target (MTTR) | Notification Protocol |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **P1 - Critical** | Complete service outage, API returning 500 across all pilot Upazilas, or corrupted advisory advice that could cause crop destruction. | Farmers and SAAOs cannot access advisories; risk of erroneous pumping or harvesting action. | **$<15\text{ minutes}$** | **$<2\text{ hours}$** | Immediate paging of DevOps & Lead Agronomist; banner on web client. |
| **P2 - Major** | Core pipeline failure causing automated suppression on all cards ($>36\text{h}$ staleness); rate limiting malfunction; single pilot region unavailable. | Advisories suppressed; farmers see safe fallback cards instructing manual field inspection. | **$<30\text{ minutes}$** | **$<6\text{ hours}$** | Tech Lead notified; SAAO WhatsApp broadcast if suppression persists. |
| **P3 - Moderate** | Minor API latency degradation ($P_{95} > 250\text{ms}$); non-critical dataset delayed (Sentinel-1 SAR pending pass); logging format anomaly. | Slight UI lag on 3G; fallback to optical/catchment indices. | **$<2\text{ hours}$** | **$<24\text{ hours}$** | Slack/Email alert to engineering team; resolved during working hours. |
| **P4 - Minor** | Cosmetic UI misalignment; minor typo in Bengali tooltip; non-impacting telemetry bug. | Minimal; core decision intelligence completely intact. | **$<1\text{ business day}$** | Next release cycle | Logged as GitHub issue; triaged in routine sprint. |

---

## 2. Common Incident Playbooks

### Playbook 1: Production Service 500 Errors / CrashLoopBackOff (P1)
1. **Detection**: Uptime monitor reports HTTP 500 or Cloud Run container health check fails 3 consecutive probes.
2. **Immediate Mitigation**:
   ```bash
   # Check active revisions
   gcloud run revisions list --service=ritucast-backend --region=asia-south1

   # Instant rollback to previous verified revision (<2s traffic shift)
   gcloud run services update-traffic ritucast-backend \
     --region=asia-south1 \
     --to-revisions=ritucast-backend-PREVIOUS_REV=100
   ```
3. **Investigation**:
   ```bash
   gcloud logging read "resource.type=cloud_run_revision AND severity>=ERROR" --limit=20
   ```
4. **Verification**: Confirm `/health` and `/ready` return `200 OK`.

---

### Playbook 2: Data Pipeline Stale (>36h) & Advisories Suppressed (P2)
1. **Detection**: `/health/deep` reports `pipeline_health.circuit_breaker_tripped = true` and `stale_tables_count > 0`.
2. **Likely Impact**: Farmers see amber suppression banner: *"পরামর্শ সাময়িকভাবে স্থগিত"*. No erroneous advice is delivered, but decision support is paused.
3. **Investigation**:
   - Check upstream provider status (NASA POWER, Open-Meteo).
   - Inspect GitHub Actions scheduled smoke logs: `gh run list --workflow=live-data-smoke.yml`.
4. **Mitigation**:
   - If upstream API was down and has recovered, trigger manual data update:
     `gh workflow run live-data-smoke.yml`.
   - If upstream API is experiencing multi-day outage, notify SAAO network via DAE district coordinators to rely on manual soil moisture checking.
5. **Verification**: Re-query `/health/deep` to confirm `circuit_breaker_tripped = false`.

---

### Playbook 3: Cloud Run Memory or CPU Exhaustion Alert (P2)
1. **Detection**: Cloud Monitoring alert triggers for container memory $>200\text{MB}$ or CPU $>80\%$.
2. **Mitigation**:
   - Check if an abusive client IP is flooding requests:
     Inspect structured logs for high-frequency callers:
     `gcloud logging read "jsonPayload.logger=ritucast.api.access" --limit=100 | jq .client_ip`
   - If needed, scale instance memory limit from 256MB to 512MB:
     ```bash
     gcloud run services update ritucast-backend --memory=512Mi --region=asia-south1
     ```
3. **Verification**: Confirm memory RSS stabilizes below 80MB.

---

## 3. Post-Incident Review (PIR) Protocol

Within 48 hours of resolving any P1 or P2 incident, an engineering post-mortem must be published documenting:
1. **Incident Summary**: Exact duration, affected Upazilas, and user impact.
2. **Timeline of Events**: Chronological log from first anomaly detection to complete recovery.
3. **Root Cause Analysis (RCA)**: Using the "5 Whys" methodology to identify root technical or operational flaws.
4. **Corrective Action Items**: Specific preventative measures with assigned GitHub issues and owners.
