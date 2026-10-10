# Secrets Management & Workflow Permissions: Ritucast

## 1. Overview

This document specifies the least-privilege security model governing GitHub Actions workflow permissions and Google Cloud identity integration.

---

## 2. GitHub Actions Workflow Permissions

Workflows define the minimum required GitHub token permissions explicitly at the root level:

### For `ci.yml` and `live-data-smoke.yml`:
```yaml
permissions:
  contents: read
```
- Restricts the default `GITHUB_TOKEN` to read-only access.
- Eliminates risks of unauthorized commits, issue modifications, or release publication from pull requests.

### For `release.yml`:
```yaml
permissions:
  contents: write
  id-token: write
```
- `contents: write`: Required to publish GitHub Releases, attach `.tar.gz` assets, and push release tags.
- `id-token: write`: Required to exchange OpenID Connect (OIDC) JWT tokens with Google Cloud Workload Identity Federation.

---

## 3. Secret Management via Workload Identity Federation

Ritucast avoids long-lived service account private keys (`credentials.json`). Instead, deployment uses **Google Cloud Workload Identity Federation**:

1. GitHub Actions runner requests an ephemeral OIDC token signed by GitHub.
2. The runner presents this token to Google Cloud Security Token Service (STS).
3. Google validates the token's subject (`repo:owner/ritucast:ref:refs/tags/*`).
4. Google returns a short-lived (1-hour) OAuth access token bound to the `ritucast-deployer` service account.

### Required Repository Secrets in GitHub:
| Secret Name | Purpose | Example Value |
| :--- | :--- | :--- |
| `GCP_PROJECT_ID` | Target Google Cloud Project ID | `ritucast-prod` |
| `GCP_WORKLOAD_IDENTITY_PROVIDER` | Full OIDC provider resource path | `projects/123/locations/global/workloadIdentityPools/github-pool/providers/github-provider` |
| `GCP_SERVICE_ACCOUNT` | Deployer Service Account Email | `ritucast-deployer@ritucast-prod.iam.gserviceaccount.com` |
| `GCP_REGION` (Optional) | Target Cloud Run Region | `asia-south1` |

---

## 4. Secret Protection Standards
- Zero secrets are printed in workflow step outputs (`add-mask` used for sensitive parameters).
- Secrets are NEVER injected into client-side frontend builds (only `VITE_API_BASE_URL` is passed).
- PRs from forks do NOT have access to repository secrets by GitHub default security policy.
