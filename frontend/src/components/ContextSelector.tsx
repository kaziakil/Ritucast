import React from 'react'
import { MapPin, Wheat, Calendar, RefreshCw, AlertCircle } from 'lucide-react'
import type { UpazilaSummary, CropInfo } from '../types/api'
import { useLanguage } from '../context/LanguageContext'
import { STAGE_TRANSLATIONS } from '../i18n/translations'

interface ContextSelectorProps {
  upazilas: UpazilaSummary[]
  selectedUpazilaId: string
  setSelectedUpazilaId: (id: string) => void
  crops: CropInfo[]
  selectedCropId: string
  setSelectedCropId: (id: string) => void
  growthStages: string[]
  selectedStage: string
  setSelectedStage: (stage: string) => void
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
  onRefresh,
  loading,
}) => {
  const { language, t } = useLanguage()
  const currentUpazila = upazilas.find((u) => u.upazila_id === selectedUpazilaId)
  const stagesMap = STAGE_TRANSLATIONS[language] || STAGE_TRANSLATIONS.bn

  return (
    <section
      aria-label={t('context_section_label')}
      style={{
        backgroundColor: 'var(--color-bg-surface)',
        borderBottom: '1px solid var(--color-border-default)',
        padding: 'var(--spacing-lg) 0',
        boxShadow: 'var(--shadow-sm)',
        marginBottom: 'var(--spacing-xl)',
      }}
    >
      <div className="app-container">
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr)) auto',
            gap: 'var(--spacing-md)',
            alignItems: 'flex-end',
          }}
        >
          {/* Upazila Selector */}
          <div className="form-group" style={{ marginBottom: 0 }}>
            <label className="form-label" htmlFor="upazila-select">
              <MapPin size={14} style={{ display: 'inline', marginRight: 4, verticalAlign: 'middle' }} />
              {t('upazila_label')}
            </label>
            <select
              id="upazila-select"
              className="form-select"
              value={selectedUpazilaId}
              onChange={(e) => setSelectedUpazilaId(e.target.value)}
            >
              {upazilas.map((u) => {
                const zoneName = u.aez_code === 26 ? t('zone_barind') : t('zone_haor')
                return (
                  <option key={u.upazila_id} value={u.upazila_id}>
                    {language === 'en'
                      ? `${u.name_en} (${u.name_bn}) — ${u.district_name} (${zoneName})`
                      : `${u.name_bn} (${u.name_en}) — ${u.district_name} (${zoneName})`}
                  </option>
                )
              })}
            </select>
          </div>

          {/* Crop Selector */}
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
              {crops.map((c) => (
                <option key={c.crop_id} value={c.crop_id}>
                  {language === 'en'
                    ? `${c.name_en} (${c.name_bn})`
                    : `${c.name_bn} (${c.name_en})`}
                </option>
              ))}
            </select>
          </div>

          {/* Phenological Stage Selector */}
          <div className="form-group" style={{ marginBottom: 0 }}>
            <label className="form-label" htmlFor="stage-select">
              <Calendar size={14} style={{ display: 'inline', marginRight: 4, verticalAlign: 'middle' }} />
              {t('stage_label')}
            </label>
            <select
              id="stage-select"
              className="form-select"
              value={selectedStage}
              onChange={(e) => setSelectedStage(e.target.value)}
            >
              {growthStages.map((stage) => (
                <option key={stage} value={stage}>
                  {stagesMap[stage] || stage}
                </option>
              ))}
            </select>
          </div>

          {/* Refresh Action */}
          <div style={{ marginBottom: 0 }}>
            <button
              className="btn btn-primary"
              onClick={onRefresh}
              disabled={loading}
              aria-busy={loading}
              style={{ width: '100%', minWidth: '160px' }}
              aria-label={t('refresh_aria_label')}
            >
              <RefreshCw size={16} className={loading ? 'animate-spin' : ''} />
              <span>{loading ? t('refresh_loading') : t('refresh_btn')}</span>
            </button>
          </div>
        </div>

        {/* Selected Zone Pill and Contextual Status */}
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
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--spacing-sm)' }}>
            <span style={{ fontWeight: 600 }}>{t('current_zone')}</span>
            <span
              style={{
                backgroundColor: currentUpazila?.aez_code === 26 ? 'var(--primitive-amber-100)' : 'var(--primitive-sky-100)',
                color: currentUpazila?.aez_code === 26 ? 'var(--primitive-amber-900)' : 'var(--primitive-sky-900)',
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
