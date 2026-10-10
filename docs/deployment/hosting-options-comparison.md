# Hosting Options Comparison: Ritucast Agricultural Intelligence Platform

## 1. Overview and Evaluation Criteria

In accordance with Phase 13 requirements and `DEC-09` / `ADR-07`, hosting options for Ritucast were evaluated across six architectural dimensions:
1. **Compatibility with Technical Stack**: Python 3.10 FastAPI backend with NumPy/Pandas/Scipy/PyArrow dependencies and React 19 / TypeScript SPA frontend.
2. **Operational Simplicity & Maintenance Overhead**: Zero or minimal infrastructure management; no dedicated cluster maintenance (e.g., Kubernetes).
3. **Storage & Data Handling**: Support for bundled Parquet feature files and GeoJSON polygons ($<100\text{KB}$) without requiring a managed relational database or Redis cache.
4. **Latency & Regional Proximity**: Low-latency edge or regional points of presence serving rural users in Bangladesh.
5. **Cost Predictability & Scaling**: Scale-to-zero when idle, supporting seasonal and morning/evening agricultural query spikes within a $\le \$65/\text{month}$ total operational ceiling (and ideally $\$0 - \$10/\text{month}$ under free tier).
6. **Portability & Vendor Lock-in**: Standard OCI containers ensuring portability across multiple clouds or on-premise infrastructure.

---

## 2. Platform Comparison Matrix

| Evaluation Dimension | Option A: Google Cloud Run (Recommended) | Option B: AWS ECS Fargate + S3/CloudFront | Option C: Fly.io / Render Managed Apps | Option D: Dedicated VPS (Hetzner / DigitalOcean) |
| :--- | :--- | :--- | :--- | :--- |
| **Frontend Hosting** | NGINX Alpine Container on Cloud Run or Firebase Hosting | S3 Bucket + CloudFront CDN distribution | Static Site hosting on Render or Fly machine | Nginx on Linux VM host |
| **Backend Runtime** | Serverless Container (1 vCPU, 1GB RAM) | Serverless Container on ECS Fargate | Micro VM (512MB–1GB RAM) | Systemd service / Docker on VM |
| **Database Requirement** | None (Bundled Parquet in image) | None (Bundled Parquet in image) | None (Bundled Parquet in image) | None (Bundled Parquet in image) |
| **Regional Proximity** | `asia-south1` (Mumbai, $\approx 35\text{ms}$) | `ap-south-1` (Mumbai, $\approx 35\text{ms}$) | `sin` (Singapore, $\approx 60\text{ms}$) | Frankfurt / Singapore ($\approx 60-150\text{ms}$) |
| **Scale-to-Zero** | Supported natively (0 instances) | Not natively on Fargate (min 1 task) | Fly.io supports auto-stop; Render free sleeps | No (Continuous VM compute cost) |
| **Cold Start Performance** | $\approx 1.8\text{s} - 2.5\text{s}$ (lightweight image) | $\approx 20\text{s} - 45\text{s}$ (task provisioning) | $\approx 1.5\text{s} - 3.0\text{s}$ (micro-VM wake) | 0s (Always running) |
| **Free Tier / Base Cost** | Free Tier covers 2M requests/month. Base cost: **$0.00/month** | S3+CloudFront free tier; Fargate min 1 task: **~$15–$25/month** | Fly/Render free tier available with usage caps: **$0–$7/month** | Fixed VM cost: **$4–$12/month** |
| **Container Portability** | 100% OCI Standard | 100% OCI Standard | OCI / Buildpack | 100% OCI Standard |
| **Maintenance Burden** | Zero OS/patching maintenance | Low-to-Medium (IAM, VPC, ALB setup) | Zero OS maintenance | High (OS updates, security patches, firewall) |

---

## 3. Selected Platform: Google Cloud Run

### Key Justifications
1. **True Scale-to-Zero**: Farmers in Godagari, Tanore, Sunamganj, and Tahirpur check advisories predominantly at sunrise (06:00–08:00) and evening (17:00–19:00). Cloud Run scales to zero instances during idle off-peak hours, incurring zero compute cost.
2. **Generous Free Allocation**: Cloud Run provides 2 million free requests, 360,000 vCPU-seconds, and 180,000 GiB-seconds monthly. The entire pilot scale easily fits inside this free tier.
3. **Mumbai Region (`asia-south1`)**: Direct fiber peering with Bangladeshi international internet gateways (IIGs) guarantees the lowest latency for rural 3G connections.
4. **Zero-Database Architectural Fit**: Because Ritucast uses verified Parquet tables ($<100\text{KB}$) embedded in the image, no Cloud SQL or external database instance is needed.
5. **Knative Compliance**: Cloud Run uses the open Knative serving standard (`serving.knative.dev/v1`), preventing proprietary platform lock-in.
