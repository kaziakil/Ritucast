import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import { WaterBalanceView } from '../components/WaterBalanceView'
import type { WaterBalanceResponse } from '../types/api'

const mockWaterBalance: WaterBalanceResponse = {
  upazila_id: 'godagari',
  crop_id: 'boro_rice',
  growth_stage: 'tillering',
  tier_2_indicators: {
    calculation_date: '2026-10-10',
    fao56_et0_mm_day: 3.45,
    calibrated_kc: 1.1,
    crop_etc_mm_day: 3.8,
    current_soil_water_deficit_dt_mm: 12.4,
    status: 'AWD_DRYING_PERMISSIBLE',
    status_bn: 'AWD শুকানো অনুমোদিত - সেচ অপ্রয়োজনীয়',
    soil_properties: {
      texture: 'Clay Loam (Paleosol)',
      root_zone_depth_m: 0.4,
      total_available_water_taw_mm: 56.0,
      readily_available_water_raw_mm: 19.6,
    },
  },
  provenance: {
    equation: 'FAO-56 Penman-Monteith (EQN-ET0-01)',
  },
}

describe('WaterBalanceView Component', () => {
  it('renders FAO-56 Penman-Monteith ET0, ETc and depletion gauges correctly', () => {
    render(
      <WaterBalanceView
        waterBalance={mockWaterBalance}
        loading={false}
        error={null}
      />
    )

    expect(screen.getByText('AWD শুকানো অনুমোদিত - সেচ অপ্রয়োজনীয়')).toBeInTheDocument()
    expect(screen.getByText(/3.45/)).toBeInTheDocument() // ET0
    expect(screen.getByText(/3.8/)).toBeInTheDocument() // ETc
    expect(screen.getByText(/12.4/)).toBeInTheDocument() // Dt
    expect(screen.getAllByText(/56/).length).toBeGreaterThan(0) // TAW
  })
})
