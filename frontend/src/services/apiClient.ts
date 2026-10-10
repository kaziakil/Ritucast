import type {
  UpazilaSummary,
  UpazilaDetail,
  CropInfo,
  SeasonInfo,
  WeatherFeedResponse,
  WaterBalanceResponse,
  FloodHazardResponse,
  AdvisoryResponse,
  RiskEvaluationResponse,
  SystemProvenanceResponse,
  HealthResponse,
  ReadinessResponse,
} from '../types/api'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || ''

class ApiError extends Error {
  code: string
  status: number

  constructor(message: string, code: string = 'UNKNOWN_ERROR', status: number = 500) {
    super(message)
    this.name = 'ApiError'
    this.code = code
    this.status = status
  }
}

async function request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`
  const headers = {
    'Content-Type': 'application/json',
    Accept: 'application/json',
    ...options.headers,
  }

  try {
    const res = await fetch(url, { ...options, headers })
    if (!res.ok) {
      let errPayload: any = {}
      try {
        errPayload = await res.json()
      } catch {
        // non-json error
      }
      const message = errPayload.detail || errPayload.message || `HTTP error ${res.status}: ${res.statusText}`
      const code = errPayload.code || `HTTP_${res.status}`
      throw new ApiError(message, code, res.status)
    }
    return (await res.json()) as T
  } catch (err: any) {
    if (err instanceof ApiError) {
      throw err
    }
    throw new ApiError(
      err.message || 'নেটওয়ার্ক সংযোগে সমস্যা হয়েছে। দয়া করে পুনরায় চেষ্টা করুন।',
      'NETWORK_FAILURE',
      0
    )
  }
}

export const apiClient = {
  getHealth: async (): Promise<HealthResponse> => {
    return request<HealthResponse>('/health')
  },

  getReadiness: async (): Promise<ReadinessResponse> => {
    return request<ReadinessResponse>('/ready')
  },

  getUpazilas: async (all: boolean = false): Promise<UpazilaSummary[]> => {
    const endpoint = all ? '/api/v1/upazilas?all=true' : '/api/v1/upazilas'
    const res = await request<{ status: string; count: number; data: UpazilaSummary[] }>(endpoint)
    return res.data
  },

  getGeoHierarchy: async (): Promise<any> => {
    const res = await request<{ status: string; data: any }>('/api/v1/geo/hierarchy')
    return res.data
  },

  getDivisions: async (): Promise<any[]> => {
    const res = await request<{ status: string; count: number; data: any[] }>('/api/v1/geo/divisions')
    return res.data
  },

  getDistricts: async (divisionId?: string): Promise<any[]> => {
    const url = divisionId ? `/api/v1/geo/districts?division_id=${divisionId}` : '/api/v1/geo/districts'
    const res = await request<{ status: string; count: number; data: any[] }>(url)
    return res.data
  },

  getUpazilaDetail: async (upazilaId: string): Promise<UpazilaDetail> => {
    const res = await request<{ status: string; data: UpazilaDetail }>(`/api/v1/upazilas/${upazilaId}`)
    return res.data
  },

  getCrops: async (): Promise<CropInfo[]> => {
    const res = await request<{ status: string; count: number; data: CropInfo[] }>('/api/v1/crops')
    return res.data
  },

  getSeasons: async (): Promise<SeasonInfo[]> => {
    const res = await request<{ status: string; count: number; data: SeasonInfo[] }>('/api/v1/seasons')
    return res.data
  },

  getWeather: async (upazilaId: string, startDate?: string, endDate?: string): Promise<WeatherFeedResponse> => {
    const params = new URLSearchParams()
    if (startDate) params.append('start_date', startDate)
    if (endDate) params.append('end_date', endDate)
    const qs = params.toString() ? `?${params.toString()}` : ''
    return request<WeatherFeedResponse>(`/api/v1/upazilas/${upazilaId}/weather${qs}`)
  },

  getWaterBalance: async (
    upazilaId: string,
    crop: string,
    stage: string,
    startDate?: string,
    endDate?: string
  ): Promise<WaterBalanceResponse> => {
    const params = new URLSearchParams({ crop, stage })
    if (startDate) params.append('start_date', startDate)
    if (endDate) params.append('end_date', endDate)
    return request<WaterBalanceResponse>(`/api/v1/upazilas/${upazilaId}/water-balance?${params.toString()}`)
  },

  getFloodHazard: async (upazilaId: string): Promise<FloodHazardResponse> => {
    return request<FloodHazardResponse>(`/api/v1/upazilas/${upazilaId}/flood-hazard`)
  },

  getAdvisories: async (
    upazilaId: string,
    crop: string,
    stage: string,
    startDate?: string,
    endDate?: string
  ): Promise<AdvisoryResponse> => {
    const params = new URLSearchParams({ crop, stage })
    if (startDate) params.append('start_date', startDate)
    if (endDate) params.append('end_date', endDate)
    return request<AdvisoryResponse>(`/api/v1/upazilas/${upazilaId}/advisories?${params.toString()}`)
  },

  evaluateRisk: async (
    upazilaId: string,
    cropId: string,
    growthStage: string,
    hazardTypes?: string[]
  ): Promise<RiskEvaluationResponse> => {
    return request<RiskEvaluationResponse>('/api/v1/risk/evaluate', {
      method: 'POST',
      body: JSON.stringify({
        upazila_id: upazilaId,
        crop_id: cropId,
        growth_stage: growthStage,
        hazard_types: hazardTypes,
      }),
    })
  },

  getProvenance: async (): Promise<SystemProvenanceResponse> => {
    return request<SystemProvenanceResponse>('/api/v1/provenance')
  },
}
