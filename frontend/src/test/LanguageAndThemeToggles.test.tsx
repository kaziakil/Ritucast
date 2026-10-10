import { describe, it, expect, beforeEach, vi } from 'vitest'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import App from '../App'
import { Header } from '../components/Header'
import { LanguageProvider } from '../context/LanguageContext'
import { ThemeProvider } from '../context/ThemeContext'
import { apiClient } from '../services/apiClient'
import type { ReadinessResponse } from '../types/api'

const mockReadiness: ReadinessResponse = {
  status: 'ready',
  data_store_ready: true,
  analytics_ready: true,
  verified_datasets: ['nasa_power', 'bmd', 'sentinel_1'],
  missing_dependencies: [],
}

describe('Language & Theme Toggles Feature', () => {
  beforeEach(() => {
    localStorage.clear()
    document.documentElement.removeAttribute('data-theme')
    document.documentElement.removeAttribute('data-theme-mode')
    document.documentElement.removeAttribute('lang')
    vi.clearAllMocks()
  })

  describe('Language Toggle (Bangla & English)', () => {
    it('defaults to Bangla and persists choice in localStorage', () => {
      render(
        <ThemeProvider>
          <LanguageProvider>
            <Header
              activeTab="advisories"
              setActiveTab={vi.fn()}
              readiness={mockReadiness}
              loadingReadiness={false}
            />
          </LanguageProvider>
        </ThemeProvider>
      )

      // Default state: Bangla
      expect(document.documentElement.getAttribute('lang')).toBe('bn')
      expect(screen.getByText('পরামর্শ কেন্দ্র')).toBeInTheDocument()
      expect(screen.getByText('আবহাওয়া')).toBeInTheDocument()
      expect(screen.getByText('মাটির আর্দ্রতা (AWD)')).toBeInTheDocument()
      expect(screen.getByText('সচল (লাইভ)')).toBeInTheDocument()

      const bnButton = screen.getByRole('radio', { name: 'বাংলা' })
      const enButton = screen.getByRole('radio', { name: 'English' })
      expect(bnButton).toHaveAttribute('aria-checked', 'true')
      expect(enButton).toHaveAttribute('aria-checked', 'false')

      // Switch to English
      fireEvent.click(enButton)

      expect(document.documentElement.getAttribute('lang')).toBe('en')
      expect(localStorage.getItem('ritucast_lang')).toBe('en')
      expect(screen.getByText('Advisory Hub')).toBeInTheDocument()
      expect(screen.getByText('Weather Feed')).toBeInTheDocument()
      expect(screen.getByText('Soil Moisture (AWD)')).toBeInTheDocument()
      expect(screen.getByText('Haor Flood Hazard')).toBeInTheDocument()
      expect(screen.getByText('Transparency & Data')).toBeInTheDocument()
      expect(screen.getByText('Live (Active)')).toBeInTheDocument()
      expect(enButton).toHaveAttribute('aria-checked', 'true')
      expect(bnButton).toHaveAttribute('aria-checked', 'false')

      // Switch back to Bangla
      fireEvent.click(bnButton)
      expect(document.documentElement.getAttribute('lang')).toBe('bn')
      expect(localStorage.getItem('ritucast_lang')).toBe('bn')
      expect(screen.getByText('পরামর্শ কেন্দ্র')).toBeInTheDocument()
    })

    it('initializes from pre-existing localStorage language preference', () => {
      localStorage.setItem('ritucast_lang', 'en')

      render(
        <ThemeProvider>
          <LanguageProvider>
            <Header
              activeTab="advisories"
              setActiveTab={vi.fn()}
              readiness={mockReadiness}
              loadingReadiness={false}
            />
          </LanguageProvider>
        </ThemeProvider>
      )

      expect(document.documentElement.getAttribute('lang')).toBe('en')
      expect(screen.getByText('Advisory Hub')).toBeInTheDocument()
    })
  })

  describe('Theme Toggle (System, Light, Dark)', () => {
    it('defaults to System mode and applies data-theme attributes', () => {
      render(
        <ThemeProvider>
          <LanguageProvider>
            <Header
              activeTab="advisories"
              setActiveTab={vi.fn()}
              readiness={mockReadiness}
              loadingReadiness={false}
            />
          </LanguageProvider>
        </ThemeProvider>
      )

      // Initial mode is system
      expect(document.documentElement.getAttribute('data-theme-mode')).toBe('system')
      expect(['light', 'dark']).toContain(document.documentElement.getAttribute('data-theme'))

      const systemBtn = screen.getByRole('radio', { name: /সিস্টেম|System/i })
      const lightBtn = screen.getByRole('radio', { name: /লাইট|Light/i })
      const darkBtn = screen.getByRole('radio', { name: /ডার্ক|Dark/i })

      expect(systemBtn).toHaveAttribute('aria-checked', 'true')
      expect(lightBtn).toHaveAttribute('aria-checked', 'false')
      expect(darkBtn).toHaveAttribute('aria-checked', 'false')

      // Switch to Dark mode
      fireEvent.click(darkBtn)
      expect(localStorage.getItem('ritucast_theme')).toBe('dark')
      expect(document.documentElement.getAttribute('data-theme')).toBe('dark')
      expect(document.documentElement.getAttribute('data-theme-mode')).toBe('dark')
      expect(darkBtn).toHaveAttribute('aria-checked', 'true')
      expect(lightBtn).toHaveAttribute('aria-checked', 'false')
      expect(systemBtn).toHaveAttribute('aria-checked', 'false')

      // Switch to Light mode
      fireEvent.click(lightBtn)
      expect(localStorage.getItem('ritucast_theme')).toBe('light')
      expect(document.documentElement.getAttribute('data-theme')).toBe('light')
      expect(document.documentElement.getAttribute('data-theme-mode')).toBe('light')
      expect(lightBtn).toHaveAttribute('aria-checked', 'true')
      expect(darkBtn).toHaveAttribute('aria-checked', 'false')

      // Switch back to System mode
      fireEvent.click(systemBtn)
      expect(localStorage.getItem('ritucast_theme')).toBe('system')
      expect(document.documentElement.getAttribute('data-theme-mode')).toBe('system')
      expect(systemBtn).toHaveAttribute('aria-checked', 'true')
    })

    it('initializes from pre-existing localStorage theme preference', () => {
      localStorage.setItem('ritucast_theme', 'dark')

      render(
        <ThemeProvider>
          <LanguageProvider>
            <Header
              activeTab="advisories"
              setActiveTab={vi.fn()}
              readiness={mockReadiness}
              loadingReadiness={false}
            />
          </LanguageProvider>
        </ThemeProvider>
      )

      expect(document.documentElement.getAttribute('data-theme')).toBe('dark')
      expect(document.documentElement.getAttribute('data-theme-mode')).toBe('dark')
    })
  })

  describe('Full Application Integration', () => {
    it('switches whole application language seamlessly including ContextSelector and Footer', async () => {
      vi.spyOn(apiClient, 'getUpazilas').mockResolvedValue([
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
      ])
      vi.spyOn(apiClient, 'getCrops').mockResolvedValue([
        {
          crop_id: 'boro_rice',
          name_en: 'Boro Rice',
          name_bn: 'বোরো ধান',
          scientific_name: 'Oryza sativa L.',
          typical_duration_days: 145,
          supported_stages: ['Tillering', 'Booting'],
          calibration_status: 'CALIBRATED',
        },
      ])
      vi.spyOn(apiClient, 'getReadiness').mockResolvedValue(mockReadiness)

      render(<App />)

      // In Bangla default:
      expect(screen.getByText(/উপজেলা \(পাইলট অঞ্চল\):/)).toBeInTheDocument()
      expect(screen.getByText(/আবাদি ফসল|ফসল \(ক্যালিব্রেটেড\):/)).toBeInTheDocument()
      expect(screen.getByText(/বাংলাদেশ কৃষি আবহাওয়া প্ল্যাটফর্ম/)).toBeInTheDocument()

      // Switch to English:
      const enBtn = screen.getByRole('radio', { name: 'English' })
      fireEvent.click(enBtn)

      await waitFor(() => {
        expect(screen.getByText(/Upazila \(Pilot Region\):/)).toBeInTheDocument()
        expect(screen.getByText(/Active Crop \(Calibrated\):/)).toBeInTheDocument()
        expect(screen.getByText(/Crop Growth Stage \(DEC-17\):/)).toBeInTheDocument()
        expect(screen.getByText(/Refresh Analysis/)).toBeInTheDocument()
        expect(screen.getByText(/Current Agro-Zone:/)).toBeInTheDocument()
        expect(screen.getByText(/Bangladesh Agro-Meteorological Intelligence Platform/)).toBeInTheDocument()
      })
    })
  })
})
