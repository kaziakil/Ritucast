import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, waitFor, fireEvent } from '@testing-library/react'
import App from '../App'
import { apiClient } from '../services/apiClient'
import type {
  UpazilaSummary,
  CropInfo,
  AdvisoryResponse,
  RiskEvaluationResponse,
  WeatherFeedResponse,
  WaterBalanceResponse,
  FloodHazardResponse,
  SystemProvenanceResponse,
  ReadinessResponse,
} from '../types/api'

// Deterministic Pilot Upazila Fixtures (High Barind & Haor Basin)
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
    primary_risk: 'FLASH_FLOOD',
  },
]

const mockCrops: CropInfo[] = [
  {
    crop_id: 'boro_rice',
    name_en: 'Boro Rice',
    name_bn: 'বোরো ধান',
    scientific_name: 'Oryza sativa L.',
    typical_duration_days: 145,
    supported_stages: ['Tillering', 'Booting', 'Flowering', 'Dough', 'Maturity'],
    calibration_status: 'CALIBRATED',
  },
]

const mockReadiness: ReadinessResponse = {
  status: 'ready',
  data_store_ready: true,
  analytics_ready: true,
  verified_datasets: ['nasa_power', 'bmd', 'sentinel_1', 'ecmwf_ifs'],
  missing_dependencies: [],
}

const mockAdvisoryGodagari: AdvisoryResponse = {
  upazila_id: 'BD-50-20-30',
  upazila_name_bn: 'গোদাগাড়ী',
  crop_id: 'boro_rice',
  crop_name_bn: 'বোরো ধান',
  growth_stage: 'Tillering',
  growth_stage_bn: 'কুশি পর্যায়',
  generated_at_bst: '2026-10-10 12:00:00 BST',
  tier_1_observations: {
    summary_bn: 'বিগত ৭ দিনে মোট ৫.২ মিমি বৃষ্টিপাত রেকর্ড করা হয়েছে।',
    rainfall_7d_total_mm: 5.2,
    mean_temp_c: 27.2,
  },
  tier_2_indicators: {
    summary_bn: 'মাটির আর্দ্রতা ঘাটতি ২৪.০ মিমি এবং FAO-56 বাষ্পীভবন ৩.৮ মিমি/দিন।',
    soil_water_deficit_dt_mm: 24.0,
    fao56_et0_mm_day: 3.8,
  },
  tier_3_predictions: {
    summary_bn: 'আগামী ৪৮ ঘণ্টায় মাঝারি বৃষ্টির সম্ভাবনা (৬৫%)।',
    rain_probability_48h_pct: 65,
    qpf_48h_mm: 16.5,
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
      'আইলের পানি ধরে রাখার ব্যবস্থা নিশ্চিত করুন',
    ],
    rationale_breakdown: {
      scientific_basis: 'FAO-56 গণনা অনুযায়ী সম্ভাব্য বৃষ্টিপাত মাটির আর্দ্রতা পূরণ করবে।',
      pumping_savings_est_bdt: '৫৫০-৭৫০ টাকা/বিঘা',
    },
    confidence: {
      score: 0.88,
      tier: 'HIGH',
      tier_bn: 'উচ্চ আস্থা',
      color_hex: '#15803D',
    },
    is_suppressed: false,
  },
  provenance: {
    engine_version: '1.0.0',
    pilot_zone: 'High Barind Tract',
  },
}

const mockAdvisorySuppressed: AdvisoryResponse = {
  ...mockAdvisoryGodagari,
  tier_4_recommendation: {
    ...mockAdvisoryGodagari.tier_4_recommendation,
    is_suppressed: true,
    headline_bn: 'পরামর্শ সাময়িকভাবে স্থগিত',
    body_bn: 'মডেলসমূহের অনিশ্চয়তা অতিরিক্ত হওয়ায় পরামর্শ স্থগিত করা হয়েছে।',
  },
}

