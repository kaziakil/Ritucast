import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, waitFor, fireEvent } from '@testing-library/react'
import App from '../App'
import { apiClient } from '../services/apiClient'
import type {
  UpazilaSummary,
  CropInfo,
  AdvisoryResponse,
  RiskEvaluationResponse,
  WaterBalanceResponse,
  FloodHazardResponse,
  ReadinessResponse,
} from '../types/api'

const mockUpazilas: UpazilaSummary[] = [
  {
    upazila_id: 'BD-50-20-30',
    name_en: 'Godagari',
    name_bn: 'গোদাগাড়ী',
    district_name: 'Rajshahi',
    division_name: 'Rajshahi',
    aez_code: 26,
    aez_name: 'High Barind Tract',
    centroid: { lat: 24.4667, lon: 88.3333 },
    primary_risk: 'Groundwater Deficit / Drought',
  },
  {
    upazila_id: 'BD-60-90-89',
    name_en: 'Tahirpur',
    name_bn: 'তাহিরপুর',
    district_name: 'Sunamganj',
    division_name: 'Sylhet',
    aez_code: 21,
    aez_name: 'Sylhet Basin / Haor',
    centroid: { lat: 25.0833, lon: 91.1833 },
    primary_risk: 'Early Pre-Monsoon Flash Flood',
  },
]

const mockCrops: CropInfo[] = [
  {
    crop_id: 'boro_rice',
    name_en: 'Boro Rice',
    name_bn: 'বোরো ধান',
    scientific_name: 'Oryza sativa L.',
    typical_duration_days: 145,
    supported_stages: ['vegetative', 'panicle_initiation', 'flowering', 'ripening'],
    calibration_status: 'CALIBRATED',
  },
]

const mockReadiness: ReadinessResponse = {
  status: 'ready',
  data_store_ready: true,
  analytics_ready: true,
  verified_datasets: ['nasa_power', 'bmd', 'sentinel_1'],
  missing_dependencies: [],
}

const mockAdvisoryGodagari: AdvisoryResponse = {
  upazila_id: 'BD-50-20-30',
  upazila_name_bn: 'গোদাগাড়ী',
  crop_id: 'boro_rice',
  crop_name_bn: 'বোরো ধান',
  growth_stage: 'panicle_initiation',
  growth_stage_bn: 'শীষ আসার সূচনা',
  generated_at_bst: '2026-10-10 12:00:00 BST',
  tier_1_observations: {
    summary_bn: 'গত ৭ দিনে মোট ৫.২ মিমি বৃষ্টিপাত হয়েছে।',
    rainfall_7d_total_mm: 5.2,
    mean_temp_c: 26.5,
  },
  tier_2_indicators: {
    summary_bn: 'মাটির আর্দ্রতা ঘাটতি ২৪.০ মিমি।',
    soil_water_deficit_dt_mm: 24.0,
    fao56_et0_mm_day: 3.8,
  },
  tier_3_predictions: {
    summary_bn: 'আগামী ৪৮ ঘণ্টায় মাঝারি বৃষ্টির সম্ভাবনা (৬৫%)।',
    rain_probability_48h_pct: 65,
    qpf_48h_mm: 18.0,
  },
  tier_4_recommendation: {
    rule_id: 'RULE-IRR-01',
    category: 'IRRIGATION_SCHEDULING',
    action_code: 'POSTPONE_IRRIGATION',
    severity: 'ADVISORY',
    headline_bn: 'আগামী ৪৮ ঘণ্টা সেচ স্থগিত রাখুন',
    body_bn: 'মাঝারি বৃষ্টির সম্ভাবনা থাকায় সেচ স্থগিত রাখা যুক্তিযুক্ত।',
    mandatory_disclaimer_bn: 'সেচ বন্ধ করার আগে জমির আইল এবং মাটির রস নিজে হাত দিয়ে পরীক্ষা করুন।',
    action_items_bn: [
      'পাম্প বন্ধ রাখুন',
      'আইলের পানি ধরে রাখার ব্যবস্থা নিন',
    ],
    rationale_breakdown: {
      scientific_basis: 'FAO-56 গণনা অনুযায়ী সম্ভাব্য বৃষ্টিপাত মাটির আর্দ্রতা পূরণ করবে।',
    },
    confidence: {
      score: 0.88,
      tier: 'HIGH',
      tier_bn: 'উচ্চ নির্ভরযোগ্যতা',
      color_hex: '#15803D',
    },
    is_suppressed: false,
  },
  provenance: {
    engine_version: '1.0.0',
    pilot_zone: 'High Barind Tract',
  },
}

const mockRisk: RiskEvaluationResponse = {
  upazila_id: 'BD-50-20-30',
  crop_id: 'boro_rice',
  growth_stage: 'panicle_initiation',
  evaluation_date: '2026-10-10',
  overall_hazard_tier: 'LOW',
  overall_hazard_tier_bn: 'কম ঝুঁকি',
  hazard_assessments: [
    {
      hazard_domain: 'DROUGHT',
      hazard_tier: 'LOW',
      hazard_tier_bn: 'কম',
      primary_metric_name: 'soil_water_deficit',
      primary_metric_value: 24.0,
      threshold_applied: 40.0,
      action_warranted: false,
    },
  ],
  scientific_disclaimer_bn: 'মাঠে সেচ বন্ধের পূর্বে মাটির রস সরাসরি হাত দিয়ে পরীক্ষা করুন।',
  provenance: {
    engine: 'Phase 9 Risk Evaluator',
  },
}

