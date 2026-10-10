import { describe, it, expect, vi } from 'vitest'
import { render, screen, fireEvent, within } from '@testing-library/react'
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

  it('searches upazilas using English and Bangla queries and displays autocomplete dropdown', () => {
    const handleUpazilaChange = vi.fn()

    render(
      <ContextSelector
        upazilas={mockUpazilas}
        selectedUpazilaId="BD-50-20-30"
        setSelectedUpazilaId={handleUpazilaChange}
        crops={mockCrops}
        selectedCropId="boro_rice"
        setSelectedCropId={vi.fn()}
        growthStages={['Tillering']}
        selectedStage="Tillering"
        setSelectedStage={vi.fn()}
        onRefresh={vi.fn()}
        loading={false}
      />
    )

    const searchInput = screen.getByPlaceholderText(/অনুসন্ধান করুন/i)

    // English search (case-insensitive)
    fireEvent.change(searchInput, { target: { value: 'tahir' } })
    const listbox = screen.getByRole('listbox')
    expect(listbox).toBeInTheDocument()
    const tahirOption = within(listbox).getByText(/Tahirpur/i)
    expect(tahirOption).toBeInTheDocument()

    // Select Tahirpur from dropdown
    fireEvent.click(tahirOption)
    expect(handleUpazilaChange).toHaveBeenCalledWith('BD-60-90-86')
    expect(screen.queryByRole('listbox')).not.toBeInTheDocument()

    // Bangla search
    fireEvent.change(searchInput, { target: { value: 'গোদাগাড়ী' } })
    const listboxBn = screen.getByRole('listbox')
    expect(listboxBn).toBeInTheDocument()
    expect(within(listboxBn).getByText(/গোদাগাড়ী/i)).toBeInTheDocument()
  })

  it('searches districts and updates upazila when district result is selected', () => {
    const handleUpazilaChange = vi.fn()

    const { container } = render(
      <ContextSelector
        upazilas={mockUpazilas}
        selectedUpazilaId="BD-50-20-30"
        setSelectedUpazilaId={handleUpazilaChange}
        crops={mockCrops}
        selectedCropId="boro_rice"
        setSelectedCropId={vi.fn()}
        growthStages={['Tillering']}
        selectedStage="Tillering"
        setSelectedStage={vi.fn()}
        onRefresh={vi.fn()}
        loading={false}
      />
    )

    const searchInput = screen.getByPlaceholderText(/অনুসন্ধান করুন/i)
    fireEvent.change(searchInput, { target: { value: 'Sunamganj' } })

    // Verify district match item exists inside listbox
    const districtItem = container.querySelector('#search-item-dist-Sunamganj') as HTMLElement
    expect(districtItem).toBeInTheDocument()

    fireEvent.click(districtItem)
    expect(handleUpazilaChange).toHaveBeenCalledWith('BD-60-90-86')
  })

  it('supports keyboard navigation (ArrowDown, Enter, Escape) in search results', () => {
    const handleUpazilaChange = vi.fn()

    render(
      <ContextSelector
        upazilas={mockUpazilas}
        selectedUpazilaId="BD-50-20-30"
        setSelectedUpazilaId={handleUpazilaChange}
        crops={mockCrops}
        selectedCropId="boro_rice"
        setSelectedCropId={vi.fn()}
        growthStages={['Tillering']}
        selectedStage="Tillering"
        setSelectedStage={vi.fn()}
        onRefresh={vi.fn()}
        loading={false}
      />
    )

    const searchInput = screen.getByPlaceholderText(/অনুসন্ধান করুন/i)
    fireEvent.change(searchInput, { target: { value: 'tahir' } })

    // Arrow down and press Enter to select
    fireEvent.keyDown(searchInput, { key: 'ArrowDown' })
    fireEvent.keyDown(searchInput, { key: 'Enter' })
    expect(handleUpazilaChange).toHaveBeenCalledWith('BD-60-90-86')

    // Escape closes dropdown
    fireEvent.change(searchInput, { target: { value: 'godagari' } })
    expect(screen.getByRole('listbox')).toBeInTheDocument()
    fireEvent.keyDown(searchInput, { key: 'Escape' })
    expect(screen.queryByRole('listbox')).not.toBeInTheDocument()
  })

  it('displays empty results notice when no matching location found and clears with X button', () => {
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
        onRefresh={vi.fn()}
        loading={false}
      />
    )

    const searchInput = screen.getByPlaceholderText(/অনুসন্ধান করুন/i)
    fireEvent.change(searchInput, { target: { value: 'NonExistentLocation' } })

    expect(screen.getByText('কোনো উপজেলা বা জেলা পাওয়া যায়নি')).toBeInTheDocument()

    // Clear button
    const clearBtn = screen.getByRole('button', { name: /মুছুন/i })
    fireEvent.click(clearBtn)
    expect(screen.queryByRole('listbox')).not.toBeInTheDocument()
    expect(searchInput).toHaveValue('')
  })
})