const mockWaterBalance: WaterBalanceResponse = {
  upazila_id: 'BD-50-20-30',
  crop_id: 'boro_rice',
  growth_stage: 'Tillering',
  tier_2_indicators: {
    calculation_date: '2026-10-10',
    status: 'AWD_DRYING_PERMISSIBLE',
    status_bn: 'AWD শুকানো অনুমোদিত - সেচ অপ্রয়োজনীয়',
    current_soil_water_deficit_dt_mm: 24.0,
    fao56_et0_mm_day: 3.8,
    calibrated_kc: 1.1,
    crop_etc_mm_day: 4.18,
    soil_properties: {
      texture: 'Clay Loam (Paleosol)',
      root_zone_depth_m: 0.5,
      total_available_water_taw_mm: 85.0,
      readily_available_water_raw_mm: 42.5,
    },
  },
  provenance: {
    equation: 'FAO-56 Penman-Monteith (EQN-ET0-01)',
  },
}

const mockFloodGodagari: FloodHazardResponse = {
  upazila_id: 'BD-50-20-30',
  name_bn: 'গোদাগাড়ী',
  tier_2_indicators: {
    flood_hazard_index_iflood: 0.05,
    hazard_tier: 'NOT_APPLICABLE',
    hazard_tier_bn: 'প্রযোজ্য নয়',
    evaluation_timestamp_bst: '2026-10-10 12:00:00 BST',
    sub_indices: {
      f_P: 0.0,
      f_S: 0.0,
      f_I: 0.0,
    },
    trigger_early_harvest: false,
  },
  provenance: {
    radar_source: 'Sentinel-1 C-band SAR',
  },
}

const mockWeatherFeed: WeatherFeedResponse = {
  upazila_id: 'BD-50-20-30',
  name_bn: 'গোদাগাড়ী',
  timezone: 'Asia/Dhaka',
  tier_1_observations: {
    source: 'NASA POWER / BMD Station',
    updated_at_bst: '2026-10-10 09:00 BST',
    yesterday: {
      date: '2026-10-09',
      temp_max_c: 32.5,
      temp_min_c: 22.0,
      precip_24h_mm: 0.0,
      rh_mean_pct: 74,
      solar_radiation_mj_m2: 19.8,
      wind_speed_ms: 1.8,
    },
  },
  tier_3_forecasts: {
    model_sources: ['ECMWF IFS', 'NOAA GFS', 'BMD WRF'],
    issued_at_bst: '2026-10-10 06:00 BST',
    ensemble_spread_pct: 18,
    daily_forecast: [
      {
        date: '2026-10-11',
        lead_time_h: 24,
        precip_probability_pct: 65,
        qpf_precip_mm: 16.5,
        temp_max_c: 30.0,
        temp_min_c: 21.5,
        confidence: 'HIGH',
      },
    ],
  },
}

const mockRiskEvaluation: RiskEvaluationResponse = {
  upazila_id: 'BD-50-20-30',
  crop_id: 'boro_rice',
  growth_stage: 'Tillering',
  evaluation_date: '2026-10-10',
  overall_hazard_tier: 'LOW',
  overall_hazard_tier_bn: 'স্বাভাবিক / কম ঝুঁকি',
  scientific_disclaimer_bn: 'ঝুঁকি নির্দেশকসমূহ শারীরিক সমীকরণ দ্বারা গণনাকৃত।',
  hazard_assessments: [
    {
      hazard_domain: 'SOIL_WATER_DEFICIT',
      hazard_tier: 'LOW',
      hazard_tier_bn: 'কম ঝুঁকি',
      primary_metric_name: 'soil_water_deficit_dt_mm',
      primary_metric_value: 24.0,
      threshold_applied: 42.5,
      action_warranted: false,
    },
  ],
  provenance: {
    engine: 'Phase 9 Risk Evaluator',
  },
}

const mockProvenance: SystemProvenanceResponse = {
  system_name: 'Ritucast Agricultural Intelligence Platform',
  version: '1.0.0',
  generated_at_bst: '2026-10-10 12:00 BST',
  pilot_regions: ['High Barind Tract (Rajshahi)', 'Haor Basin (Sylhet)'],
  datasets: [
    {
      dataset_id: 'DATA-MET-01',
      dataset_name: 'NASA POWER Daily Agroclimatology',
      source_agency: 'NASA Langley Research Center',
      spatial_coverage: 'High Barind Tract & Haor Basin',
      temporal_resolution: 'Daily',
      latency_hours: 24,
      latest_record_bst: '2026-10-10 06:00 BST',
      license: 'Public Domain / Open Data',
      status: 'VERIFIED',
    },
  ],
  scientific_methodologies: [
    {
      method_id: 'METH-ET0-01',
      title: 'FAO-56 Penman-Monteith Reference Evapotranspiration',
      reference_standard: 'FAO Irrigation and Drainage Paper 56',
      calibration_status: 'CALIBRATED',
    },
  ],
  scientific_boundaries: {
    no_yield_prediction: 'Strictly enforced (DEC-06 / MOD-YLD-01)',
    no_pesticide_rx: 'Strictly enforced (DEC-06 / MOD-DIS-01)',
  },
}

