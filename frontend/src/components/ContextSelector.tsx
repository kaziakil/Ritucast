import React, { useState, useMemo, useEffect, useRef } from 'react'
import {
  MapPin,
  Wheat,
  Calendar,
  RefreshCw,
  AlertCircle,
  Search,
  CheckCircle2,
  Clock,
  X,
  Sparkles,
} from 'lucide-react'
import type { UpazilaSummary, CropInfo } from '../types/api'
import { useLanguage } from '../context/LanguageContext'
import { STAGE_TRANSLATIONS } from '../i18n/translations'

export interface SearchLocationItem {
  id: string
  type: 'upazila' | 'district'
  nameEn: string
  nameBn: string
  divisionEn: string
  divisionBn?: string
  districtEn: string
  districtBn?: string
  upazilaId?: string
  isPilot?: boolean
  aezName?: string
}

export function getDefaultDateRange(): { startDate: string; endDate: string } {
  const now = new Date()
  const end = new Date(now)
  end.setDate(now.getDate() - 1) // yesterday: complete days only
  const start = new Date(now)
  start.setDate(now.getDate() - 7) // 7 full days prior

  const format = (d: Date) => {
    const y = d.getFullYear()
    const m = String(d.getMonth() + 1).padStart(2, '0')
    const day = String(d.getDate()).padStart(2, '0')
    return `${y}-${m}-${day}`
  }

  return {
    startDate: format(start),
    endDate: format(end),
  }
}

export interface ContextSelectorProps {
  upazilas: UpazilaSummary[]
  selectedUpazilaId: string
  setSelectedUpazilaId: (id: string) => void
  crops: CropInfo[]
  selectedCropId: string
  setSelectedCropId: (id: string) => void
  growthStages: string[]
  selectedStage: string
  setSelectedStage: (stage: string) => void
  startDate?: string
  setStartDate?: (date: string) => void
  endDate?: string
  setEndDate?: (date: string) => void
  plantingDate?: string
  setPlantingDate?: (date: string) => void
  onRefresh: () => void
  loading: boolean
}

