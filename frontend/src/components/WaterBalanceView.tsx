import React from 'react'
import { Droplets, Activity, Gauge, HelpCircle, CheckCircle, AlertTriangle } from 'lucide-react'
import type { WaterBalanceResponse } from '../types/api'
import { useLanguage } from '../context/LanguageContext'

interface WaterBalanceViewProps {
  waterBalance: WaterBalanceResponse | null
  loading: boolean
  error: string | null
}

export const WaterBalanceView: React.FC<WaterBalanceViewProps> = ({
  waterBalance,
  loading,
  error,
}) => {
  const { language, t } = useLanguage()

  if (loading) {
    return (
      <div className="card">
        <div className="skeleton" style={{ width: 260, height: 28, marginBottom: 16 }} />
        <div className="skeleton" style={{ width: '100%', height: 180, marginBottom: 20 }} />
        <div className="metric-grid">
          <div className="skeleton" style={{ height: 90 }} />
          <div className="skeleton" style={{ height: 90 }} />
          <div className="skeleton" style={{ height: 90 }} />
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="error-box" role="alert" aria-live="assertive">
        <Droplets size={40} style={{ margin: '0 auto 12px' }} />
        <h3 className="error-title">{t('water_error_title')}</h3>
        <p>{error}</p>
      </div>
    )
  }

  if (!waterBalance) {
    return null
  }

  const wb = waterBalance.tier_2_indicators
  const soil = wb.soil_properties
  const isDryingOk = wb.status === 'AWD_DRYING_PERMISSIBLE'
  const deficitPct = Math.min(100, Math.round((wb.current_soil_water_deficit_dt_mm / soil.total_available_water_taw_mm) * 100))
  const rawPct = Math.round((soil.readily_available_water_raw_mm / soil.total_available_water_taw_mm) * 100)

  return (
    <div>
      {/* AWD Status Banner */}
      <div
        className="card"
        style={{
          borderLeft: `5px solid ${isDryingOk ? 'var(--color-brand-primary)' : 'var(--primitive-red-600)'}`,
          backgroundColor: isDryingOk ? 'var(--color-status-success-bg)' : 'var(--color-status-critical-bg)',
          marginBottom: 'var(--spacing-xl)',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--spacing-md)' }}>
          {isDryingOk ? (
            <CheckCircle size={32} color="var(--color-brand-primary)" style={{ flexShrink: 0 }} />
          ) : (
            <AlertTriangle size={32} color="var(--primitive-red-600)" style={{ flexShrink: 0 }} />
          )}
          <div>
            <span
              style={{
                fontSize: 'var(--font-size-meta)',
                fontWeight: 700,
                color: isDryingOk ? 'var(--color-brand-primary)' : 'var(--primitive-red-600)',
                textTransform: 'uppercase',
                letterSpacing: '0.05em',
              }}
            >
              {language === 'en'
                ? 'Alternate Wetting and Drying (AWD) Monitor'
                : 'পর্যায়ক্রমিক ভেজানো ও শুকানো (AWD) নিরীক্ষণ'}
            </span>
            <h2 style={{ fontSize: '1.25rem', marginTop: 2, marginBottom: 4, color: 'var(--color-text-primary)' }}>
              {language === 'en'
                ? (isDryingOk ? t('water_awd_drying_ok') : t('water_awd_irrigation_needed'))
                : wb.status_bn}
            </h2>
            <p style={{ margin: 0, fontSize: 'var(--font-size-body)', color: 'var(--color-text-secondary)' }}>
              {isDryingOk
                ? (language === 'en' ? t('water_awd_desc_ok') : 'শিকড় অঞ্চলে সহনীয় আর্দ্রতা রয়েছে। অপ্রয়োজনীয় পাম্প চালনা স্থগিত রাখলে ডিজেল ও বিদ্যুৎ সাশ্রয় হবে।')
                : (language === 'en' ? t('water_awd_desc_needed') : 'মাটির আর্দ্রতা সংকটজনক সীমায় নেমেছে (Dt ≥ RAW)। অবিলম্বে হালকা সেচ প্রদান নিশ্চিত করুন।')}
            </p>
          </div>
        </div>
      </div>

      {/* Root-Zone Water Deficit Progress Gauge */}
      <div className="card" style={{ marginBottom: 'var(--spacing-xl)' }}>
        <div className="card-header">
          <h3 className="card-title">
            <Gauge size={20} color="var(--color-brand-primary)" />
            <span>{t('water_deficit_label')} ($D_t$ বনাম TAW/RAW)</span>
          </h3>
          <span style={{ fontSize: 'var(--font-size-caption)', color: 'var(--color-text-muted)' }}>
            {language === 'en' ? 'Calculated:' : 'হিসাবের তারিখ:'} {wb.calculation_date}
          </span>
        </div>

        <div style={{ margin: 'var(--spacing-xl) 0' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8, fontSize: 'var(--font-size-body)' }}>
            <span>
              {language === 'en' ? 'Current Deficit' : 'বর্তমান পানির ঘাটতি'} ($D_t$): <strong>{wb.current_soil_water_deficit_dt_mm} {language === 'en' ? 'mm' : 'মিমি'}</strong>
            </span>
            <span style={{ color: 'var(--color-text-muted)', fontSize: 'var(--font-size-caption)' }}>
              {t('water_taw_label')}: {soil.total_available_water_taw_mm} {language === 'en' ? 'mm' : 'মিমি'}
            </span>
          </div>

          {/* Visual Track */}
          <div
            style={{
              height: 24,
              backgroundColor: 'var(--color-border-default)',
              borderRadius: 'var(--radius-pill)',
              position: 'relative',
              overflow: 'hidden',
            }}
          >
            {/* Safe AWD Zone (Up to RAW) */}
            <div
              style={{
                position: 'absolute',
                left: 0,
                top: 0,
                bottom: 0,
                width: `${rawPct}%`,
                backgroundColor: 'rgba(34, 197, 94, 0.25)',
                borderRight: '2px dashed var(--color-brand-primary)',
              }}
              title={`${t('water_raw_label')} = ${soil.readily_available_water_raw_mm} mm`}
            />

            {/* Current Depletion Fill */}
            <div
              style={{
                height: '100%',
                width: `${deficitPct}%`,
                backgroundColor: isDryingOk ? 'var(--color-brand-primary)' : 'var(--primitive-red-600)',
                borderRadius: 'var(--radius-pill)',
                transition: 'width 0.5s ease',
              }}
            />
          </div>

          <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: 6, fontSize: '0.75rem', color: 'var(--color-text-muted)' }}>
            <span>0 {language === 'en' ? 'mm (Saturation)' : 'মিমি (সম্পৃক্ত)'}</span>
            <span style={{ color: 'var(--color-brand-primary)', fontWeight: 600 }}>
              ← AWD Permissible Zone (RAW = {soil.readily_available_water_raw_mm} {language === 'en' ? 'mm' : 'মিমি'}) →
            </span>
            <span>{soil.total_available_water_taw_mm} {language === 'en' ? 'mm (Permanent Wilting Point)' : 'মিমি (স্থায়ী ম্লান বিন্দু)'}</span>
          </div>
        </div>

        {/* Soil Physics & Hydraulic Properties */}
        <div className="metric-grid">
          <div className="metric-pill">
            <span className="metric-label">{language === 'en' ? 'Soil Texture' : 'মাটির ধরন (Soil Texture)'}</span>
            <span className="metric-value" style={{ fontSize: '1.05rem' }}>{soil.texture}</span>
            <span className="metric-sub">{language === 'en' ? 'Barind Old Paleosol Clay' : 'বরেন্দ্র প্রাচীন কাদামাটি (Paleosol)'}</span>
          </div>

          <div className="metric-pill">
            <span className="metric-label">{language === 'en' ? 'Effective Root Depth' : 'কার্যকর শিকড়ের গভীরতা'}</span>
            <span className="metric-value">{soil.root_zone_depth_m} {language === 'en' ? 'm' : 'মিটার'}</span>
            <span className="metric-sub">{language === 'en' ? 'Boro Rice Root Zone (Zr)' : 'বোরো ধান শিকড় স্তর ($Z_r$)'}</span>
          </div>

          <div className="metric-pill">
            <span className="metric-label">{t('water_raw_label')}</span>
            <span className="metric-value">{soil.readily_available_water_raw_mm} {language === 'en' ? 'mm' : 'মিমি'}</span>
            <span className="metric-sub">{language === 'en' ? 'Critical depletion limit (p=0.35)' : 'সেচ প্রদানের ক্রান্তীয় সীমা ($p=0.35$)'}</span>
          </div>

          <div className="metric-pill">
            <span className="metric-label">{t('water_taw_label')}</span>
            <span className="metric-value">{soil.total_available_water_taw_mm} {language === 'en' ? 'mm' : 'মিমি'}</span>
            <span className="metric-sub">{language === 'en' ? 'Total available water capacity' : 'মোট ধারণক্ষম পানি ধারণক্ষমতা'}</span>
          </div>
        </div>
      </div>

      {/* FAO-56 Penman-Monteith Evapotranspiration Parameters */}
      <div className="card">
        <div className="card-header">
          <h3 className="card-title">
            <Activity size={20} color="var(--primitive-sky-600)" />
            <span>{t('water_budget_heading')} (FAO-56 PM)</span>
          </h3>
          <span style={{ fontSize: 'var(--font-size-caption)', color: 'var(--color-text-muted)' }}>
            {language === 'en' ? 'Calibrated Crop Coefficient:' : 'ক্যালিব্রেটেড ক্রপ কো-এফিসিয়েন্ট:'} <strong>K_c = {wb.calibrated_kc}</strong>
          </span>
        </div>

        <div className="metric-grid">
          <div className="metric-pill">
            <span className="metric-label">{t('water_et0_label')}</span>
            <span className="metric-value">{wb.fao56_et0_mm_day} {language === 'en' ? 'mm/day' : 'মিমি/দিন'}</span>
            <span className="metric-sub">{language === 'en' ? 'Atmospheric evaporative demand' : 'বায়ুমণ্ডলীয় প্রস্বেদন চাপ'}</span>
          </div>

          <div className="metric-pill">
            <span className="metric-label">{t('water_kc_label')}</span>
            <span className="metric-value">{wb.calibrated_kc}</span>
            <span className="metric-sub">{waterBalance.growth_stage} {language === 'en' ? 'Growth Stage' : 'বৃদ্ধিকালীন গুণক'}</span>
          </div>

          <div className="metric-pill">
            <span className="metric-label">{t('water_etc_label')}</span>
            <span className="metric-value">{wb.crop_etc_mm_day} {language === 'en' ? 'mm/day' : 'মিমি/দিন'}</span>
            <span className="metric-sub">ET_c = ET_0 × K_c</span>
          </div>
        </div>

        <div style={{ marginTop: 'var(--spacing-lg)', display: 'flex', alignItems: 'center', gap: 6, fontSize: 'var(--font-size-caption)', color: 'var(--color-text-muted)' }}>
          <HelpCircle size={14} />
          <span>
            {language === 'en'
              ? 'Soil water balance utilizes FAO-56 daily depletion accounting coupled with NASA POWER solar and meteorological readings.'
              : 'মাটির আর্দ্রতা হিসাবায়ন এফএও-৫৬ দৈনিক ডেপ্লিশন অ্যাকাউন্টিং পদ্ধতি এবং নাসা পাওয়ার উপগ্রহ উপাত্তের ভিত্তিতে স্বয়ংক্রিয়ভাবে পরিচালিত হয়।'}
          </span>
        </div>
      </div>
    </div>
  )
}
export default WaterBalanceView
