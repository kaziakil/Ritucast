/**
 * TypeScript interfaces matching Phase 10 backend OpenAPI contract.
 */

export interface CentroidCoord {
  lat: number;
  lon: number;
}

export interface UpazilaSummary {
  upazila_id: string;
  name_en: string;
  name_bn: string;
  district_name: string;
  division_name: string;
  aez_code: number;
  aez_name: string;
  centroid: CentroidCoord;
  primary_risk: string;
  district_id?: string;
  division_id?: string;
  district_name_bn?: string;
  division_name_bn?: string;
  is_pilot?: boolean;
}

export interface UpazilaHierarchyItem {
  id: string;
  upazila_id: string;
  name_en: string;
  name_bn: string;
  district_id: string;
  division_id: string;
  lat: number;
  lon: number;
  is_pilot?: boolean;
}

export interface DistrictHierarchyItem {
  id: string;
  district_id: string;
  division_id: string;
  name_en: string;
  name_bn: string;
  aez_code: number;
  aez_name: string;
  primary_risk: string;
  upazilas: UpazilaHierarchyItem[];
}

export interface DivisionHierarchyItem {
  id: string;
  division_id: string;
  name_en: string;
  name_bn: string;
  districts: DistrictHierarchyItem[];
}

export interface GeoHierarchyData {
  metadata: {
    total_divisions: number;
    total_districts: number;
    total_upazilas: number;
  };
  divisions: DivisionHierarchyItem[];
  districts_flat?: Record<string, any>;
  upazilas_flat?: Record<string, UpazilaSummary>;
}

export interface UpazilaDetail extends UpazilaSummary {
  area_sq_km?: number;
  unions_count?: number;
  elevation_m?: number;
  calibrated_crops?: string[];
}

export interface CropInfo {
  crop_id: string;
  name_en: string;
  name_bn: string;
  scientific_name: string;
  category?: string;
  category_en?: string;
  category_bn?: string;
  typical_duration_days: number;
  supported_stages: string[];
  calibration_status: string;
  primary_season?: string;
  kc_mid?: number;
  analytical_support_description?: string;
}

export interface SeasonInfo {
  season_id: string;
  name_en: string;
  name_bn: string;
  start_month: string;
  end_month: string;
  primary_crops: string[];
  is_active_season: boolean;
}

export interface WeatherDailyObservation {
  date: string;
  temp_max_c: number;
  temp_min_c: number;
  solar_radiation_mj_m2: number;
  precip_24h_mm: number;
  rh_mean_pct: number;
  wind_speed_ms?: number;
}

export interface WeatherDailyForecast {
  date: string;
  lead_time_h: number;
  temp_max_c: number;
  temp_min_c: number;
  qpf_precip_mm: number;
  precip_probability_pct: number;
  confidence: string;
}

export interface WeatherFeedResponse {
  upazila_id: string;
  name_bn: string;
  timezone: string;
  tier_1_observations: {
    source: string;
    updated_at_bst: string;
    yesterday: WeatherDailyObservation;
  };
  tier_3_forecasts: {
    model_sources: string[];
    issued_at_bst: string;
    ensemble_spread_pct: number;
    daily_forecast: WeatherDailyForecast[];
  };
}

export interface SoilPropertiesSchema {
  texture: string;
  root_zone_depth_m: number;
  total_available_water_taw_mm: number;
  readily_available_water_raw_mm: number;
}

export interface WaterBalanceIndicators {
  calculation_date: string;
  fao56_et0_mm_day: number;
  calibrated_kc: number;
  crop_etc_mm_day: number;
  soil_properties: SoilPropertiesSchema;
  current_soil_water_deficit_dt_mm: number;
  status: string;
  status_bn: string;
}

export interface WaterBalanceResponse {
  upazila_id: string;
  crop_id: string;
  growth_stage: string;
  tier_2_indicators: WaterBalanceIndicators;
  provenance: Record<string, any>;
}