export const ContextSelector: React.FC<ContextSelectorProps> = ({
  upazilas,
  selectedUpazilaId,
  setSelectedUpazilaId,
  crops,
  selectedCropId,
  setSelectedCropId,
  growthStages,
  selectedStage,
  setSelectedStage,
  startDate: propStartDate,
  setStartDate: propSetStartDate,
  endDate: propEndDate,
  setEndDate: propSetEndDate,
  plantingDate: propPlantingDate,
  setPlantingDate: propSetPlantingDate,
  onRefresh,
  loading,
}) => {
  const { language, t } = useLanguage()

  // Local fallback date state if parent doesn't provide setters
  const defaultDates = useMemo(() => getDefaultDateRange(), [])
  const [internalStartDate, setInternalStartDate] = useState<string>(defaultDates.startDate)
  const [internalEndDate, setInternalEndDate] = useState<string>(defaultDates.endDate)
  const [internalPlantingDate, setInternalPlantingDate] = useState<string>('')

  const activeStartDate = propStartDate !== undefined ? propStartDate : internalStartDate
  const activeEndDate = propEndDate !== undefined ? propEndDate : internalEndDate
  const activePlantingDate = propPlantingDate !== undefined ? propPlantingDate : internalPlantingDate

  const handleStartDateChange = (d: string) => {
    if (propSetStartDate) propSetStartDate(d)
    else setInternalStartDate(d)
  }

  const handleEndDateChange = (d: string) => {
    if (propSetEndDate) propSetEndDate(d)
    else setInternalEndDate(d)
  }

  const handlePlantingDateChange = (d: string) => {
    if (propSetPlantingDate) propSetPlantingDate(d)
    else setInternalPlantingDate(d)
  }

  // Active items lookup
  const currentUpazila = useMemo(
    () => upazilas.find((u) => u.upazila_id === selectedUpazilaId) || upazilas[0],
    [upazilas, selectedUpazilaId]
  )
  const currentCrop = useMemo(
    () => crops.find((c) => c.crop_id === selectedCropId) || crops[0],
    [crops, selectedCropId]
  )

  // Cascading Geography Hierarchy: Division -> District -> Upazila
  const [selectedDivision, setSelectedDivision] = useState<string>('')
  const [selectedDistrict, setSelectedDistrict] = useState<string>('')

  // Search State & Dropdown Management
  const [searchQuery, setSearchQuery] = useState<string>('')
  const [isSearchDropdownOpen, setIsSearchDropdownOpen] = useState<boolean>(false)
  const [highlightedIndex, setHighlightedIndex] = useState<number>(0)
  const searchContainerRef = useRef<HTMLDivElement>(null)

  // Click-outside listener to dismiss search dropdown
  useEffect(() => {
    const handleOutsideClick = (e: MouseEvent) => {
      if (searchContainerRef.current && !searchContainerRef.current.contains(e.target as Node)) {
        setIsSearchDropdownOpen(false)
      }
    }
    document.addEventListener('mousedown', handleOutsideClick)
    return () => {
      document.removeEventListener('mousedown', handleOutsideClick)
    }
  }, [])

  // Build searchable index of all 495 upazilas and 64 districts
  const searchableLocations = useMemo<SearchLocationItem[]>(() => {
    const list: SearchLocationItem[] = []
    const districtMap = new Map<string, { nameEn: string; nameBn: string; divisionEn: string; divisionBn?: string }>()

    upazilas.forEach((u) => {
      // 1. Index Upazila
      list.push({
        id: `upz-${u.upazila_id}`,
        type: 'upazila',
        nameEn: u.name_en,
        nameBn: u.name_bn,
        divisionEn: u.division_name,
        divisionBn: u.division_name_bn,
        districtEn: u.district_name,
        districtBn: u.district_name_bn,
        upazilaId: u.upazila_id,
        isPilot: u.is_pilot,
        aezName: u.aez_name,
      })

      // 2. Accumulate District
      if (u.district_name && !districtMap.has(u.district_name)) {
        districtMap.set(u.district_name, {
          nameEn: u.district_name,
          nameBn: u.district_name_bn || u.district_name,
          divisionEn: u.division_name,
          divisionBn: u.division_name_bn,
        })
      }
    })

    // 3. Index Districts
    districtMap.forEach((dist) => {
      list.push({
        id: `dist-${dist.nameEn}`,
        type: 'district',
        nameEn: dist.nameEn,
        nameBn: dist.nameBn,
        divisionEn: dist.divisionEn,
        divisionBn: dist.divisionBn,
        districtEn: dist.nameEn,
        districtBn: dist.nameBn,
      })
    })

    return list
  }, [upazilas])

  // Filter and score search results
  const searchResults = useMemo<SearchLocationItem[]>(() => {
    const q = searchQuery.trim()
    if (!q) return []
    const lower = q.toLowerCase()

    const scored = searchableLocations
      .map((item) => {
        let score = 0
        const nameEnLower = item.nameEn.toLowerCase()
        const distEnLower = item.districtEn.toLowerCase()
        const divEnLower = item.divisionEn.toLowerCase()

        // Direct Name Match
        if (nameEnLower === lower || item.nameBn === q) {
          score += 100
        } else if (nameEnLower.startsWith(lower) || item.nameBn.startsWith(q)) {
          score += 80
        } else if (nameEnLower.includes(lower) || item.nameBn.includes(q)) {
          score += 60
        } else if (distEnLower.includes(lower) || (item.districtBn && item.districtBn.includes(q))) {
          score += 40
        } else if (divEnLower.includes(lower) || (item.divisionBn && item.divisionBn.includes(q))) {
          score += 20
        }

        if (score > 0) {
          if (item.isPilot) score += 15
          if (item.type === 'district' && (nameEnLower.startsWith(lower) || item.nameBn.startsWith(q))) {
            score += 10
          }
        }

        return { item, score }
      })
      .filter((res) => res.score > 0)
      .sort((a, b) => b.score - a.score)
      .map((res) => res.item)

    return scored.slice(0, 10)
  }, [searchableLocations, searchQuery])

  // Handle Location Selection from Search Result
  const handleSelectLocation = (item: SearchLocationItem) => {
    if (item.type === 'upazila' && item.upazilaId) {
      setSelectedUpazilaId(item.upazilaId)
      setSelectedDivision(item.divisionEn)
      setSelectedDistrict(item.districtEn)
    } else if (item.type === 'district') {
      setSelectedDivision(item.divisionEn)
      setSelectedDistrict(item.nameEn)
      // Pick pilot upazila in this district or first available
      const targetUpz =
        upazilas.find((u) => u.district_name === item.nameEn && u.is_pilot) ||
        upazilas.find((u) => u.district_name === item.nameEn)
      if (targetUpz) {
        setSelectedUpazilaId(targetUpz.upazila_id)
      }
    }
    setSearchQuery('')
    setIsSearchDropdownOpen(false)
    setHighlightedIndex(0)
  }

  // Keyboard navigation within search input
  const handleSearchKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (!isSearchDropdownOpen && (e.key === 'ArrowDown' || e.key === 'ArrowUp')) {
      if (searchQuery.trim().length > 0) {
        setIsSearchDropdownOpen(true)
      }
      return
    }

    if (e.key === 'ArrowDown') {
      e.preventDefault()
      if (searchResults.length > 0) {
        setHighlightedIndex((prev) => (prev + 1) % searchResults.length)
      }
    } else if (e.key === 'ArrowUp') {
      e.preventDefault()
      if (searchResults.length > 0) {
        setHighlightedIndex((prev) => (prev <= 0 ? searchResults.length - 1 : prev - 1))
      }
    } else if (e.key === 'Enter') {
      e.preventDefault()
      if (searchResults.length > 0 && searchResults[highlightedIndex]) {
        handleSelectLocation(searchResults[highlightedIndex])
      }
    } else if (e.key === 'Escape') {
      e.preventDefault()
      setIsSearchDropdownOpen(false)
    }
  }

  // Extract unique divisions from upazilas list
  const availableDivisions = useMemo(() => {
    const set = new Set<string>()
    upazilas.forEach((u) => {
      if (u.division_name) set.add(u.division_name)
    })
    return Array.from(set).sort()
  }, [upazilas])

  // Extract districts belonging to the selected division
  const availableDistricts = useMemo(() => {
    const set = new Set<string>()
    upazilas.forEach((u) => {
      if (!selectedDivision || u.division_name === selectedDivision) {
        if (u.district_name) set.add(u.district_name)
      }
    })
    return Array.from(set).sort()
  }, [upazilas, selectedDivision])

  // Extract upazilas belonging to current division and district
  const filteredUpazilas = useMemo(() => {
    if (!selectedDivision && !selectedDistrict) {
      return upazilas
    }

    return upazilas.filter((u) => {
      const matchesDiv = !selectedDivision || u.division_name === selectedDivision
      const matchesDist = !selectedDistrict || u.district_name === selectedDistrict
      return matchesDiv && matchesDist
    })
  }, [upazilas, selectedDivision, selectedDistrict])

  // Ensure currentUpazila is always available in the options
  const displayUpazilas = useMemo(() => {
    if (currentUpazila && !filteredUpazilas.some((u) => u.upazila_id === currentUpazila.upazila_id)) {
      return [currentUpazila, ...filteredUpazilas]
    }
    return filteredUpazilas
  }, [filteredUpazilas, currentUpazila])

  // Handle Division Selection
  const onDivisionChange = (divName: string) => {
    setSelectedDivision(divName)
    const firstDist = upazilas.find((u) => u.division_name === divName)?.district_name || ''
    setSelectedDistrict(firstDist)
    const firstUpz = upazilas.find((u) => u.division_name === divName && u.district_name === firstDist)
    if (firstUpz) setSelectedUpazilaId(firstUpz.upazila_id)
  }

  // Handle District Selection
  const onDistrictChange = (distName: string) => {
    setSelectedDistrict(distName)
    const firstUpz = upazilas.find(
      (u) => (!selectedDivision || u.division_name === selectedDivision) && u.district_name === distName
    )
    if (firstUpz) setSelectedUpazilaId(firstUpz.upazila_id)
  }

  // Crops grouped by Category
  const groupedCrops = useMemo(() => {
    const groups: Record<string, CropInfo[]> = {}
    crops.forEach((c) => {
      const catKey = c.category_bn || c.category_en || c.category || 'General'
      if (!groups[catKey]) groups[catKey] = []
      groups[catKey].push(c)
    })
    return groups
  }, [crops])

  // Adaptive Growth Stage Derivation from Planting Date
  const [stageDerivedNotice, setStageDerivedNotice] = useState<string | null>(null)

  useEffect(() => {
    if (!activePlantingDate || !currentCrop) {
      setStageDerivedNotice(null)
      return
    }

    try {
      const pDate = new Date(activePlantingDate)
      const refDate = activeEndDate ? new Date(activeEndDate) : new Date()
      const diffMs = refDate.getTime() - pDate.getTime()
      const daysElapsed = Math.floor(diffMs / (1000 * 60 * 60 * 24))

      if (daysElapsed >= 0 && currentCrop.typical_duration_days > 0) {
        const ratio = daysElapsed / currentCrop.typical_duration_days
        const stages = growthStages.length > 0 ? growthStages : currentCrop.supported_stages
        if (stages && stages.length > 0) {
          const index = Math.min(Math.floor(ratio * stages.length), stages.length - 1)
          const estimatedStage = stages[index]
          if (estimatedStage && estimatedStage !== selectedStage) {
            setSelectedStage(estimatedStage)
          }
          setStageDerivedNotice(
            language === 'en'
              ? `Estimated: Day ${daysElapsed} of ${currentCrop.typical_duration_days} days (${Math.round(ratio * 100)}%)`
              : `রোপণের ${daysElapsed}তম দিন (মোট ${currentCrop.typical_duration_days} দিনের ${Math.round(ratio * 100)}%)`
          )
        }
      } else {
        setStageDerivedNotice(null)
      }
    } catch {
      setStageDerivedNotice(null)
    }
  }, [activePlantingDate, activeEndDate, currentCrop, growthStages, language, selectedStage, setSelectedStage])

  // Date Range Presets
  const applyDatePreset = (days: number) => {
    const now = new Date()
    const end = new Date(now)
    end.setDate(now.getDate() - 1)
    const start = new Date(now)
    start.setDate(now.getDate() - days)

    const format = (d: Date) => {
      const y = d.getFullYear()
      const m = String(d.getMonth() + 1).padStart(2, '0')
      const day = String(d.getDate()).padStart(2, '0')
      return `${y}-${m}-${day}`
    }

    handleStartDateChange(format(start))
    handleEndDateChange(format(end))
  }

  // Date Range Validation
  const dateValidationError = useMemo(() => {
    if (!activeStartDate || !activeEndDate) return null
    if (activeStartDate > activeEndDate) {
      return t('date_err_start_after_end')
    }

    const todayStr = new Date().toISOString().slice(0, 10)
    if (activeEndDate >= todayStr) {
      return t('date_err_future')
    }

    return null
  }, [activeStartDate, activeEndDate, t])

  const stagesMap = STAGE_TRANSLATIONS[language] || STAGE_TRANSLATIONS.bn

  return (
    <section aria-label={t('context_section_label')} className="context-section">
      <div className="app-container">
        {/* TOP ROW: Quick Search & Active Context Meta Group */}
        <div className="context-top-bar">
          {/* Quick Search across all 64 districts & 495 upazilas */}
          <div className="context-search-container" ref={searchContainerRef}>
            <div className="context-search-input-box">
              <Search size={16} className="context-search-icon" aria-hidden="true" />
              <input
                type="text"
                role="combobox"
                aria-expanded={isSearchDropdownOpen}
                aria-haspopup="listbox"
                aria-autocomplete="list"
                aria-controls="location-search-listbox"
                className="context-search-input"
                placeholder={t('search_placeholder')}
                value={searchQuery}
                onFocus={() => {
                  if (searchQuery.trim().length > 0) setIsSearchDropdownOpen(true)
                }}
                onChange={(e) => {
                  setSearchQuery(e.target.value)
                  setIsSearchDropdownOpen(e.target.value.trim().length > 0)
                  setHighlightedIndex(0)
                }}
                onKeyDown={handleSearchKeyDown}
                aria-label={language === 'en' ? 'Search locations' : 'অবস্থান অনুসন্ধান'}
              />
              {searchQuery && (
                <button
                  type="button"
                  onClick={() => {
                    setSearchQuery('')
                    setIsSearchDropdownOpen(false)
                  }}
                  className="context-search-clear"
                  aria-label={t('clear_search')}
                >
                  <X size={14} />
                </button>
              )}

              {/* Floating Autocomplete Dropdown List */}
              {isSearchDropdownOpen && searchQuery.trim().length > 0 && (
                <div
                  id="location-search-listbox"
                  role="listbox"
                  className="search-autocomplete-dropdown"
                >
                  {searchResults.length > 0 ? (
                    searchResults.map((item, idx) => (
                      <div
                        key={item.id}
                        role="option"
                        id={`search-item-${item.id}`}
                        aria-selected={idx === highlightedIndex}
                        className={`search-result-item ${idx === highlightedIndex ? 'highlighted' : ''}`}
                        onClick={() => handleSelectLocation(item)}
                        onMouseEnter={() => setHighlightedIndex(idx)}
                      >
                        <div className="search-result-primary">
                          <span className="search-result-name">
                            {language === 'en' ? item.nameEn : item.nameBn}{' '}
                            <span className="search-result-subname" style={{ fontWeight: 400, opacity: 0.85, fontSize: '0.9em' }}>
                              ({language === 'en' ? item.nameBn : item.nameEn})
                            </span>
                          </span>
                          {item.type === 'upazila' ? (
                            <span className="search-type-badge upazila">
                              {t('search_type_upazila')}
                            </span>
                          ) : (
                            <span className="search-type-badge district">
                              {t('search_type_district')}
                            </span>
                          )}
                          {item.isPilot && (
                            <span className="search-pilot-badge">
                              ★ {t('pilot_badge')}
                            </span>
                          )}
                        </div>
                        <div className="search-result-secondary">
                          {item.type === 'upazila' ? (
                            <span>
                              {language === 'en'
                                ? `${item.districtEn}, ${item.divisionEn}`
                                : `${item.districtBn || item.districtEn}, ${item.divisionBn || item.divisionEn}`}
                            </span>
                          ) : (
                            <span>
                              {language === 'en'
                                ? `Division: ${item.divisionEn}`
                                : `বিভাগ: ${item.divisionBn || item.divisionEn}`}
                            </span>
                          )}
                        </div>
                      </div>
                    ))
                  ) : (
                    <div className="search-no-results">
                      {t('search_no_results')}
                    </div>
                  )}
                  <div className="search-dropdown-footer">
                    <span>{t('search_hint')}</span>
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Active Context Meta & Coverage Badges */}
          <div className="context-meta-group">
            <span className="context-badge-scope">
              <CheckCircle2 size={12} />
              {t('national_badge')} (64 {t('district_label').replace(':', '')} / 495 {t('upazila_count_suffix')})
            </span>

            {currentUpazila?.is_pilot && (
              <span className="context-badge-pilot">
                ★ {t('pilot_badge')}
              </span>
            )}
          </div>
        </div>

        {/* PRIMARY CONTROLS GRID */}
        <div className="context-controls-grid">
          {/* 1. DIVISION SELECTOR */}
          <div className="form-group" style={{ marginBottom: 0 }}>
            <label className="form-label" htmlFor="division-select">
              <MapPin size={14} style={{ display: 'inline', marginRight: 4, verticalAlign: 'middle' }} />
              {t('division_label')}
            </label>
            <select
              id="division-select"
              className="form-select"
              value={selectedDivision}
              onChange={(e) => onDivisionChange(e.target.value)}
            >
              <option value="">{t('all_divisions')}</option>
              {availableDivisions.map((div) => (
                <option key={div} value={div}>
                  {div}
                </option>
              ))}
            </select>
          </div>

          {/* 2. DISTRICT SELECTOR */}
          <div className="form-group" style={{ marginBottom: 0 }}>
            <label className="form-label" htmlFor="district-select">
              <MapPin size={14} style={{ display: 'inline', marginRight: 4, verticalAlign: 'middle' }} />
              {t('district_label')}
            </label>
            <select
              id="district-select"
              className="form-select"
              value={selectedDistrict}
              onChange={(e) => onDistrictChange(e.target.value)}
            >
              <option value="">{t('select_district')}</option>
              {availableDistricts.map((dist) => (
                <option key={dist} value={dist}>
                  {dist}
                </option>
              ))}
            </select>
          </div>

          {/* 3. UPAZILA SELECTOR (Primary Tested Combobox) */}
          <div className="form-group" style={{ marginBottom: 0 }}>
            <label className="form-label" htmlFor="upazila-select">
              <MapPin size={14} style={{ display: 'inline', marginRight: 4, verticalAlign: 'middle' }} />
              {t('upazila_label')}
            </label>
            <select
              id="upazila-select"
              className="form-select"
              value={selectedUpazilaId}
              onChange={(e) => {
                setSelectedUpazilaId(e.target.value)
                const upz = upazilas.find((u) => u.upazila_id === e.target.value)
                if (upz) {
                  setSelectedDivision(upz.division_name)
                  setSelectedDistrict(upz.district_name)
                }
              }}
            >
              {displayUpazilas.length === 0 ? (
                <option value="" disabled>
                  {t('select_upazila')}
                </option>
              ) : (
                displayUpazilas.map((u) => {
                  const pilotMark = u.is_pilot ? '★ ' : ''
                  return (
                    <option key={u.upazila_id} value={u.upazila_id}>
                      {language === 'en'
                        ? `${pilotMark}${u.name_en} (${u.name_bn}) — ${u.district_name}`
                        : `${pilotMark}${u.name_bn} (${u.name_en}) — ${u.district_name_bn || u.district_name}`}
                    </option>
                  )
                })
              )}
            </select>
          </div>

          {/* 4. EXPANDED CROP SELECTOR (Grouped by Category) */}
          <div className="form-group" style={{ marginBottom: 0 }}>
            <label className="form-label" htmlFor="crop-select">
              <Wheat size={14} style={{ display: 'inline', marginRight: 4, verticalAlign: 'middle' }} />
              {t('crop_label')}
            </label>
            <select
              id="crop-select"
              className="form-select"
              value={selectedCropId}
              onChange={(e) => setSelectedCropId(e.target.value)}
            >
              {Object.entries(groupedCrops).map(([categoryName, cropList]) => (
                <optgroup key={categoryName} label={categoryName}>
                  {cropList.map((c) => {
                    const isCalibrated =
                      c.calibration_status === 'FULL_CALIBRATION' || c.calibration_status === 'PILOT_CALIBRATED'
                    const calTag = isCalibrated ? '●' : '○'
                    return (
                      <option key={c.crop_id} value={c.crop_id}>
                        {language === 'en'
                          ? `${calTag} ${c.name_en} (${c.name_bn})`
                          : `${calTag} ${c.name_bn} (${c.name_en})`}
                      </option>
                    )
                  })}
                </optgroup>
              ))}
            </select>
          </div>

          {/* 5. PHENOLOGICAL STAGE SELECTOR */}
          <div className="form-group" style={{ marginBottom: 0 }}>
            <label className="form-label" htmlFor="stage-select">
              <Calendar size={14} style={{ display: 'inline', marginRight: 4, verticalAlign: 'middle' }} />
              {t('stage_label')}
            </label>
            <select
              id="stage-select"
              className="form-select"
              value={selectedStage}
              onChange={(e) => {
                setSelectedStage(e.target.value)
                setStageDerivedNotice(null)
              }}
            >
              {growthStages.map((stage) => (
                <option key={stage} value={stage}>
                  {stagesMap[stage] || stage}
                </option>
              ))}
            </select>
          </div>

          {/* REFRESH / ANALYZE BUTTON */}
          <div className="context-refresh-action" style={{ marginBottom: 0 }}>
            <button
              className="btn btn-primary context-refresh-btn"
              onClick={onRefresh}
              disabled={loading || !!dateValidationError}
              aria-busy={loading}
              aria-label={t('refresh_aria_label')}
            >
              <RefreshCw size={16} className={loading ? 'animate-spin' : ''} />
              <span>{loading ? t('refresh_loading') : t('refresh_btn')}</span>
            </button>
          </div>
        </div>

        {/* SECOND ROW: CUSTOM DATE RANGE CONTROLS & PLANTING DATE */}
        <div className="context-temporal-card">
          <div className="context-temporal-grid">
            {/* Start Date */}
            <div className="form-group" style={{ marginBottom: 0 }}>
              <label className="form-label" htmlFor="start-date-input" style={{ fontSize: 'var(--font-size-caption)' }}>
                <Clock size={12} style={{ display: 'inline', marginRight: 4, verticalAlign: 'middle' }} />
                {t('start_date_label')}
              </label>
              <input
                id="start-date-input"
                type="date"
                className="form-input"
                value={activeStartDate}
                onChange={(e) => handleStartDateChange(e.target.value)}
                style={{ height: '36px', fontSize: 'var(--font-size-body-sm)' }}
              />
            </div>

            {/* End Date */}
            <div className="form-group" style={{ marginBottom: 0 }}>
              <label className="form-label" htmlFor="end-date-input" style={{ fontSize: 'var(--font-size-caption)' }}>
                <Clock size={12} style={{ display: 'inline', marginRight: 4, verticalAlign: 'middle' }} />
                {t('end_date_label')}
              </label>
              <input
                id="end-date-input"
                type="date"
                className="form-input"
                value={activeEndDate}
                onChange={(e) => handleEndDateChange(e.target.value)}
                style={{ height: '36px', fontSize: 'var(--font-size-body-sm)' }}
              />
            </div>

            {/* Date Presets Buttons */}
            <div className="form-group" style={{ marginBottom: 0 }}>
              <span className="form-label" style={{ fontSize: 'var(--font-size-caption)' }}>
                <Clock size={12} style={{ display: 'inline', marginRight: 4, verticalAlign: 'middle' }} />
                {t('date_range_label')}
              </span>
              <div className="context-preset-container">
                <button
                  type="button"
                  className="context-preset-chip"
                  onClick={() => applyDatePreset(7)}
                >
                  {t('date_preset_7d')}
                </button>
                <button
                  type="button"
                  className="context-preset-chip"
                  onClick={() => applyDatePreset(14)}
                >
                  {t('date_preset_14d')}
                </button>
                <button
                  type="button"
                  className="context-preset-chip"
                  onClick={() => applyDatePreset(30)}
                >
                  {t('date_preset_30d')}
                </button>
              </div>
            </div>

            {/* Optional Planting Date */}
            <div className="form-group" style={{ marginBottom: 0 }}>
              <label className="form-label" htmlFor="planting-date-input" style={{ fontSize: 'var(--font-size-caption)' }}>
                <Sparkles size={12} style={{ display: 'inline', marginRight: 4, verticalAlign: 'middle' }} />
                {t('planting_date_label')}
              </label>
              <input
                id="planting-date-input"
                type="date"
                className="form-input"
                value={activePlantingDate}
                onChange={(e) => handlePlantingDateChange(e.target.value)}
                style={{ height: '36px', fontSize: 'var(--font-size-body-sm)' }}
                placeholder={t('planting_date_hint')}
              />
            </div>
          </div>
        </div>

        {/* DATE VALIDATION OR LATENCY NOTICE */}
        {dateValidationError ? (
          <div
            role="alert"
            style={{
              marginTop: 'var(--spacing-sm)',
              padding: '6px 12px',
              backgroundColor: 'var(--primitive-rose-100)',
              color: 'var(--primitive-rose-900)',
              borderRadius: 'var(--radius-sm)',
              fontSize: 'var(--font-size-caption)',
              display: 'flex',
              alignItems: 'center',
              gap: 6,
              fontWeight: 500,
            }}
          >
            <AlertCircle size={14} />
            <span>{dateValidationError}</span>
          </div>
        ) : (
          <div
            style={{
              marginTop: 'var(--spacing-xs)',
              fontSize: '11px',
              color: 'var(--color-text-muted)',
              display: 'flex',
              alignItems: 'center',
              gap: 6,
            }}
          >
            <Clock size={12} />
            <span>{t('date_latency_notice')}</span>
            {stageDerivedNotice && (
              <span
                style={{
                  marginLeft: 'auto',
                  backgroundColor: 'var(--primitive-teal-100)',
                  color: 'var(--primitive-teal-900)',
                  padding: '2px 6px',
                  borderRadius: 'var(--radius-sm)',
                  fontWeight: 600,
                }}
              >
                {stageDerivedNotice}
              </span>
            )}
          </div>
        )}

        {/* BOTTOM METADATA BAR: Selected Zone, Risk Domain & Calibration */}
        <div
          aria-live="polite"
          style={{
            marginTop: 'var(--spacing-md)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            flexWrap: 'wrap',
            gap: 'var(--spacing-sm)',
            fontSize: 'var(--font-size-caption)',
            color: 'var(--color-text-secondary)',
            borderTop: '1px solid var(--color-border-subtle)',
            paddingTop: 'var(--spacing-sm)',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--spacing-sm)', flexWrap: 'wrap' }}>
            <span style={{ fontWeight: 600 }}>{t('current_zone')}</span>
            <span
              style={{
                backgroundColor:
                  currentUpazila?.aez_code === 26 ? 'var(--primitive-amber-100)' : 'var(--primitive-sky-100)',
                color:
                  currentUpazila?.aez_code === 26 ? 'var(--primitive-amber-900)' : 'var(--primitive-sky-900)',
                padding: '2px 8px',
                borderRadius: 'var(--radius-sm)',
                fontWeight: 600,
              }}
            >
              {currentUpazila?.aez_name} (AEZ-{currentUpazila?.aez_code})
            </span>
            <span>
              • {t('primary_risk_label')}{' '}
              <strong>
                {currentUpazila?.primary_risk === 'FLASH_FLOOD'
                  ? t('primary_risk_flood')
                  : t('primary_risk_drought')}
              </strong>
            </span>
            {currentCrop && (
              <span>
                •{' '}
                <strong style={{ color: 'var(--color-brand-primary)' }}>
                  {language === 'en' ? currentCrop.name_en : currentCrop.name_bn}
                </strong>{' '}
                ({currentCrop.calibration_status === 'FULL_CALIBRATION' || currentCrop.calibration_status === 'PILOT_CALIBRATED'
                  ? t('crop_calibrated_badge')
                  : t('crop_regional_badge')}
                )
              </span>
            )}
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: 4, color: 'var(--color-brand-primary)' }}>
            <AlertCircle size={14} />
            <span>{t('gating_verified')}</span>
          </div>
        </div>
      </div>
    </section>
  )
}

export default ContextSelector
