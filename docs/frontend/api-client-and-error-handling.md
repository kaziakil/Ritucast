# API Client Architecture & Error Handling

## 1. Overview

The Ritucast API Client (`[apiClient.ts](file:///Users/kazi/Projects/RITUCAST/frontend/src/services/apiClient.ts)`) centralizes all asynchronous HTTP communications between the frontend UI and the Phase 10 REST service. It provides unified serialization, error unwrapping, header management, and runtime error classification.

---

## 2. Implementation Specifications

### 2.1 The `ApiError` Class
```typescript
export class ApiError extends Error {
  code: string
  status: number

  constructor(message: string, code: string = 'UNKNOWN_ERROR', status: number = 500) {
    super(message)
    this.name = 'ApiError'
    this.code = code
    this.status = status
  }
}
```

### 2.2 Error Payload Parsing
When FastAPI returns an HTTP 4xx or 5xx status:
1. The client inspects the JSON payload for FastAPI's standard `detail` field.
2. If `detail` is missing, it falls back to `message` or HTTP status text.
3. If JSON parsing fails (e.g., gateway timeout HTML), it generates a localized network error message in Bangla:
   *"নেটওয়ার্ক সংযোগে সমস্যা হয়েছে। দয়া করে পুনরায় চেষ্টা করুন।"*

---

## 3. Failure Mode Matrix & UI Behavior

| Failure Mode | Status Code | UI Display Behavior | Recovery Action |
| :--- | :--- | :--- | :--- |
| **Missing Gating Parameters** | `400 / 422` | Contextual selection banner flashes with warning badge. | User prompted to select Crop or Growth Stage. |
| **Upazila Not Found** | `404` | Specific error card rendered in content area. | Automatic reset to canonical Godagari ID. |
| **Advisory Suppressed** | `200` (`is_suppressed: true`) | Amber alert banner displayed prominently (`DEC-10`). | Advisory card replaced with SAAO contact instructions. |
| **Backend Unreachable** | `0` (Network Error) | Header status changes to `সীমাবদ্ধ` with red network alert. | Single-click "বিশ্লেষণ হালনাগাদ" retry button. |
| **Out-of-Scope Analytical Request**| `400` | Explanatory banner noting geographical boundaries (`DEC-06`). | Directs user to relevant pilot region. |

---

## 4. Stale Data Prevention

To prevent stale results from a previous Upazila or crop stage being erroneously displayed during active network requests:
1. All query states (`advisory`, `risk`, `weather`, `waterBalance`, `floodHazard`) are cleared or put into loading state (`loadingData = true`) before initiating requests.
2. The UI renders skeleton placeholders during network transit.
3. Responses are tied directly to the currently selected IDs upon receipt.
