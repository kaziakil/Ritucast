# Ritucast: Data Architecture & Relational Schema Specification

## 1. Executive Summary & Data Lifecycle

The Ritucast data platform transforms multi-source spaceborne observations and numerical weather predictions into structured, localized, and explainable agricultural insights. In accordance with the **Four-Tier Information Taxonomy (`DEC-08`, `NFR-SCI-01`)**, the data architecture maintains strict separation between empirical measurements, physical indicators, probabilistic forecasts, and operational recommendations.

```mermaid
flowchart TD
    subgraph S1[Stage 1: External Sourcing]
        E1[NASA POWER Daily]
        E2[Open-Meteo NWP 7-Day]
        E3[GPM IMERG V07 Early]
        E4[ESA CDSE Sentinel-1 SAR]
        E5[BWDB River Gauge Logs]
    end

    subgraph S2[Stage 2: Ingestion & Staging]
        W[Celery Ingestion Workers<br>Temporal & Spatial Windowing]
        ST[(GCS Bucket: Staged NetCDF/TIFF<br>7-Day Auto-Purge)]
    end

    subgraph S3[Stage 3: Validation & Processing]
        QC[5-Stage Quality Gate<br>Physical Range & Coordinate Check]
        TR[Spatial Zonal Aggregation<br>EPSG:4326 -> PostGIS Polygons]
    end

    subgraph S4[Stage 4: Analytical Persistence Tier: PostgreSQL 16 + PostGIS]
        T1[(Tier 1: Observations<br>raw physical readings)]
        T2[(Tier 2: Indicators<br>ET0, Deficit Dt, Iflood)]
        T3[(Tier 3: Forecasts<br>QPF, Prob %, Ensemble Spread)]
        T4[(Tier 4: Advisories<br>Action cards, Rationale, Provenance)]
    end

    subgraph S5[Stage 5: Caching & Delivery]
        REDIS[(Redis 7 Cache<br>Pre-computed Upazila JSON)]
        API[FastAPI Service -> PWA Client]
    end

    S1 --> S2 --> S3
    TR --> T1 & T2 & T3
    T1 & T2 & T3 --> T4
    T4 --> REDIS --> API
```

---

## 2. Relational Database Schema Blueprints (PostgreSQL 16 + PostGIS 3.4)

The database schema strictly mirrors the 4-tier taxonomy, with dedicated tables and spatial indices optimized for rapid upazila lookups:

```mermaid
erDiagram
    ADMINISTRATIVE_UPAZILAS ||--o{ METEOROLOGICAL_OBSERVATIONS : "records"
    ADMINISTRATIVE_UPAZILAS ||--o{ AGRONOMIC_INDICATORS : "evaluates"
    ADMINISTRATIVE_UPAZILAS ||--o{ WEATHER_FORECASTS : "predicts"
    ADMINISTRATIVE_UPAZILAS ||--o{ ACTIONABLE_ADVISORIES : "emits"
    ADMINISTRATIVE_UPAZILAS ||--o{ PHENOLOGY_CALENDARS : "calibrates"

    ADMINISTRATIVE_UPAZILAS {
        varchar upazila_id PK "e.g. BD-50-28"
        varchar name_en "Godagari"
        varchar name_bn "গোদাগাড়ী"
        varchar division_name "Rajshahi"
        varchar district_name "Rajshahi"
        integer aez_code "26"
        geometry geom "MultiPolygon WGS84"
        numeric soil_awc_mm_m "145.0"
        geometry centroid "Point WGS84"
    }

    METEOROLOGICAL_OBSERVATIONS {
        uuid obs_id PK
        varchar upazila_id FK
        date obs_date_bst
        numeric t_max_c
        numeric t_min_c
        numeric solar_rad_mj_m2
        numeric rh_mean_pct
        numeric wind_speed_2m_ms
        numeric precip_24h_mm
        varchar source_dataset
        timestamptz retrieval_timestamp
    }

    AGRONOMIC_INDICATORS {
        uuid ind_id PK
        varchar upazila_id FK
        date calc_date_bst
        numeric et0_fao56_mm
        numeric crop_etc_mm
        numeric soil_water_deficit_mm
        numeric catchment_rain_48h_mm
        numeric surma_stage_m
        numeric sar_inundation_pct
        numeric flood_hazard_index_iflood
        boolean heat_stress_flag
        boolean cold_shock_flag
    }

    WEATHER_FORECASTS {
        uuid fcst_id PK
        varchar upazila_id FK
        timestamptz issued_at_utc
        date forecast_date_bst
        integer lead_time_hours
        numeric qpf_precip_mm
        integer precip_prob_pct
        numeric temp_max_c
        numeric temp_min_c
        numeric ensemble_spread_pct
    }

    ACTIONABLE_ADVISORIES {
        uuid adv_id PK
        varchar upazila_id FK
        varchar crop_id "boro_rice"
        varchar growth_stage "vegetative_tillering"
        timestamptz generated_at_utc
        varchar rule_id "RULE-IRR-01"
        varchar category "IRRIGATION"
        text headline_bn
        text body_bn
        text rationale_bn
        numeric confidence_score "0.85"
        varchar confidence_tier "HIGH"
        boolean is_suppressed "false"
        jsonb provenance_metadata
    }
```

