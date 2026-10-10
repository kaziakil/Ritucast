# User Workflows & Operational Journeys

## 1. Primary Persona Overview

### 1.1 Farmer Rafiqul (Barind Smallholder)
- **Profile**: 42-year-old farmer cultivating 2.5 acres of Boro rice in Godagari, Rajshahi. Relies on rented diesel tubewell water.
- **Pain Point**: High diesel costs; runs pump unnecessarily before unanticipated rainstorms, wasting money and washing away fertilizer.
- **Goal**: Check whether he can safely shut off the pump for the next 2 days without risking yield loss.

### 1.2 Extension Officer Salma (SAAO Tahirpur)
- **Profile**: 29-year-old Sub-Assistant Agriculture Officer advising 650 farming households across Tahirpur Haor basin.
- **Pain Point**: Rapid mountain runoff from Meghalaya hills inundates haors before farmers can finish hand-harvesting.
- **Goal**: Monitor the Haor Flash Flood Hazard Index ($I_{\text{flood}}$) and advise farmers when to initiate emergency harvesting of mature paddy.

---

## 2. Core User Journey Flows

### 2.1 Journey A: Farmer Irrigation Check (Barind)
```
[1. Open Web App]
       │
       ▼
[2. View Sticky Context Bar]
       │  Defaults: Godagari / Boro Rice / Tillering
       ▼
[3. Review Advisory Hub]
       │
       ├─► Headline: "আগামী ৪৮ ঘণ্টা সেচ স্থগিত রাখুন"
       ├─► Economic Benefit: ৳৪৫০ / ৪.৫ লিটার ডিজেল সাশ্রয়
       └─► Field Check Notice: Inspect soil & bunds before turning off pump
       │
       ▼
[4. Switch to "মাটির আর্দ্রতা" Tab]
       │
       └─► Verifies D_t (12.4mm) is well below RAW (19.6mm)
       │
       ▼
[5. Confidence Confirmed: Keeps pump off]
```

### 2.2 Journey B: Extension Worker Flood Alert (Haor)
```
[1. Open Web App]
       │
       ▼
[2. Switch Upazila to "তাহিরপুর (Haor Basin)"]
       │  Crop: Boro Rice / Stage: Maturity (পাকা পর্যায়)
       ▼
[3. Advisory Hub displays Early Harvest Alert]
       │
       ├─► RULE-FLD-01 Triggered
       └─► Recommendation: Immediate harvesting of 80% ripe paddy
       │
       ▼
[4. Switch to "হাওড় বন্যা ঝুঁকি" Tab]
       │
       ├─► Inspects I_flood (0.68 - WARNING Tier)
       ├─► Verifies upstream Meghalaya rainfall rate (0.72)
       └─► Checks SAR inundation footprint (28% haor basin covered)
       │
       ▼
[5. SAAO issues field advisory via loudspeaker & SMS]
```

### 2.3 Journey C: Researcher Data Audit
```
[1. Switch to "স্বচ্ছতা ও তথ্যসূত্র" Tab]
       │
       ├─► Inspects latency of NASA POWER, BMD, Sentinel-1
       ├─► Verifies physical equations (FAO-56 Penman-Monteith)
       └─► Confirms DEC-06 non-goals are respected
```