const mockWaterBalance: WaterBalanceResponse = {
  upazila_id: 'BD-50-20-30',
  crop_id: 'boro_rice',
  growth_stage: 'panicle_initiation',
  tier_2_indicators: {
    calculation_date: '2026-10-10',
    fao56_et0_mm_day: 3.8,
    calibrated_kc: 1.1,
    crop_etc_mm_day: 4.18,
    soil_properties: {
      texture: 'clay_loam',
      root_zone_depth_m: 0.5,
      total_available_water_taw_mm: 80.0,
      readily_available_water_raw_mm: 40.0,
    },
    current_soil_water_deficit_dt_mm: 24.5,
    status: 'OPTIMAL',
    status_bn: 'অনুকূল আর্দ্রতা',
  },
  provenance: {
    calculation_method: 'FAO-56 Dual Crop Coefficient',
  },
}

const mockFloodHazard: FloodHazardResponse = {
  upazila_id: 'BD-60-90-89',
  name_bn: 'তাহিরপুর',
  tier_2_indicators: {
    evaluation_timestamp_bst: '2026-10-10 12:00:00 BST',
    flood_hazard_index_iflood: 0.42,
    hazard_tier: 'ADVISORY',
    hazard_tier_bn: 'সতর্কতা',
    sub_indices: {
      sar_inundation_fraction: 0.15,
      water_level_anomaly: 0.35,
    },
    trigger_early_harvest: false,
  },
  provenance: {
    radar_source: 'Sentinel-1 C-band SAR',
  },
}

describe('Phase 12 End-to-End User Journey Integration Tests', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    vi.spyOn(apiClient, 'getReadiness').mockResolvedValue(mockReadiness)
    vi.spyOn(apiClient, 'getUpazilas').mockResolvedValue(mockUpazilas)
    vi.spyOn(apiClient, 'getCrops').mockResolvedValue(mockCrops)
    vi.spyOn(apiClient, 'getAdvisories').mockResolvedValue(mockAdvisoryGodagari)
    vi.spyOn(apiClient, 'evaluateRisk').mockResolvedValue(mockRisk)
    vi.spyOn(apiClient, 'getWaterBalance').mockResolvedValue(mockWaterBalance)
    vi.spyOn(apiClient, 'getFloodHazard').mockResolvedValue(mockFloodHazard)
  })

  it('completes the full end-to-end journey from pilot selection to 4-tier advisory rendering', async () => {
    render(<App />)

    // 1. Initial load verifies readiness and pilot Upazilas
    await waitFor(() => {
      expect(screen.getAllByText(/ঋতুকাস্ট/).length).toBeGreaterThan(0)
    })

    // 2. Verify Upazila select shows Godagari by default
    const upazilaSelect = screen.getByLabelText(/উপজেলা/i)
    expect(upazilaSelect).toBeInTheDocument()
    expect(screen.getByText(/গোদাগাড়ী \(Godagari\)/i)).toBeInTheDocument()

    // 3. Verify 4-tier advisory card rendered
    await waitFor(() => {
      expect(screen.getByText(/আগামী ৪৮ ঘণ্টা সেচ স্থগিত রাখুন/i)).toBeInTheDocument()
    })

    // 4. Verify Tier taxonomy badges and headings
    expect(screen.getAllByText(/পর্যবেক্ষণ/i).length).toBeGreaterThan(0)
    expect(screen.getAllByText(/হিসাবকৃত সূচক/i).length).toBeGreaterThan(0)
    expect(screen.getAllByText(/পূর্বাভাস/i).length).toBeGreaterThan(0)
    expect(screen.getAllByText(/কার্যকর পরামর্শ/i).length).toBeGreaterThan(0)

    // 5. Verify mandatory field check copy (DEC-10 / DEC-17)
    expect(screen.getAllByText(/সেচ বন্ধ করার আগে জমির আইল এবং মাটির রস নিজে হাত দিয়ে পরীক্ষা করুন/i).length).toBeGreaterThan(0)
  })

  it('navigates seamlessly across Water Balance and Haor Flash Flood Hazard views', async () => {
    render(<App />)

    await waitFor(() => {
      expect(screen.getByText(/আগামী ৪৮ ঘণ্টা সেচ স্থগিত রাখুন/i)).toBeInTheDocument()
    })

    // Switch to Water Balance tab
    const waterTab = screen.getByRole('button', { name: /মাটির আর্দ্রতা/i })
    fireEvent.click(waterTab)

    await waitFor(() => {
      expect(screen.getByText(/পর্যায়ক্রমিক ভেজানো ও শুকানো \(AWD\) নিরীক্ষণ/i)).toBeInTheDocument()
    })

    // Switch to Haor Flood Hazard tab
    const floodTab = screen.getByRole('button', { name: /হাওড় বন্যা ঝুঁকি/i })
    fireEvent.click(floodTab)

    await waitFor(() => {
      expect(screen.getAllByText(/হাওড়/i).length).toBeGreaterThan(0)
    })
  })

  it('handles backend service failure gracefully without crash', async () => {
    vi.spyOn(apiClient, 'getAdvisories').mockRejectedValue(new Error('Network error connecting to backend API'))
    vi.spyOn(apiClient, 'getWeather').mockRejectedValue(new Error('Network error connecting to backend API'))

    render(<App />)

    await waitFor(() => {
      expect(screen.getByText(/সার্ভার থেকে তথ্য পাওয়া যায়নি/i)).toBeInTheDocument()
    })
  })
})
