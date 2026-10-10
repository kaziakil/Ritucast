import { describe, it, expect, vi, beforeEach } from 'vitest'
import { apiClient } from '../services/apiClient'
import type { UpazilaSummary } from '../types/api'

describe('apiClient', () => {
  beforeEach(() => {
    vi.restoreAllMocks()
  })

  it('fetches metadata upazilas successfully', async () => {
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

    globalThis.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({
        status: 'success',
        count: 1,
        data: mockUpazilas,
      }),
    } as Response)

    const result = await apiClient.getUpazilas()
    expect(result).toEqual(mockUpazilas)
    expect(globalThis.fetch).toHaveBeenCalledWith('/api/v1/upazilas', expect.any(Object))
  })

  it('handles API errors properly', async () => {
    globalThis.fetch = vi.fn().mockResolvedValue({
      ok: false,
      status: 404,
      statusText: 'Not Found',
      json: async () => ({ detail: 'Upazila not found' }),
    } as Response)

    await expect(apiClient.getUpazilaDetail('unknown')).rejects.toThrow('Upazila not found')
  })

  it('fetches health check successfully', async () => {
    const mockHealth = {
      status: 'healthy',
      version: '0.1.0',
      timestamp_utc: '2026-10-10T12:00:00Z',
    }

    globalThis.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => mockHealth,
    } as Response)

    const result = await apiClient.getHealth()
    expect(result).toEqual(mockHealth)
    expect(globalThis.fetch).toHaveBeenCalledWith('/health', expect.any(Object))
  })
})
