import React, { useState, useEffect, useCallback, useMemo } from 'react'
import { Header } from './components/Header'
import { ContextSelector, getDefaultDateRange } from './components/ContextSelector'
import { AdvisoryHubView } from './components/AdvisoryHubView'
import { WeatherFeedView } from './components/WeatherFeedView'
import { WaterBalanceView } from './components/WaterBalanceView'
import { FloodHazardView } from './components/FloodHazardView'
import { ProvenanceView } from './components/ProvenanceView'
import { Footer } from './components/Footer'
import { apiClient } from './services/apiClient'
import { ThemeProvider } from './context/ThemeContext'
import { LanguageProvider, useLanguage } from './context/LanguageContext'
import type {
  UpazilaSummary,
  CropInfo,
  AdvisoryResponse,
  RiskEvaluationResponse,
  WeatherFeedResponse,
  WaterBalanceResponse,
  FloodHazardResponse,
  SystemProvenanceResponse,
  ReadinessResponse,
} from './types/api'

export interface ContextPreferences {
  division: string
  district: string
  upazilaId: string
  cropId: string
  stage: string
}

export const PREFS_STORAGE_KEY = 'ritucast_geo_context_prefs'

export const DEFAULT_CONTEXT_PREFS: ContextPreferences = {
  division: 'Rajshahi',
  district: 'Bogura',
  upazilaId: 'BD-50-10-06', // Adamdighi (আদমদিঘী)
  cropId: 'boro_rice', // Boro Rice (বোরো ধান)
  stage: 'Transplanting', // Transplanting
}

export function getStoredContextPrefs(): ContextPreferences {
  if (typeof window === 'undefined') return DEFAULT_CONTEXT_PREFS
  try {
    const raw = localStorage.getItem(PREFS_STORAGE_KEY)
    if (!raw) return DEFAULT_CONTEXT_PREFS
    const parsed = JSON.parse(raw)
    return {
      division: parsed.division || DEFAULT_CONTEXT_PREFS.division,
      district: parsed.district || DEFAULT_CONTEXT_PREFS.district,
      upazilaId: parsed.upazilaId || DEFAULT_CONTEXT_PREFS.upazilaId,
      cropId: parsed.cropId || DEFAULT_CONTEXT_PREFS.cropId,
      stage: parsed.stage || DEFAULT_CONTEXT_PREFS.stage,
    }
  } catch {
    return DEFAULT_CONTEXT_PREFS
  }
}

export function saveStoredContextPrefs(prefs: Partial<ContextPreferences>) {
  if (typeof window === 'undefined') return
  try {
    const current = getStoredContextPrefs()
    const updated = { ...current, ...prefs }
    localStorage.setItem(PREFS_STORAGE_KEY, JSON.stringify(updated))
  } catch {
    // ignore
  }
}

