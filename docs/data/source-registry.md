# Ritucast: Source Registry & Technical Endpoint Catalog

## 1. Catalog Architecture

This registry provides a consolidated technical inventory of all verified endpoints, protocols, collection identifiers, and coordinate bounding boxes for the Ritucast platform.

---

## 2. Technical Source Registry Table

```json
{
  "project": "Ritucast",
  "geographic_domain": {
    "name": "Bangladesh and Transboundary Catchments",
    "bounding_box_wgs84": {
      "min_longitude": 88.0,
      "min_latitude": 20.5,
      "max_longitude": 92.8,
      "max_latitude": 26.7
    },
    "meghalaya_upstream_box": {
      "min_longitude": 90.0,
      "min_latitude": 25.0,
      "max_longitude": 92.8,
      "max_latitude": 26.2
    },
    "epsg": 4326
  },
  "sources": [
    {
      "id": "DATA-MET-01",
      "name": "NASA POWER Daily Agrometeorology",
      "provider": "NASA Langley Research Center",
      "category": "Atmospheric Forcing",
      "status": "Verified / Initial Core",
      "priority": "P0",
      "api": {
        "type": "REST JSON",
        "base_url": "https://power.larc.nasa.gov/api/temporal/daily/point",
        "auth": "None",
        "parameters": [
          "T2M",
          "T2M_MAX",
          "T2M_MIN",
          "PRECTOTCORR",
          "RH2M",
          "WS2M",
          "ALLSKY_SFC_SW_DWN"
        ],
        "community": "AG",
        "rate_limit_per_min": 30
      }
    },
    {
      "id": "DATA-FCST-01",
      "name": "Open-Meteo Operational Weather Forecasts",
      "provider": "Open-Meteo / ECMWF / NOAA",
      "category": "Numerical Weather Prediction",
      "status": "Verified / Initial Core",
      "priority": "P0",
      "api": {
        "type": "REST JSON",
        "base_url": "https://api.open-meteo.com/v1/forecast",
        "auth": "None (Free Tier)",
        "models": ["ecmwf_ifs025", "gfs_seamless"],
        "rate_limit_daily": 10000
      }
    },
    {
      "id": "DATA-PCP-01",
      "name": "GPM IMERG Precipitation Estimates",
      "provider": "NASA GES DISC / GSFC",
      "category": "Multi-Satellite Precipitation",
      "status": "Verified / Initial Core",
      "priority": "P0",
      "cmr": {
        "short_name_final": "GPM_3IMERGDF",
        "short_name_early": "GPM_3IMERGDE",
        "version": "07",
        "auth": "NASA Earthdata Login (OAuth2)",
        "format": "HDF5 / NetCDF4"
      }
    },
    {
      "id": "DATA-SAR-01",
      "name": "Copernicus Sentinel-1 SAR GRD",
      "provider": "European Space Agency (ESA) CDSE",
      "category": "Synthetic Aperture Radar",
      "status": "Verified / Initial Core",
      "priority": "P1",
      "cdse": {
        "collection": "SENTINEL-1",
        "product_type": "GRD",
        "sensor_mode": "IW",
        "polarization": "VV+VH",
        "odata_endpoint": "https://catalogue.dataspace.copernicus.eu/odata/v1/Products",
        "auth": "CDSE Keycloak Bearer Token"
      }
    },
    {
      "id": "DATA-SMC-01",
      "name": "SMAP Enhanced L3 Radiometer Soil Moisture",
      "provider": "NASA JPL / NSIDC DAAC",
      "category": "Soil Moisture",
      "status": "Verified / Initial Core",
      "priority": "P1",
      "cmr": {
        "short_name": "SPL3SMP_E",
        "version": "006",
        "grid": "EASE-Grid 2.0 9km",
        "auth": "NASA Earthdata Login (OAuth2)",
        "format": "HDF5"
      }
    },
    {
      "id": "DATA-BND-01",
      "name": "Bangladesh Administrative Boundaries Level 0-3",
      "provider": "BBS / Survey of Bangladesh / UN OCHA HDX",
      "category": "Geospatial Vector",
      "status": "Verified / Initial Core",
      "priority": "P0",
      "format": "GeoJSON / TopoJSON",
      "units_count": 495
    },
    {
      "id": "DATA-AGR-01",
      "name": "BRRI / BARI Modern Crop Calendars and Kc Tables",
      "provider": "BRRI / BARI / DAE",
      "category": "Agronomic Phenology",
      "status": "Verified / Initial Core",
      "priority": "P0",
      "format": "Relational Tables / JSON Mapping",
      "anchor_crops": ["Boro Rice", "Potato", "Mustard"]
    },
    {
      "id": "DATA-HYD-01",
      "name": "BWDB FFWC River Stage Gauge Logs",
      "provider": "BWDB Flood Forecasting and Warning Centre",
      "category": "In-Situ Hydrology",
      "status": "Verified / Ground Reference",
      "priority": "P1",
      "format": "Web Bulletins / Tabular Records",
      "key_rivers": ["Surma", "Kushiyara", "Kangsha"]
    }
  ]
}
```
