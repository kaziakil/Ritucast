import { describe, it, expect, vi } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import { ContextSelector } from '../components/ContextSelector'
import type { UpazilaSummary, CropInfo } from '../types/api'

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
    upazila_id: 'BD-60-90-86',
    name_en: 'Tahirpur',
    name_bn: 'তাহিরপুর',
    district_name: 'Sunamganj',
    division_name: 'Sylhet',
    aez_code: 21,
    aez_name: 'Haor Basin',
    centroid: { lat: 25.0833, lon: 91.1833 },
    primary_risk: 'Transboundary Flash Flood',
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

describe('ContextSelector Component', () => {
  it('renders upazila options and triggers change callback', () => {
    const handleUpazilaChange = vi.fn()
    const handleCropChange = vi.fn()
    const handleStageChange = vi.fn()
    const handleRefresh = vi.fn()

    render(
      <ContextSelector
        upazilas={mockUpazilas}
        selectedUpazilaId="BD-50-20-30"
        setSelectedUpazilaId={handleUpazilaChange}
        crops={mockCrops}
        selectedCropId="boro_rice"
        setSelectedCropId={handleCropChange}
        growthStages={['Tillering', 'Booting', 'Flowering']}
        selectedStage="Tillering"
        setSelectedStage={handleStageChange}
        onRefresh={handleRefresh}
        loading={false}
      />
    )

    expect(screen.getByText(/গোদাগাড়ী/)).toBeInTheDocument()
    expect(screen.getByText(/তাহিরপুর/)).toBeInTheDocument()

    const selectEl = screen.getByRole('combobox', { name: /উপজেলা/ })
    fireEvent.change(selectEl, { target: { value: 'BD-60-90-86' } })
    expect(handleUpazilaChange).toHaveBeenCalledWith('BD-60-90-86')
  })

  it('triggers refresh button when clicked', () => {
    const handleRefresh = vi.fn()

    render(
      <ContextSelector
        upazilas={mockUpazilas}
        selectedUpazilaId="BD-50-20-30"
        setSelectedUpazilaId={vi.fn()}
        crops={mockCrops}
        selectedCropId="boro_rice"
        setSelectedCropId={vi.fn()}
        growthStages={['Tillering']}
        selectedStage="Tillering"
        setSelectedStage={vi.fn()}
        onRefresh={handleRefresh}
        loading={false}
      />
    )

    const refreshBtn = screen.getByRole('button', { name: /হালনাগাদ/ })
    fireEvent.click(refreshBtn)
    expect(handleRefresh).toHaveBeenCalledTimes(1)
  })
})
