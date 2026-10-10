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

    expect(screen.getByText(/ঋতুকাস্ট/)).toBeInTheDocument()
    expect(screen.getByText('Ritucast')).toBeInTheDocument()
    expect(screen.getByText('সচল (লাইভ)')).toBeInTheDocument()
  })

  it('handles desktop tab switches', () => {
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

  it('toggles mobile navigation drawer and handles mobile item selection', () => {
    const handleTabChange = vi.fn()
    render(
      <Header
        activeTab="advisories"
        setActiveTab={handleTabChange}
        readiness={mockReadiness}
        loadingReadiness={false}
      />
    )

    // Mobile menu button should be present with accessible label
    const menuToggle = screen.getByRole('button', { name: /মেনু খুলুন/i })
    expect(menuToggle).toHaveAttribute('aria-expanded', 'false')

    // Open mobile menu
    fireEvent.click(menuToggle)
    expect(menuToggle).toHaveAttribute('aria-expanded', 'true')
    expect(screen.getByRole('region', { name: /Mobile Navigation/i })).toBeInTheDocument()

    // Find and click mobile link
    const mobileLinks = screen.getAllByRole('button', { name: /হাওড় বন্যা ঝুঁকি/i })
    expect(mobileLinks.length).toBeGreaterThanOrEqual(1)
    fireEvent.click(mobileLinks[mobileLinks.length - 1])

    expect(handleTabChange).toHaveBeenCalledWith('flood')
    expect(screen.queryByRole('region', { name: /Mobile Navigation/i })).not.toBeInTheDocument()
  })

  it('closes mobile menu on Escape key press', () => {
    render(
      <Header
        activeTab="advisories"
        setActiveTab={vi.fn()}
        readiness={mockReadiness}
        loadingReadiness={false}
      />
    )

    const menuToggle = screen.getByRole('button', { name: /মেনু খুলুন/i })
    fireEvent.click(menuToggle)
    expect(screen.getByRole('region', { name: /Mobile Navigation/i })).toBeInTheDocument()

    // Press Escape
    fireEvent.keyDown(window, { key: 'Escape' })
    expect(screen.queryByRole('region', { name: /Mobile Navigation/i })).not.toBeInTheDocument()
  })
})
