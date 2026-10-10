import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import { FloodHazardView } from '../components/FloodHazardView'
import type { FloodHazardResponse } from '../types/api'

const mockHaorFlood: FloodHazardResponse = {
  upazila_id: 'tahirpur',
  name_bn: 'তাহিরপুর',
  tier_2_indicators: {
    evaluation_timestamp_bst: '2026-10-10 12:00:00 BST',
    flood_hazard_index_iflood: 0.68,
    hazard_tier: 'WARNING',
    hazard_tier_bn: 'সতর্কবার্তা (WARNING)',
    sub_indices: {
      upstream_rainfall_index: 0.72,
      water_level_rate_index: 0.65,
      sar_inundation_fraction: 0.28,
      soil_saturation_index: 0.75,
    },
    trigger_early_harvest: true,
  },
  provenance: {
    model: 'Haor Transboundary Flash Flood Index',
  },
}

const mockBarindFlood: FloodHazardResponse = {
  upazila_id: 'godagari',
  name_bn: 'গোদাগাড়ী',
  tier_2_indicators: {
    evaluation_timestamp_bst: '2026-10-10 12:00:00 BST',
    flood_hazard_index_iflood: 0.0,
    hazard_tier: 'NOT_APPLICABLE',
    hazard_tier_bn: 'প্রযোজ্য নয়',
    sub_indices: {},
    trigger_early_harvest: false,
  },
  provenance: {},
}

describe('FloodHazardView Component', () => {
  it('renders Haor flash flood hazard index and early harvest alert', () => {
    render(
      <FloodHazardView
        flood={mockHaorFlood}
        loading={false}
        error={null}
      />
    )

    expect(screen.getByText(/জরুরি ফসল কর্তন সতর্কতা/)).toBeInTheDocument()
    expect(screen.getByText('সতর্কবার্তা (WARNING)')).toBeInTheDocument()
    expect(screen.getByText(/হাওড়ে আকস্মিক বন্যার আশঙ্কা: ৮০% পাকা ধান অবিলম্বে কর্তন করুন/)).toBeInTheDocument()
  })

  it('renders non-applicable state for High Barind Tract', () => {
    render(
      <FloodHazardView
        flood={mockBarindFlood}
        loading={false}
        error={null}
      />
    )

    expect(screen.getByText('হাওড় আকস্মিক বন্যা ঝুঁকি সূচক প্রযোজ্য নয়')).toBeInTheDocument()
    expect(screen.getByText(/উচ্চ বরেন্দ্র অঞ্চলের \(AEZ-26\) অন্তর্গত/)).toBeInTheDocument()
  })
})