---

## 3. Spatial Data Architecture & Coordinate Reference Systems (CRS)

To guarantee mathematical accuracy across Bangladesh's geography:

| Spatial Dimension | Standard Convention | Technical Justification & Processing Rules |
| :--- | :--- | :--- |
| **Storage & API Standard** | **WGS84 (`EPSG:4326`)** | Universal global standard for GPS, GeoJSON, and web mapping. All spatial database tables store polygon boundaries and centroids in EPSG:4326. |
| **Projected Metric Computation (West)** | **UTM Zone 45N (`EPSG:32645`)** | Covers Western Bangladesh (Barind Tract, Rajshahi Division). Used by backend workers for precise metric distance, buffer, and area computations ($m^2$). |
| **Projected Metric Computation (East)** | **UTM Zone 46N (`EPSG:32646`)** | Covers Eastern Bangladesh (Haor Basin, Sylhet Division). Used for measuring catchment areas and flooded hectare calculations. |
| **Spatial Indexing** | **PostGIS GiST Indexing** | Spatial columns (`geom`) are indexed using Generalized Search Trees (`CREATE INDEX idx_upazila_geom ON administrative_upazilas USING GIST (geom);`). Enables sub-millisecond bounding box filtering. |
| **Area-Weighted Zonal Aggregation** | **Polygon Weighted Mean** | Coarse raster grid cells ($X_i$) intersecting upazila polygon $P$ are aggregated via area-weighting: $\bar{X} = \frac{\sum (X_i \cdot \text{Area}(X_i \cap P))}{\text{Area}(P)}$. Avoids unweighted center-point biases. |

---

## 4. Temporal Data Architecture & Timezone Conventions

Agricultural operations in Bangladesh follow local solar diurnal cycles, while spaceborne platforms and global weather models operate in Universal Coordinated Time (UTC).

### 4.1 Temporal Harmonization Protocol
1. **Internal Datastore Convention**: All timestamp columns (`retrieval_timestamp`, `issued_at_utc`, `generated_at_utc`) are stored strictly in **UTC with timezone (`timestamptz`)**.
2. **User-Facing Presentation Convention**: All dates presented in API responses, Bangla UI cards, and historical logs are converted to **Bangladesh Standard Time (BST = UTC+6)**.
3. **The 24-Hour Rainfall Day Alignment**:
   - The Bangladesh Meteorological Department (BMD) standard 24h rainfall day runs from **09:00 BST to 09:00 BST** (which corresponds to **03:00 UTC to 03:00 UTC**).
   - Backend ingestion workers aggregate half-hourly GPM IMERG rainfall grids across this exact $03:00\text{ UTC}$ window, eliminating timing mismatches between satellite accumulations and ground-truth gauges.

---

## 5. Data Freshness, Staleness Tracking & Retention Policy

```mermaid
graph LR
    Ingest[Data Ingestion Worker] --> TimeStamp[Attach Ingestion Timestamp: timestamptz]
    TimeStamp --> DB[(PostgreSQL & Redis)]
    
    DB --> Check{Age > 36 Hours?}
    Check -- Yes --> Suppress[Trigger Automated Suppression<br>Set is_suppressed = True<br>Emit Safe Fallback Copy]
    Check -- No --> Active[Active Advisory Emitted]
```

### 5.1 Freshness Auditing & Alert Thresholds
- **Critical Threshold ($\le 12\text{ hours}$)**: Fresh data; full confidence weighting applied.
- **Degraded Threshold ($12–36\text{ hours}$)**: Moderately aged data; confidence score decays proportionally (`DEC-18`).
- **Suppression Ceiling ($>36\text{ hours}$)**: **Mandatory Automated Suppression (`DEC-10`, `NFR-REL-03`)**. Active advisories are suppressed; fallback notice served.

### 5.2 Data Retention & Lifecycle Rules
- **Hot Analytical Tier (PostgreSQL / Redis)**: Active 7-day rolling forecasts and past 30 days of daily observations are retained in PostgreSQL and Redis for immediate API querying.
- **Historical Timeseries Tier (PostgreSQL Partitioning)**: Historical daily observations are partitioned by year (`PARTITION BY RANGE (obs_date_bst)`), indexed for multi-year baseline climatology.
- **Raw Satellite Storage (GCS Bucket)**: Staged raw NetCDF, HDF5, and GeoTIFF files have an automated **7-day Lifecycle Deletion Rule**, preventing storage cost bloat. Only processed tabular summaries and vector inundation polygons are permanently retained.