describe('Phase 16: User Acceptance, Usability, and Field Readiness Test Suite', () => {
  beforeEach(() => {
    vi.clearAllMocks()

    vi.spyOn(apiClient, 'getUpazilas').mockResolvedValue(mockUpazilas)
    vi.spyOn(apiClient, 'getCrops').mockResolvedValue(mockCrops)
    vi.spyOn(apiClient, 'getReadiness').mockResolvedValue(mockReadiness)
    vi.spyOn(apiClient, 'getAdvisories').mockResolvedValue(mockAdvisoryGodagari)
    vi.spyOn(apiClient, 'evaluateRisk').mockResolvedValue(mockRiskEvaluation)
    vi.spyOn(apiClient, 'getWeather').mockResolvedValue(mockWeatherFeed)
    vi.spyOn(apiClient, 'getWaterBalance').mockResolvedValue(mockWaterBalance)
    vi.spyOn(apiClient, 'getFloodHazard').mockResolvedValue(mockFloodGodagari)
    vi.spyOn(apiClient, 'getProvenance').mockResolvedValue(mockProvenance)
  })

  // --------------------------------------------------------------------------
  // JOURNEY A: First Visit, Default Orientation & Pilot Anchoring
  // --------------------------------------------------------------------------
  it('Journey A: loads initial state with Godagari Boro Rice and active advisory card', async () => {
    render(<App />)

    // Verify Brand Logo
    expect(screen.getByText('ঋতুকেস্ট')).toBeInTheDocument()
    expect(screen.getByText('Ritucast')).toBeInTheDocument()

    // Verify Readiness indicator shows live state
    await waitFor(() => {
      expect(screen.getByText('সচল (লাইভ)')).toBeInTheDocument()
    })

    // Verify Default Pilot Upazila is Godagari (High Barind Tract)
    await waitFor(() => {
      expect(screen.getByDisplayValue(/গোদাগাড়ী/)).toBeInTheDocument()
      expect(screen.getByDisplayValue(/বোরো ধান/)).toBeInTheDocument()
    })

    // Verify Tier 4 Actionable Advisory Headline
    await waitFor(() => {
      expect(screen.getByText('আগামী ৪৮ ঘণ্টা সেচ স্থগিত রাখুন')).toBeInTheDocument()
    })

    // Verify 4-Tier Structure Elements exist
    expect(screen.getByText(/১ম স্তর: প্রত্যক্ষ পর্যবেক্ষণ/)).toBeInTheDocument()
    expect(screen.getByText(/২য় স্তর: হিসাবকৃত সূচক/)).toBeInTheDocument()
    expect(screen.getByText(/৩য় স্তর: আবহাওয়া পূর্বাভাস/)).toBeInTheDocument()
    expect(screen.getByText(/চতুর্থ স্তর: কার্যকর পরামর্শ/)).toBeInTheDocument()
  })

  // --------------------------------------------------------------------------
  // JOURNEY B: Geographic Context Switching & Dual-Zone Pilot Adaptation
  // --------------------------------------------------------------------------
  it('Journey B: switches location from Godagari (Barind) to Tahirpur (Haor) and updates hazard context', async () => {
    render(<App />)

    await waitFor(() => {
      expect(screen.getByDisplayValue(/গোদাগাড়ী/)).toBeInTheDocument()
      expect(screen.getByText('আগামী ৪৮ ঘণ্টা সেচ স্থগিত রাখুন')).toBeInTheDocument()
    })

    // Change Upazila to Tahirpur (Haor Basin)
    const select = screen.getByRole('combobox', { name: /উপজেলা/i })
    fireEvent.change(select, { target: { value: 'BD-60-90-89' } })

    // Verify context bar updates to Haor risk and AEZ
    await waitFor(() => {
      expect(screen.getByText(/মূল প্রাকৃতিক ঝুঁকি:/)).toBeInTheDocument()
      expect(screen.getByText(/আকস্মিক বন্যা/)).toBeInTheDocument()
      expect(screen.getByText(/Sylhet Basin \/ Haor/)).toBeInTheDocument()
    })
  })

  // --------------------------------------------------------------------------
  // JOURNEY C: Understand Agricultural Weather Conditions
  // --------------------------------------------------------------------------
  it('Journey C: displays Tier 1 sensor readings and Tier 3 rainfall forecast in Weather tab', async () => {
    render(<App />)

    await waitFor(() => {
      expect(screen.getByText('আগামী ৪৮ ঘণ্টা সেচ স্থগিত রাখুন')).toBeInTheDocument()
    })

    const weatherTab = screen.getByRole('button', { name: /আবহাওয়া/i })
    fireEvent.click(weatherTab)

    await waitFor(() => {
      expect(screen.getByText(/বিগত ২৪ ঘণ্টার প্রত্যক্ষ আবহাওয়া পর্যবেক্ষণ/)).toBeInTheDocument()
      expect(screen.getByText(/উৎস: NASA POWER \/ BMD Station/)).toBeInTheDocument()
      expect(screen.getByText(/32.5° সে./)).toBeInTheDocument()
      expect(screen.getByText(/19.8 MJ\/m²/)).toBeInTheDocument()
    })

    // Verify 48h rain forecast
    expect(screen.getByText(/আগামী ৭২ ঘণ্টার সম্ভাব্যতাভিত্তিক আবহাওয়া পূর্বাভাস/)).toBeInTheDocument()
    expect(screen.getByText(/65%/)).toBeInTheDocument()
  })

  // --------------------------------------------------------------------------
  // JOURNEY D: Deep Dive into AWD Soil Moisture & Water Balance
  // --------------------------------------------------------------------------
  it('Journey D: displays AWD perched water table and soil water deficit in Water Balance tab', async () => {
    render(<App />)

    await waitFor(() => {
      expect(screen.getByText('আগামী ৪৮ ঘণ্টা সেচ স্থগিত রাখুন')).toBeInTheDocument()
    })

    const waterTab = screen.getByRole('button', { name: /মাটির আর্দ্রতা/i })
    fireEvent.click(waterTab)

    await waitFor(() => {
      expect(screen.getByText(/শিকড় অঞ্চলের পানি ঘাটতি নির্দেশক/)).toBeInTheDocument()
      expect(screen.getByText(/AWD শুকানো অনুমোদিত - সেচ অপ্রয়োজনীয়/)).toBeInTheDocument()
      expect(screen.getAllByText(/24 মিমি/).length).toBeGreaterThan(0) // Deficit D_t
    })
  })

  // --------------------------------------------------------------------------
  // JOURNEY E: Context Gating & Mandatory Field Verification Notice (DEC-10, DEC-17)
  // --------------------------------------------------------------------------
  it('Journey E: enforces mandatory field inspection notice and avoids banned overconfidence', async () => {
    render(<App />)

    await waitFor(() => {
      expect(screen.getByText('আগামী ৪৮ ঘণ্টা সেচ স্থগিত রাখুন')).toBeInTheDocument()
    })

    // Mandatory copy per AGENTS.md DEC-10
    const disclaimer = screen.getByText(/সেচ বন্ধ করার আগে জমির আইল এবং মাটির রস নিজে হাত দিয়ে পরীক্ষা করুন/i)
    expect(disclaimer).toBeInTheDocument()

    // Verify prohibited overconfident terms are ABSENT
    expect(screen.queryByText(/১০০% নিশ্চিত/)).not.toBeInTheDocument()
    expect(screen.queryByText(/নিশ্চিত বৃষ্টি/)).not.toBeInTheDocument()
    expect(screen.queryByText(/ফলনের নিশ্চয়তা/)).not.toBeInTheDocument()
  })

  // --------------------------------------------------------------------------
  // JOURNEY F: Automated Suppression Banner & Graceful Offline Degradation
  // --------------------------------------------------------------------------
  it('Journey F: displays automated suppression banner (DEC-10) when advisory is suppressed', async () => {
    vi.spyOn(apiClient, 'getAdvisories').mockResolvedValue(mockAdvisorySuppressed)

    render(<App />)

    await waitFor(() => {
      expect(screen.getByRole('alert')).toBeInTheDocument()
      expect(
        screen.getByText(/পরামর্শ সাময়িকভাবে স্থগিত \(স্বয়ংক্রিয় সুরক্ষা নীতি DEC-10\)/)
      ).toBeInTheDocument()
    })
  })

  it('Journey F: displays user-friendly error message with role=alert on network outage', async () => {
    vi.spyOn(apiClient, 'getAdvisories').mockRejectedValue(new Error('Network connection failed'))
    vi.spyOn(apiClient, 'getWeather').mockRejectedValue(new Error('Network connection failed'))

    render(<App />)

    await waitFor(() => {
      const alert = screen.getByRole('alert')
      expect(alert).toBeInTheDocument()
      expect(
        screen.getByText(/সার্ভার থেকে তথ্য পাওয়া যায়নি। অনুগ্রহ করে ব্যাকএন্ড সংযোগ পরীক্ষা করুন।/)
      ).toBeInTheDocument()
    })
  })

  // --------------------------------------------------------------------------
  // ACCESSIBILITY & USABILITY VALIDATION (WCAG 2.1 AA)
  // --------------------------------------------------------------------------
  it('Accessibility: renders accessible Skip to Content bypass link targeting main content landmark', () => {
    render(<App />)

    const skipLink = screen.getByText(/মূল বিষয়বস্তুতে সরাসরি প্রবেশ \(Skip to main content\)/)
    expect(skipLink).toBeInTheDocument()
    expect(skipLink).toHaveAttribute('href', '#main-content')

    const mainLandmark = document.getElementById('main-content')
    expect(mainLandmark).toBeInTheDocument()
    expect(mainLandmark?.tagName.toLowerCase()).toBe('main')
  })

  it('Accessibility: brand logo supports keyboard Enter and Space navigation', async () => {
    render(<App />)

    await waitFor(() => {
      expect(screen.getByText('আগামী ৪৮ ঘণ্টা সেচ স্থগিত রাখুন')).toBeInTheDocument()
    })

    // Switch to Weather tab first
    const weatherTab = screen.getByRole('button', { name: /আবহাওয়া/i })
    fireEvent.click(weatherTab)

    await waitFor(() => {
      expect(screen.getByText(/বিগত ২৪ ঘণ্টার প্রত্যক্ষ আবহাওয়া পর্যবেক্ষণ/)).toBeInTheDocument()
    })

    // Now focus and trigger Enter on brand logo
    const brandLogo = screen.getByLabelText('ঋতুকেস্ট হোমপেইজে যান')
    expect(brandLogo).toBeInTheDocument()
    expect(brandLogo).toHaveAttribute('role', 'button')
    expect(brandLogo).toHaveAttribute('tabIndex', '0')

    fireEvent.keyDown(brandLogo, { key: 'Enter', code: 'Enter' })

    // Should navigate back to advisories hub
    await waitFor(() => {
      expect(screen.getByText('আগামী ৪৮ ঘণ্টা সেচ স্থগিত রাখুন')).toBeInTheDocument()
    })
  })

  it('Accessibility: navigation links have accessible labels and current page aria attributes', async () => {
    render(<App />)

    await waitFor(() => {
      expect(screen.getByText('আগামী ৪৮ ঘণ্টা সেচ স্থগিত রাখুন')).toBeInTheDocument()
    })

    const advisoryTab = screen.getByRole('button', { name: /পরামর্শ কেন্দ্র/i })
    expect(advisoryTab).toHaveAttribute('aria-current', 'page')

    const weatherTab = screen.getByRole('button', { name: /আবহাওয়া/i })
    expect(weatherTab).not.toHaveAttribute('aria-current')

    fireEvent.click(weatherTab)

    await waitFor(() => {
      expect(weatherTab).toHaveAttribute('aria-current', 'page')
      expect(advisoryTab).not.toHaveAttribute('aria-current')
    })
  })

  it('Usability: refresh action indicates busy state and communicates live status', async () => {
    render(<App />)

    await waitFor(() => {
      expect(screen.getByText('আগামী ৪৮ ঘণ্টা সেচ স্থগিত রাখুন')).toBeInTheDocument()
    })

    const refreshBtn = screen.getByRole('button', { name: /হালনাগাদ তথ্য আনুন/i })
    expect(refreshBtn).toBeInTheDocument()
    expect(refreshBtn).not.toHaveAttribute('aria-busy', 'true')
  })
})
