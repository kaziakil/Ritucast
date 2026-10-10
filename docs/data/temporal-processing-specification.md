# Phase 8: Temporal Processing Specification

## 1. Executive Summary & Timezone Conventions

Environmental observations and meteorological forecasts arrive at radically different temporal resolutions and timeframes:
- **NASA POWER**: Daily observations with 24–48h latency (T+24 to T+48).
- **Open-Meteo**: Hourly and 3-hourly forecast projections updated 4 times daily (T0 to T+168h).
- **GPM IMERG**: Half-hourly satellite microwave/IR precipitation (<6h latency for Early, T+3.5 months for Final).
- **Sentinel-1 SAR**: Ephemeral passes every 6 to 12 days over Bangladesh.
- **SMAP**: Daily descending/ascending passes on a 2–3 day repeat cycle.

### Standard Timezone Protocol
- **Storage & Processing Standard**: All internal database records, Parquet timestamps, and API payloads are stored in **UTC (Coordinated Universal Time)** with explicit ISO-8601 formatting (`YYYY-MM-DDTHH:MM:SSZ`).
- **Local Agricultural Conversion**: When aggregating to local agricultural calendar days, the pipeline aligns to **Bangladesh Standard Time (BST, UTC+6)**:
  $$\text{BST} = \text{UTC} + 6\text{ hours}$$
- **Day Boundary Definition**: An agricultural meteorological day in Bangladesh runs from 00:00 BST to 23:59 BST (corresponding to 18:00 UTC of Day $D-1$ to 17:59 UTC of Day $D$).

---

## 2. Temporal Aggregation Operations

### 2.1 Daily Resampling Rules
| Variable | Native Temporal Resolution | Aggregation Method | Missing Threshold Rule |
| :--- | :--- | :--- | :--- |
| **Precipitation ($P$)** | Hourly / Half-Hourly | **Sum** ($\sum P_i$) | If $>2$ hours missing ($>8.3\%$), flag day as `PARTIAL_PRECIP`. |
| **Max Temperature ($T_{\text{max}}$)** | Hourly | **Maximum** ($\max T_i$) | Requires at least 1 reading between 12:00–16:00 BST. |
| **Min Temperature ($T_{\text{min}}$)** | Hourly | **Minimum** ($\min T_i$) | Requires at least 1 reading between 03:00–07:00 BST. |
| **Solar Radiation ($R_s$)** | Daily Total | **Direct Pass-through** | Daily total in $\text{MJ}/\text{m}^2/\text{day}$. |
| **Relative Humidity ($RH$)** | Hourly | **Mean** ($\frac{1}{24}\sum RH_i$) | Valid if $\ge 20$ hourly readings available. |
| **Wind Speed ($u_2$)** | Hourly | **Mean** ($\frac{1}{24}\sum u_i$) | Valid if $\ge 20$ hourly readings available. |

### 2.2 Rolling Cumulative Rain Windows
For flood early warning and soil moisture water-balance modeling, the pipeline computes deterministic rolling cumulative rainfall windows over daily time series:

$$P_{\text{cum}, 24\text{h}}(t) = P(t)$$

$$P_{\text{cum}, 48\text{h}}(t) = P(t) + P(t-1)$$

$$P_{\text{cum}, 7\text{d}}(t) = \sum_{k=0}^{6} P(t-k)$$

---

## 3. Growing Degree Day (GDD) Phenology Integration

To synchronize environmental variables with Boro rice growth stages (`DATA-AGR-01`), the pipeline calculates daily thermal accumulation (Growing Degree Days, GDD) above the biological base temperature for rice ($T_{\text{base}} = 10.0^\circ\text{C}$):

$$\text{GDD}_t = \max\left(0, \, \frac{T_{\text{max}, t} + T_{\text{min}, t}}{2} - T_{\text{base}}\right)$$

$$\text{Cumulative GDD} = \sum_{t=t_{\text{transplant}}}^{T} \text{GDD}_t$$

### Threshold Guardrails
- If $T_{\text{max}} > 35.0^\circ\text{C}$, apply the high-temperature cap: $T_{\text{max}} = 35.0^\circ\text{C}$ to account for thermal stress reduction in rice enzymatic activity.
- Phenology tracking by GDD prevents the 10–14 day seasonal shifts in Boro sowing dates from misidentifying flowering and harvest windows (`RSK-16`).

---

## 4. Epistemic Separation of Observation vs Forecast Timestamps

To enforce the 4-tier information taxonomy (`DEC-08`, `DEC-10`), every analytical record maintains two strictly separated timestamp attributes:
1. `observation_time_utc`: The physical sensor sensing date or forecast target valid time.
2. `retrieval_time_utc`: The system execution time when the data was extracted from the provider.
3. `is_forecast`: Boolean flag (`true` for Tier 3 NWP predictions, `false` for Tier 1 empirical observations).
4. `forecast_horizon_hours`: Integer lead time in hours (0 for observations; 1 to 168 for forecasts).
