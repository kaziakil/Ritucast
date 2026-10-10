# Ritucast Iconography and Imagery Guidelines

## 1. Executive Summary & Aesthetic Standard

This specification establishes the rules for icons, illustrations, and photographic imagery across the Ritucast platform.

### Core Visual Principles
1. **Functional Utility over Decoration**: Every icon and image must communicate meaningful context or reduce cognitive load for users with limited literacy. Purely decorative clipart and stock photos are strictly banned.
2. **Never Misrepresent Satellites or Field Realities**: An illustrative photograph of a rice paddy must never be labeled or implied to be a live satellite image or real-time drone feed.
3. **Open-Source & Zero-Bloat**: All icons are lightweight SVG vector glyphs adhering to open permissive licenses (MIT / Apache 2.0).

---

## 2. Iconography Specification

### 2.1 Geometry, Grid, and Stroke Consistency
- **Base Grid**: $24 \times 24\text{px}$ standard viewport with a $2\text{px}$ inner safety padding.
- **Stroke Width**: Uniform **$2\text{px}$ solid stroke**; rounded line caps (`stroke-linecap="round"`) and rounded line joins (`stroke-linejoin="round"`).
- **Recommended Library**: **Lucide Icons** (Open-source, tree-shakeable SVG).
- **Scale Tokens**:
  - `--icon-size-sm`: $16 \times 16\text{px}$ (Micro-badges, inline text indicators).
  - `--icon-size-md`: $20 \times 20\text{px}$ (Button icons, chip selectors, form inputs).
  - `--icon-size-lg`: $24 \times 24\text{px}$ (Standard navigation items, card headers).
  - `--icon-size-xl`: $32 \times 32\text{px}$ (Hero status landmarks, large advisory badges).

### 2.2 Standard Agronomic and Status Glyphs

| Glyph Concept | Approved Vector Representation | Meaning in Ritucast |
| :--- | :---: | :--- |
| **Boro Rice / Crop** | Single upright grain sheaf (`wheat` / `sprout`) | Active crop context (বোরো ধান). |
| **Irrigation / Pump** | Water droplet with circular arrow (`droplet-sync`) | Tubewell irrigation status (সেচ ব্যবস্থাপনা). |
| **Flash Flood / Water** | Triple wave crest (`waves` / `cloud-rain-wind`) | Haor pre-monsoon flood threat (আকস্মিক বন্যা). |
| **Weather / Cloud** | Sun behind rain cloud (`cloud-sun-rain`) | 48-Hour rainfall and weather forecast. |
| **Soil Moisture** | Earth layer with water drop (`layers` / `droplet`) | Root-zone soil water deficit ($D_t$). |
| **AWD Field Tube** | Perforated pipe cylinder with water level line | Alternate Wetting & Drying field verification guide. |
| **Location / Pin** | Map pin marker (`map-pin`) | Active Upazila administrative boundary. |
| **Verified / Normal** | Enclosed checkmark (`check-circle-2`) | Verified observation; safe moisture level `[✓]`. |
| **Caution / Watch** | Triangle alert with exclamation (`alert-triangle`) | Near depletion limit; 48h flood watch `[⚠️]`. |
| **Emergency / Alert**| Flashing beacon / siren (`siren` / `alert-octagon`)| Immediate harvest alert; severe surge `[🚨]`. |
| **WhatsApp Share** | Chat bubble with share arrow (`share-2`) | One-click advisory broadcast to farmer groups. |

### 2.3 Accessibility Rules for Icons
- Standalone icon buttons (e.g., share button, close drawer) must feature an explicit `aria-label` in Bangla (e.g., `<button aria-label="তথ্যসূত্র বন্ধ করুন">`).
- Icons accompanied by visible text labels must include `aria-hidden="true"` to prevent redundant screen reader announcements.

---

## 3. Photographic Imagery Guidelines

### 3.1 Permitted Imagery Categories
1. **Authentic Field Demonstrations**: Photos of real Bangladeshi farmers checking Alternate Wetting and Drying (AWD) perforated field tubes in Barind clay soil.
2. **Crop Phenology Reference Guides**: Clear close-up macro shots of Boro rice at verified phenological stages (Tillering, Panicle Initiation, Flowering, Grain Filling, 80% Maturity).
3. **Embankment & River Gauges**: Photos illustrating BWDB river stage markers along the Surma River in Sunamganj.

### 3.2 Strict Photography Prohibitions
- **NO Foreign Stock Imagery**: Zero photos of Western commercial farming (massive green combines, pivot sprinklers, corn, wheat combines).
- **NO Stylized Drone Renderings**: Do not display mock 3D drone renders that mislead farmers into expecting sub-acre automated parcel tracking.
- **NO Face Exploitation**: Avoid patronizing imagery depicting impoverished farmers looking helpless. Imagery must present farmers as skilled, dignified decision-makers.

### 3.3 Technical Optimization & Licensing
- All photographic assets must be encoded in modern **WebP format** with responsive `srcset` resolutions ($360\text{w}, 720\text{w}, 1080\text{w}$).
- Maximum file size per image: **$\le 80\text{KB}$**.
- Every photo must possess full documentation of open creative commons or project-owned rights with zero royalty encumbrances.
