# Phase 8: Data Storage, File Formats & Directory Conventions

## 1. Storage Tiers & Directory Hierarchy

The Ritucast data pipeline organizes data into five isolated storage tiers. This strict lifecycle isolation guarantees that raw external inputs are never mutated, interim processing remains reproducible, and analytical outputs published to Phase 9 are cryptographically verified.

```text
RITUCAST/
├── data/
│   ├── raw/                      # Immutable raw payloads (JSON responses, NetCDF chunks) [GIT-IGNORED]
│   │   ├── nasa_power/
│   │   ├── open_meteo/
│   │   ├── gpm_imerg/
│   │   ├── sentinel1_sar/
│   │   ├── smap_soil_moisture/
│   │   ├── hydrology_ffwc/
│   │   └── reference/
│   │
│   ├── interim/                  # Validated, parsed & reprojected intermediate artifacts [GIT-IGNORED]
│   │   ├── spatial_reprojected/
│   │   └── temporal_aligned/
│   │
│   ├── processed/                # Production-ready analytical feature tables [GIT-IGNORED]
│   │   ├── meteorology_daily.parquet
│   │   ├── forecast_hourly.parquet
│   │   ├── catchment_rainfall.parquet
│   │   ├── soil_moisture_zonal.parquet
│   │   └── manifests/            # JSON execution provenance manifests [GIT-TRACKED]
│   │
│   └── sample/                   # Small, synthetic fixtures for unit & integration testing [GIT-TRACKED]
│       ├── nasa_power_sample.json
│       ├── open_meteo_sample.json
│       ├── gpm_imerg_sample.json
│       ├── sentinel1_metadata_sample.json
│       ├── smap_sample.json
│       ├── bangladesh_pilot_upazilas.geojson
│       ├── brri_phenology_boro.json
│       └── bwdb_gauge_sample.json
│
├── configs/
│   └── datasets/                 # Explicit dataset configuration parameters [GIT-TRACKED]
│       ├── pilot_zones.json
│       ├── dataset_sources.json
│       └── validation_thresholds.json
│
├── pipelines/                    # Pipeline implementation package [GIT-TRACKED]
│   ├── common/
│   ├── ingestion/
│   ├── validation/
│   ├── processing/
│   └── orchestrator.py
│
└── tests/                        # Automated test suites [GIT-TRACKED]
```

---

## 2. File Format Conventions by Storage Tier

| Storage Tier | Data Modality | Approved File Format | Format Rationale | Retention Policy |
| :--- | :--- | :---: | :--- | :--- |
| **Raw Tier** (`data/raw/`) | REST API responses | `.json` / `.json.gz` | Exact bit-for-bit record of provider response. | 30 days rolling cache; auto-purged in production. |
| **Raw Tier** (`data/raw/`) | Gridded Satellite | `.nc4` / `.h5` / `.tif` | Native provider format preserving sensor grid metadata. | Ephemeral scratch storage; deleted after aggregation. |
| **Interim Tier** (`data/interim/`) | Vector & Tabular | `.parquet` / `.geojson` | Fast columnar reads, snappy compression, geometry preservation. | Pipeline run lifetime; overwritten on retry. |
| **Processed Tier** (`data/processed/`) | Analytical Features | `.parquet` | Columnar, strongly typed, dictionary encoded, zero read overhead for Phase 9. | Permanent analytical catalog; versioned per run. |
| **Provenance** (`data/processed/manifests/`) | Run Manifests | `.json` | Human and machine-readable cryptographic audit trail. | Permanent; committed to Git. |
| **Sample Tier** (`data/sample/`) | Test Fixtures | `.json` / `.geojson` | Lightweight synthetic data ($\le 50\text{KB}$ per file) allowing reproducible tests without internet. | Permanent in Git. |

---

## 3. Git Safety & Exclusion Rules

The root `.gitignore` enforces strict exclusions to guarantee that massive geospatial files, binary rasters, and secret keys are never committed:

```gitignore
# Large geospatial and satellite datasets
data/raw/
data/processed/
data/interim/
data/cache/
*.nc
*.nc4
*.hdf
*.h5
*.tif
*.tiff
*.geotiff
*.tar.gz
*.zip
*.parquet

# Allowed test fixtures
!data/sample/
!data/sample/**
!data/processed/manifests/
!data/processed/manifests/**
```

---

## 4. Analytical Table Naming & Schema Conventions

1. **Naming Standard**: `<domain>_<aggregation_frequency>_<target_entity>.parquet`
   - Example: `meteorology_daily_upazila.parquet`
   - Example: `hydrology_daily_catchment.parquet`
   - Example: `forecast_hourly_pilot.parquet`
2. **Keying Strategy**: Every analytical table is multi-keyed by:
   - `upazila_id`: Official BBS/GeoCode string identifier (e.g. `"BD-50-20-30"`).
   - `date` or `timestamp_utc`: ISO-8601 string or Date32 (`"YYYY-MM-DD"`).
   - `source_id`: Stable source identifier (e.g. `"DATA-MET-01"`).
3. **Immutability Principle**: Once published with a valid manifest, processed Parquet tables are treated as immutable snapshots. Re-runs write to temporary staging directories and atomically replace previous outputs only after passing the complete quality gate.
