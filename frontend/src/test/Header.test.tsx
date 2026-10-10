import { describe, it, expect, vi } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import { Header } from '../components/Header'
import type { ReadinessResponse } from '../types/api'

const mockReadiness: ReadinessResponse = {
  status: 'ready',
  data_store_ready: true,
  analytics_ready: true,
  verified_datasets: ['nasa_power', 'bmd', 'sentinel_1'],
  missing_dependencies: [],
}

describe('Header Component', () => {
  it('renders branding and readiness badge', () => {
    render(
      <Header
        activeTab="advisories"
        setActiveTab={vi.fn()}
        readiness={mockReadiness}
        loadingReadiness={false}
      />
    )

    expect(screen.getByText(/ঋতুকেস্ট/)).toBeInTheDocument()
    expect(screen.getByText('Ritucast')).toBeInTheDocument()
    expect(screen.getByText('সচল (লাইভ)')).toBeInTheDocument()
  })

  it('handles tab switches', () => {
    const handleTabChange = vi.fn()
    render(
      <Header
        activeTab="advisories"
        setActiveTab={handleTabChange}
        readiness={mockReadiness}
        loadingReadiness={false}
      />
    )

    const weatherBtn = screen.getByRole('button', { name: /আবহাওয়া/ })
    fireEvent.click(weatherBtn)
    expect(handleTabChange).toHaveBeenCalledWith('weather')
  })
})