export interface FloodHazardIndicators {
  evaluation_timestamp_bst: string;
  flood_hazard_index_iflood: number;
  hazard_tier: 'NORMAL' | 'ADVISORY' | 'WARNING' | 'EMERGENCY' | 'NOT_APPLICABLE';
  hazard_tier_bn: string;
  sub_indices: Record<string, number>;
  trigger_early_harvest: boolean;
}

export interface FloodHazardResponse {
  upazila_id: string;
  name_bn: string;
  tier_2_indicators: FloodHazardIndicators;
  provenance: Record<string, any>;
}

export interface Tier1ObservationSummary {
  summary_bn: string;
  rainfall_7d_total_mm?: number;
  mean_temp_c?: number;
}

export interface Tier2IndicatorSummary {
  summary_bn: string;
  soil_water_deficit_dt_mm?: number;
  fao56_et0_mm_day?: number;
  flood_hazard_index_iflood?: number;
}

export interface Tier3PredictionSummary {
  summary_bn: string;
  rain_probability_48h_pct?: number;
  qpf_48h_mm?: number;
  ensemble_spread_pct?: number;
}

export interface Tier4RecommendationDetail {
  rule_id: string;
  category: string;
  action_code: string;
  severity: 'INFO' | 'ADVISORY' | 'WARNING' | 'EMERGENCY';
  headline_bn: string;
  body_bn: string;
  mandatory_disclaimer_bn: string;
  action_items_bn: string[];
  rationale_breakdown: Record<string, any>;
  confidence: {
    score: number;
    tier: string;
    tier_bn: string;
    color_hex?: string;
  };
  is_suppressed: boolean;
  suppression_reason?: string;
}

export interface AdvisoryResponse {
  upazila_id: string;
  upazila_name_bn: string;
  crop_id: string;
  crop_name_bn: string;
  growth_stage: string;
  growth_stage_bn: string;
  generated_at_bst: string;
  tier_1_observations: Tier1ObservationSummary;
  tier_2_indicators: Tier2IndicatorSummary;
  tier_3_predictions: Tier3PredictionSummary;
  tier_4_recommendation: Tier4RecommendationDetail;
  all_cards?: any[];
  provenance: Record<string, any>;
  analysis_period?: {
    start_date: string;
    end_date: string;
    period_days: number;
    reporting_latency_note_bn?: string;
    reporting_latency_note_en?: string;
  };
}

export interface PhysicalHazardAssessment {
  hazard_domain: string;
  hazard_tier: 'LOW' | 'MODERATE' | 'HIGH' | 'CRITICAL';
  hazard_tier_bn: string;
  primary_metric_name: string;
  primary_metric_value: number;
  threshold_applied: number;
  action_warranted: boolean;
}

export interface RiskEvaluationResponse {
  upazila_id: string;
  crop_id: string;
  growth_stage: string;
  evaluation_date: string;
  overall_hazard_tier: string;
  overall_hazard_tier_bn: string;
  hazard_assessments: PhysicalHazardAssessment[];
  scientific_disclaimer_bn: string;
  provenance: Record<string, string>;
}

export interface DatasetProvenanceItem {
  dataset_id: string;
  dataset_name: string;
  source_agency: string;
  spatial_coverage: string;
  temporal_resolution: string;
  latency_hours: number;
  latest_record_bst: string;
  license: string;
  status: string;
}

export interface ModelMethodologyItem {
  method_id: string;
  title: string;
  reference_standard: string;
  calibration_status: string;
}

export interface SystemProvenanceResponse {
  system_name: string;
  version: string;
  generated_at_bst: string;
  pilot_regions: string[];
  datasets: DatasetProvenanceItem[];
  scientific_methodologies: ModelMethodologyItem[];
  scientific_boundaries: Record<string, string>;
}

export interface HealthResponse {
  status: string;
  version: string;
  timestamp_utc: string;
}

export interface ReadinessResponse {
  status: string;
  data_store_ready: boolean;
  analytics_ready: boolean;
  verified_datasets: string[];
  missing_dependencies: string[];
}
