import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import { AdvisoryHubView } from '../components/AdvisoryHubView'
import type { AdvisoryResponse, RiskEvaluationResponse } from '../types/api'

const mockAdvisory: AdvisoryResponse = {
  upazila_id: 'godagari',
  upazila_name_bn: 'গোদাগাড়ী',
  crop_id: 'boro_rice',
  crop_name_bn: 'বোরো ধান',
  growth_stage: 'tillering',
  growth_stage_bn: 'কুশি গজানো',
  generated_at_bst: '2026-10-10 12:00:00 BST',
  tier_1_observations: {
    summary_bn: 'গত ৭ দিনে মোট ৫.২ মিমি বৃষ্টি এবং গড় তাপমাত্রা ২৬.৫°সে রেকর্ড করা হয়েছে।',
    rainfall_7d_total_mm: 5.2,
    mean_temp_c: 26.5,
  },
  tier_2_indicators: {
    summary_bn: 'মাটির বর্তমান আর্দ্রতা ঘাটতি ১৮.৫ মিমি যা অনুমোদিত সীমার মধ্যে।',
    soil_water_deficit_dt_mm: 18.5,
    fao56_et0_mm_day: 3.45,
  },
  tier_3_predictions: {
    summary_bn: 'আগামী ৪৮ ঘণ্টায় মাঝারি বৃষ্টির সম্ভাবনা (৬৫%) এবং মোট বৃষ্টিপাত আনুমানিক ২০ মিমি।',
    rain_probability_48h_pct: 65,
    qpf_48h_mm: 20.0,
    ensemble_spread_pct: 22,
  },
  tier_4_recommendation: {
    rule_id: 'RULE-IRR-01',
    category: 'IRRIGATION_SCHEDULING',
    action_code: 'POSTPONE_IRRIGATION',
    severity: 'ADVISORY',
    headline_bn: 'আগামী ৪৮ ঘণ্টা সেচ স্থগিত রাখুন',
    body_bn: 'মাঝারি বৃষ্টির সম্ভাবনা থাকায় সেচ বন্ধ রেখে অর্থ ও জ্বালানি সাশ্রয় করুন।',
    mandatory_disclaimer_bn: 'সেচ বন্ধ করার আগে জমির আইল এবং মাটির রস নিজে হাত দিয়ে পরীক্ষা করুন।',
    action_items_bn: [
      'পাম্প বন্ধ রাখুন এবং নালার মুখ পরিষ্কার রাখুন',
      'আইলের উচ্চতা বজায় রাখুন যাতে বৃষ্টির পানি ধরে রাখা যায়',
    ],
    rationale_breakdown: {
      scientific_basis: 'QPF 48h > 15mm এবং বর্তমান মাটি আর্দ্রতা পর্যাপ্ত।',
      pumping_savings_est_bdt: '৳৪৫০ (আনুমানিক ৪.৫ লিটার ডিজেল)',
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
    engine_version: '0.1.0',
  },
}

const mockSuppressedAdvisory: AdvisoryResponse = {
  ...mockAdvisory,
  tier_4_recommendation: {
    ...mockAdvisory.tier_4_recommendation,
    is_suppressed: true,
    suppression_reason: 'NWP ensemble spread exceeds 50% threshold (DEC-10)',
    headline_bn: 'পরামর্শ স্থগিত',
  },
}

const mockRisk: RiskEvaluationResponse = {
  upazila_id: 'godagari',
  crop_id: 'boro_rice',
  growth_stage: 'tillering',
  evaluation_date: '2026-10-10',
  overall_hazard_tier: 'LOW',
  overall_hazard_tier_bn: 'স্বাভাবিক / নিম্ন ঝুঁকি',
  hazard_assessments: [
    {
      hazard_domain: 'DROUGHT',
      hazard_tier: 'LOW',
      hazard_tier_bn: 'নিম্ন ঝুঁকি',
      primary_metric_name: 'Soil Water Deficit',
      primary_metric_value: 18.5,
      threshold_applied: 24.0,
      action_warranted: false,
    },
  ],
  scientific_disclaimer_bn: 'এটি একটি ভৌত ঝুঁকি মূল্যায়ন (DEC-06 অনুসারী)।',
  provenance: {},
}

describe('AdvisoryHubView Component', () => {
  it('renders active advisory with 4-tier indicators and mandatory disclaimer', () => {
    render(
      <AdvisoryHubView
        advisory={mockAdvisory}
        risk={mockRisk}
        loading={false}
        error={null}
      />
    )

    expect(screen.getByText('আগামী ৪৮ ঘণ্টা সেচ স্থগিত রাখুন')).toBeInTheDocument()
    expect(screen.getByText(/মাঝারি বৃষ্টির সম্ভাবনা থাকায়/)).toBeInTheDocument()
    expect(screen.getByText(/সেচ বন্ধ করার আগে জমির আইল এবং মাটির রস নিজে হাত দিয়ে পরীক্ষা করুন।/)).toBeInTheDocument()
    expect(screen.getByText(/পাম্প বন্ধ রাখুন/)).toBeInTheDocument()
    expect(screen.getByText(/৳৪৫০/)).toBeInTheDocument()
  })

  it('renders suppression banner when advisory is suppressed (DEC-10)', () => {
    render(
      <AdvisoryHubView
        advisory={mockSuppressedAdvisory}
        risk={mockRisk}
        loading={false}
        error={null}
      />
    )

    expect(screen.getByText(/পরামর্শ সাময়িকভাবে স্থগিত \(স্বয়ংক্রিয় সুরক্ষা নীতি DEC-10\)/)).toBeInTheDocument()
  })

  it('renders loading state properly', () => {
    render(
      <AdvisoryHubView
        advisory={null}
        risk={null}
        loading={true}
        error={null}
      />
    )

    expect(screen.getByTestId('advisory-loading-skeleton')).toBeInTheDocument()
  })
})