export const AppContent: React.FC = () => {
  const { language, t } = useLanguage()

  // Navigation State
  const [activeTab, setActiveTab] = useState<string>('advisories')

  // Metadata State
  const [upazilas, setUpazilas] = useState<UpazilaSummary[]>([])
  const [crops, setCrops] = useState<CropInfo[]>([])
  const [growthStages, setGrowthStages] = useState<string[]>([
    'Transplanting',
    'Tillering',
    'Panicle Initiation',
    'Booting',
    'Flowering',
    'Milking',
    'Dough',
    'Maturity',
  ])
  const [readiness, setReadiness] = useState<ReadinessResponse | null>(null)
  const [loadingReadiness, setLoadingReadiness] = useState<boolean>(true)

  // Selection Context (DEC-17 Gating) - Defaults to Rajshahi -> Bogura -> Adamdighi, Boro Rice, Transplanting
  const initialPrefs = useMemo(() => getStoredContextPrefs(), [])
  const [selectedDivision, setSelectedDivision] = useState<string>(initialPrefs.division)
  const [selectedDistrict, setSelectedDistrict] = useState<string>(initialPrefs.district)
  const [selectedUpazilaId, setSelectedUpazilaId] = useState<string>(initialPrefs.upazilaId)
  const [selectedCropId, setSelectedCropId] = useState<string>(initialPrefs.cropId)
  const [selectedStage, setSelectedStage] = useState<string>(initialPrefs.stage)

  // Custom Date Range State (defaults dynamically to previous 7 complete days, excluding today)
  const defaultDates = useMemo(() => getDefaultDateRange(), [])
  const [startDate, setStartDate] = useState<string>(defaultDates.startDate)
  const [endDate, setEndDate] = useState<string>(defaultDates.endDate)
  const [plantingDate, setPlantingDate] = useState<string>('')

  // Analytical Data States
  const [advisory, setAdvisory] = useState<AdvisoryResponse | null>(null)
  const [risk, setRisk] = useState<RiskEvaluationResponse | null>(null)
  const [weather, setWeather] = useState<WeatherFeedResponse | null>(null)
  const [waterBalance, setWaterBalance] = useState<WaterBalanceResponse | null>(null)
  const [floodHazard, setFloodHazard] = useState<FloodHazardResponse | null>(null)
  const [provenance, setProvenance] = useState<SystemProvenanceResponse | null>(null)

  // Loading & Error States
  const [loadingData, setLoadingData] = useState<boolean>(false)
  const [dataError, setDataError] = useState<string | null>(null)

  // Handlers for context updates with preference persistence
  const handleDivisionChange = (div: string) => {
    setSelectedDivision(div)
    saveStoredContextPrefs({ division: div })
  }

  const handleDistrictChange = (dist: string) => {
    setSelectedDistrict(dist)
    saveStoredContextPrefs({ district: dist })
  }

  const handleUpazilaChange = (upzId: string) => {
    setSelectedUpazilaId(upzId)
    const upz = upazilas.find((u) => u.upazila_id === upzId)
    if (upz) {
      setSelectedDivision(upz.division_name)
      setSelectedDistrict(upz.district_name)
      saveStoredContextPrefs({
        upazilaId: upzId,
        division: upz.division_name,
        district: upz.district_name,
      })
    } else {
      saveStoredContextPrefs({ upazilaId: upzId })
    }
  }

  const handleCropChange = (cropId: string) => {
    setSelectedCropId(cropId)
    const crop = crops.find((c) => c.crop_id === cropId)
    let nextStage = selectedStage
    if (crop && crop.supported_stages?.length) {
      setGrowthStages(crop.supported_stages)
      if (!crop.supported_stages.includes(selectedStage)) {
        nextStage = crop.supported_stages.includes(DEFAULT_CONTEXT_PREFS.stage)
          ? DEFAULT_CONTEXT_PREFS.stage
          : crop.supported_stages[0]
        setSelectedStage(nextStage)
      }
    }
    saveStoredContextPrefs({ cropId, stage: nextStage })
  }

  const handleStageChange = (stage: string) => {
    setSelectedStage(stage)
    saveStoredContextPrefs({ stage })
  }

  // 1. Initial Metadata Load: load full national upazila registry and crops catalog
  useEffect(() => {
    let mounted = true

    async function loadInitialMetadata() {
      try {
        setLoadingReadiness(true)
        const [upzList, cropList, readyRes] = await Promise.allSettled([
          apiClient.getUpazilas(true), // Request all 495 upazilas across Bangladesh
          apiClient.getCrops(),
          apiClient.getReadiness(),
        ])

        if (!mounted) return

        if (upzList.status === 'fulfilled' && upzList.value.length > 0) {
          setUpazilas(upzList.value)

          // Prioritize selected/stored upazila if found, then Adamdighi default, then pilot fallback (for mock test environments)
          const targetUpz =
            upzList.value.find((u) => u.upazila_id === selectedUpazilaId) ||
            upzList.value.find((u) => u.upazila_id === DEFAULT_CONTEXT_PREFS.upazilaId) ||
            upzList.value.find((u) => u.is_pilot) ||
            upzList.value[0]

          if (targetUpz) {
            setSelectedUpazilaId(targetUpz.upazila_id)
            setSelectedDivision(targetUpz.division_name)
            setSelectedDistrict(targetUpz.district_name)
          }
        }

        if (cropList.status === 'fulfilled' && cropList.value.length > 0) {
          setCrops(cropList.value)
          const targetCrop =
            cropList.value.find((c) => c.crop_id === selectedCropId) ||
            cropList.value.find((c) => c.crop_id === DEFAULT_CONTEXT_PREFS.cropId) ||
            cropList.value[0]

          setSelectedCropId(targetCrop.crop_id)
          if (targetCrop.supported_stages?.length) {
            setGrowthStages(targetCrop.supported_stages)
            const targetStage = targetCrop.supported_stages.includes(selectedStage)
              ? selectedStage
              : targetCrop.supported_stages.includes(DEFAULT_CONTEXT_PREFS.stage)
              ? DEFAULT_CONTEXT_PREFS.stage
              : targetCrop.supported_stages[0]
            setSelectedStage(targetStage)
          }
        }

        if (readyRes.status === 'fulfilled') {
          setReadiness(readyRes.value)
        }
      } catch (err: any) {
        console.error('Failed to load initial metadata', err)
      } finally {
        if (mounted) setLoadingReadiness(false)
      }
    }

    loadInitialMetadata()
    return () => {
      mounted = false
    }
  }, [])

  // 2. Fetch Active Analytical Data using Upazila, Crop, Stage, and Custom Date Range
  const fetchAnalyticalData = useCallback(async () => {
    if (!selectedUpazilaId || !selectedCropId || !selectedStage) return

    setLoadingData(true)
    setDataError(null)

    try {
      const [advRes, riskRes, wxRes, wbRes, fldRes, provRes] = await Promise.allSettled([
        apiClient.getAdvisories(selectedUpazilaId, selectedCropId, selectedStage, startDate, endDate),
        apiClient.evaluateRisk(selectedUpazilaId, selectedCropId, selectedStage),
        apiClient.getWeather(selectedUpazilaId, startDate, endDate),
        apiClient.getWaterBalance(selectedUpazilaId, selectedCropId, selectedStage, startDate, endDate),
        apiClient.getFloodHazard(selectedUpazilaId),
        apiClient.getProvenance(),
      ])

      if (advRes.status === 'fulfilled') setAdvisory(advRes.value)
      else console.warn('Advisory query failed', advRes.reason)

      if (riskRes.status === 'fulfilled') setRisk(riskRes.value)
      if (wxRes.status === 'fulfilled') setWeather(wxRes.value)
      if (wbRes.status === 'fulfilled') setWaterBalance(wbRes.value)
      if (fldRes.status === 'fulfilled') setFloodHazard(fldRes.value)
      if (provRes.status === 'fulfilled') setProvenance(provRes.value)

      if (advRes.status === 'rejected' && wxRes.status === 'rejected') {
        setDataError(
          language === 'en'
            ? 'Unable to retrieve data from server. Please verify backend connection.'
            : 'সার্ভার থেকে তথ্য পাওয়া যায়নি। অনুগ্রহ করে ব্যাকএন্ড সংযোগ পরীক্ষা করুন।'
        )
      }
    } catch (err: any) {
      setDataError(
        err.message ||
          (language === 'en' ? 'Failed to load agronomic data' : 'ডেটা লোড করতে ব্যর্থ হয়েছে')
      )
    } finally {
      setLoadingData(false)
    }
  }, [selectedUpazilaId, selectedCropId, selectedStage, startDate, endDate, language])

  // Trigger analysis when context changes
  useEffect(() => {
    fetchAnalyticalData()
  }, [fetchAnalyticalData])

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      {/* Skip to Main Content Link (WCAG 2.1 SC 2.4.1) */}
      <a href="#main-content" className="skip-to-content">
        {t('skip_to_content')}
      </a>

      {/* App Header */}
      <Header
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        readiness={readiness}
        loadingReadiness={loadingReadiness}
      />

      {/* Primary Context Selector (DEC-17 Gating, Cascading Geo, Expanded Crops, Custom Dates) */}
      <ContextSelector
        upazilas={upazilas}
        selectedDivision={selectedDivision}
        setSelectedDivision={handleDivisionChange}
        selectedDistrict={selectedDistrict}
        setSelectedDistrict={handleDistrictChange}
        selectedUpazilaId={selectedUpazilaId}
        setSelectedUpazilaId={handleUpazilaChange}
        crops={crops}
        selectedCropId={selectedCropId}
        setSelectedCropId={handleCropChange}
        growthStages={growthStages}
        selectedStage={selectedStage}
        setSelectedStage={handleStageChange}
        startDate={startDate}
        setStartDate={setStartDate}
        endDate={endDate}
        setEndDate={setEndDate}
        plantingDate={plantingDate}
        setPlantingDate={setPlantingDate}
        onRefresh={fetchAnalyticalData}
        loading={loadingData}
      />

      {/* Main Content Workspace */}
      <main
        id="main-content"
        className="app-container"
        tabIndex={-1}
        style={{ flex: 1, paddingBottom: 'var(--spacing-3xl)' }}
      >
        {activeTab === 'advisories' && (
          <AdvisoryHubView
            advisory={advisory}
            risk={risk}
            loading={loadingData}
            error={dataError}
          />
        )}

        {activeTab === 'weather' && (
          <WeatherFeedView
            weather={weather}
            loading={loadingData}
            error={dataError}
          />
        )}

        {activeTab === 'water-balance' && (
          <WaterBalanceView
            waterBalance={waterBalance}
            loading={loadingData}
            error={dataError}
          />
        )}

        {activeTab === 'flood' && (
          <FloodHazardView
            flood={floodHazard}
            loading={loadingData}
            error={dataError}
          />
        )}

        {activeTab === 'provenance' && (
          <ProvenanceView
            provenance={provenance}
            loading={loadingData}
            error={dataError}
          />
        )}
      </main>

      {/* Global Footer */}
      <Footer />
    </div>
  )
}

export const App: React.FC = () => {
  return (
    <ThemeProvider>
      <LanguageProvider>
        <AppContent />
      </LanguageProvider>
    </ThemeProvider>
  )
}

export default App
