import React, { useState, useEffect, useCallback } from 'react'
import { Header } from './components/Header'
import { ContextSelector } from './components/ContextSelector'
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

export const AppContent: React.FC = () => {
  const { language, t } = useLanguage()

  // Navigation State
  const [activeTab, setActiveTab] = useState<string>('advisories')

  // Metadata State
  const [upazilas, setUpazilas] = useState<UpazilaSummary[]>([])
  const [crops, setCrops] = useState<CropInfo[]>([])
  const [growthStages, setGrowthStages] = useState<string[]>([
    'Tillering',
    'Booting',
    'Flowering',
    'Dough',
    'Maturity',
  ])
  const [readiness, setReadiness] = useState<ReadinessResponse | null>(null)
  const [loadingReadiness, setLoadingReadiness] = useState<boolean>(true)

  // Selection Context (DEC-17 Gating)
  const [selectedUpazilaId, setSelectedUpazilaId] = useState<string>('BD-50-20-30')
  const [selectedCropId, setSelectedCropId] = useState<string>('boro_rice')
  const [selectedStage, setSelectedStage] = useState<string>('Tillering')

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

  // 1. Initial Metadata Load
  useEffect(() => {
    let mounted = true

    async function loadInitialMetadata() {
      try {
        setLoadingReadiness(true)
        const [upzList, cropList, readyRes] = await Promise.allSettled([
          apiClient.getUpazilas(),
          apiClient.getCrops(),
          apiClient.getReadiness(),
        ])

        if (!mounted) return

        if (upzList.status === 'fulfilled' && upzList.value.length > 0) {
          setUpazilas(upzList.value)
          setSelectedUpazilaId(upzList.value[0].upazila_id)
        }

        if (cropList.status === 'fulfilled' && cropList.value.length > 0) {
          setCrops(cropList.value)
          setSelectedCropId(cropList.value[0].crop_id)
          if (cropList.value[0].supported_stages?.length) {
            setGrowthStages(cropList.value[0].supported_stages)
            setSelectedStage(cropList.value[0].supported_stages[0])
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

  // 2. Fetch Active Analytical Data
  const fetchAnalyticalData = useCallback(async () => {
    if (!selectedUpazilaId || !selectedCropId || !selectedStage) return

    setLoadingData(true)
    setDataError(null)

    try {
      const [advRes, riskRes, wxRes, wbRes, fldRes, provRes] = await Promise.allSettled([
        apiClient.getAdvisories(selectedUpazilaId, selectedCropId, selectedStage),
        apiClient.evaluateRisk(selectedUpazilaId, selectedCropId, selectedStage),
        apiClient.getWeather(selectedUpazilaId),
        apiClient.getWaterBalance(selectedUpazilaId, selectedCropId, selectedStage),
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
  }, [selectedUpazilaId, selectedCropId, selectedStage, language])

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

      {/* Primary Context Selector (DEC-17 Gating) */}
      <ContextSelector
        upazilas={upazilas}
        selectedUpazilaId={selectedUpazilaId}
        setSelectedUpazilaId={setSelectedUpazilaId}
        crops={crops}
        selectedCropId={selectedCropId}
        setSelectedCropId={setSelectedCropId}
        growthStages={growthStages}
        selectedStage={selectedStage}
        setSelectedStage={setSelectedStage}
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
