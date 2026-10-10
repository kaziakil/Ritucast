import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import App from '../App'
import { apiClient } from '../services/apiClient'
import type {
  UpazilaSummary,
  CropInfo,
  AdvisoryResponse,
  RiskEvaluationResponse,
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
]

const mockCrops: CropInfo[] = [
  {
    crop_id: 'boro_rice',
    name_en: 'Boro Rice',
    name_bn: 'বোরো ধান',
    scientific_name: 'Oryza sativa L.',
    typical_duration_days: 145,
    supported_stages: ['Tillering', 'Booting', 'Flowering'],
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

const mockAdvisory: AdvisoryResponse = {
  upazila_id: 'BD-50-20-30',
  upazila_name_bn: 'গোদাগাড়ী',
  crop_id: 'boro_rice',
  crop_name_bn: 'বোরো ধান',
  growth_stage: 'Tillering',
  growth_stage_bn: 'কুশি গজানো',
  generated_at_bst: '2026-10-10 12:00:00 BST',
  tier_1_observations: {
    summary_bn: 'গত ৭ দিনে মোট ৫.২ মিমি বৃষ্টি রেকর্ড করা হয়েছে।',
  },
  tier_2_indicators: {
    summary_bn: 'মাটির বর্তমান আর্দ্রতা ঘাটতি স্বাভাবিক সীমার মধ্যে।',
  },
  tier_3_predictions: {
    summary_bn: 'আগামী ৪৮ ঘণ্টায় মাঝারি বৃষ্টির সম্ভাবনা।',
  },
  tier_4_recommendation: {
    rule_id: 'RULE-IRR-01',
    category: 'IRRIGATION_SCHEDULING',
    action_code: 'POSTPONE_IRRIGATION',
    severity: 'ADVISORY',
    headline_bn: 'আগামী ৪৮ ঘণ্টা সেচ স্থগিত রাখুন',
    body_bn: 'মাঝারি বৃষ্টির সম্ভাবনা থাকায় সেচ স্থগিত রাখুন।',
    mandatory_disclaimer_bn: 'সেচ বন্ধ করার আগে জমির আইল এবং মাটির রস নিজে হাত দিয়ে পরীক্ষা করুন।',
    action_items_bn: ['পাম্প বন্ধ রাখুন'],
    rationale_breakdown: {
      scientific_basis: 'QPF 48h পর্যাপ্ত।',
    },
    confidence: {
      score: 0.88,
      tier: 'HIGH',
      tier_bn: 'উচ্চ নির্ভরযোগ্যতা',
    },
    is_suppressed: false,
  },
  provenance: {},
}

const mockRisk: RiskEvaluationResponse = {
  upazila_id: 'BD-50-20-30',
  crop_id: 'boro_rice',
  growth_stage: 'Tillering',
  evaluation_date: '2026-10-10',
  overall_hazard_tier: 'LOW',
  overall_hazard_tier_bn: 'নিম্ন ঝুঁকি',
  hazard_assessments: [],
  scientific_disclaimer_bn: 'ভৌত ঝুঁকি মূল্যায়ন।',
  provenance: {},
}

describe('App Integration', () => {
  beforeEach(() => {
    vi.restoreAllMocks()
    vi.spyOn(apiClient, 'getReadiness').mockResolvedValue(mockReadiness)
    vi.spyOn(apiClient, 'getUpazilas').mockResolvedValue(mockUpazilas)
    vi.spyOn(apiClient, 'getCrops').mockResolvedValue(mockCrops)
    vi.spyOn(apiClient, 'getAdvisories').mockResolvedValue(mockAdvisory)
    vi.spyOn(apiClient, 'evaluateRisk').mockResolvedValue(mockRisk)
    vi.spyOn(apiClient, 'getWeather').mockResolvedValue(null as any)
    vi.spyOn(apiClient, 'getWaterBalance').mockResolvedValue(null as any)
    vi.spyOn(apiClient, 'getFloodHazard').mockResolvedValue(null as any)
    vi.spyOn(apiClient, 'getProvenance').mockResolvedValue(null as any)
  })

  it('mounts and renders initial advisory interface correctly', async () => {
    render(<App />)

    expect(screen.getAllByText(/ঋতুকাস্ট/).length).toBeGreaterThan(0)
    expect(screen.getAllByText('Ritucast').length).toBeGreaterThan(0)

    await waitFor(() => {
      expect(screen.getByText('আগামী ৪৮ ঘণ্টা সেচ স্থগিত রাখুন')).toBeInTheDocument()
    })

    expect(screen.getByText(/সেচ বন্ধ করার আগে জমির আইল এবং মাটির রস নিজে হাত দিয়ে পরীক্ষা করুন।/)).toBeInTheDocument()
  })
})
