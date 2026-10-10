import React from 'react'
import { Droplets, Activity, Gauge, HelpCircle, CheckCircle, AlertTriangle } from 'lucide-react'
import type { WaterBalanceResponse } from '../types/api'

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
      <div className="error-box">
        <Droplets size={40} style={{ margin: '0 auto 12px' }} />
        <h3 className="error-title">মাটির আর্দ্রতা ও বাষ্পীভবন তথ্য পাওয়া যায়নি</h3>
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
          borderLeft: `5px solid ${isDryingOk ? 'var(--primitive-green-600)' : 'var(--primitive-red-600)'}`,
          backgroundColor: isDryingOk ? 'var(--primitive-green-50)' : 'var(--primitive-red-50)',
          marginBottom: 'var(--spacing-xl)',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--spacing-md)' }}>
          {isDryingOk ? (
            <CheckCircle size={32} color="var(--primitive-green-700)" style={{ flexShrink: 0 }} />
          ) : (
            <AlertTriangle size={32} color="var(--primitive-red-700)" style={{ flexShrink: 0 }} />
          )}
          <div>
            <span
              style={{
                fontSize: 'var(--font-size-meta)',
                fontWeight: 700,
                color: isDryingOk ? 'var(--primitive-green-800)' : 'var(--primitive-red-800)',
                textTransform: 'uppercase',
                letterSpacing: '0.05em',
              }}
            >
              পর্যায়ক্রমিক ভেজানো ও শুকানো (AWD) নিরীক্ষণ
            </span>
            <h2 style={{ fontSize: '1.25rem', marginTop: 2, marginBottom: 4, color: 'var(--primitive-neutral-900)' }}>
              {wb.status_bn}
            </h2>
            <p style={{ margin: 0, fontSize: 'var(--font-size-body)', color: 'var(--color-text-secondary)' }}>
              {isDryingOk
                ? 'শিকড় অঞ্চলে সহনীয় আর্দ্রতা রয়েছে। অপ্রয়োজনীয় পাম্প চালনা স্থগিত রাখলে ডিজেল ও বিদ্যুৎ সাশ্রয় হবে।'
                : 'মাটির আর্দ্রতা সংকটজনক সীমায় নেমেছে (Dt ≥ RAW)। অবিলম্বে হালকা সেচ প্রদান নিশ্চিত করুন।'}
            </p>
          </div>
        </div>
      </div>

      {/* Root-Zone Water Deficit Progress Gauge */}
      <div className="card" style={{ marginBottom: 'var(--spacing-xl)' }}>
        <div className="card-header">
          <h3 className="card-title">
            <Gauge size={20} color="var(--color-brand-primary)" />
            <span>শিকড় অঞ্চলের পানি ঘাটতি নির্দেশক ($D_t$ বনাম TAW/RAW)</span>
          </h3>
          <span style={{ fontSize: 'var(--font-size-caption)', color: 'var(--color-text-muted)' }}>
            হিসাবের তারিখ: {wb.calculation_date}
          </span>
        </div>

        <div style={{ margin: 'var(--spacing-xl) 0' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8, fontSize: 'var(--font-size-body)' }}>
            <span>
              বর্তমান পানির ঘাটতি ($D_t$): <strong>{wb.current_soil_water_deficit_dt_mm} মিমি</strong>
            </span>
            <span style={{ color: 'var(--color-text-muted)', fontSize: 'var(--font-size-caption)' }}>
              মোট ব্যবহারযোগ্য পানি (TAW): {soil.total_available_water_taw_mm} মিমি
            </span>
          </div>

          {/* Visual Track */}
          <div
            style={{
              height: 24,
              backgroundColor: 'var(--primitive-slate-200)',
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
                borderRight: '2px dashed var(--primitive-green-700)',
              }}
              title={`নিরাপদ শুকানোর সীমা (RAW = ${soil.readily_available_water_raw_mm} মিমি)`}
            />

            {/* Current Depletion Fill */}
            <div
              style={{
                height: '100%',
                width: `${deficitPct}%`,
                backgroundColor: isDryingOk ? 'var(--primitive-green-600)' : 'var(--primitive-red-600)',
                borderRadius: 'var(--radius-pill)',
                transition: 'width 0.5s ease',
              }}
            />
          </div>

          <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: 6, fontSize: '0.75rem', color: 'var(--color-text-muted)' }}>
            <span>০ মিমি (সম্পৃক্ত)</span>
            <span style={{ color: 'var(--primitive-green-800)', fontWeight: 600 }}>
              ← এডাব্লিউডি অনুমোদিত অঞ্চল (RAW = {soil.readily_available_water_raw_mm} মিমি) →
            </span>
            <span>{soil.total_available_water_taw_mm} মিমি (স্থায়ী ম্লান বিন্দু)</span>
          </div>
        </div>

        {/* Soil Physics & Hydraulic Properties */}
        <div className="metric-grid">
          <div className="metric-pill">
            <span className="metric-label">মাটির ধরন (Soil Texture)</span>
            <span className="metric-value" style={{ fontSize: '1.05rem' }}>{soil.texture}</span>
            <span className="metric-sub">বরেন্দ্র প্রাচীন কাদামাটি (Paleosol)</span>
          </div>

          <div className="metric-pill">
            <span className="metric-label">কার্যকর শিকড়ের গভীরতা</span>
            <span className="metric-value">{soil.root_zone_depth_m} মিটার</span>
            <span className="metric-sub">বোরো ধান শিকড় স্তর ($Z_r$)</span>
          </div>

          <div className="metric-pill">
            <span className="metric-label">সহজে ব্যবহারযোগ্য পানি (RAW)</span>
            <span className="metric-value">{soil.readily_available_water_raw_mm} মিমি</span>
            <span className="metric-sub">সেচ প্রদানের ক্রান্তীয় সীমা ($p=0.35$)</span>
          </div>

          <div className="metric-pill">
            <span className="metric-label">মোট ব্যবহারযোগ্য পানি (TAW)</span>
            <span className="metric-value">{soil.total_available_water_taw_mm} মিমি</span>
            <span className="metric-sub">মাটির ধারণক্ষমতা ($FC - PWP$)</span>
          </div>
        </div>
      </div>

      {/* Evapotranspiration Components (FAO-56 Penman-Monteith) */}
      <div className="card">
        <div className="card-header">
          <h3 className="card-title">
            <Activity size={20} color="var(--primitive-sky-700)" />
            <span>FAO-56 পেনম্যান-মন্টিথ বাষ্পীভবন ও ফসলের চাহিদা</span>
          </h3>
          <span className="tier-badge tier-2-badge">EQN-ET0-01 • EQN-ETC-01</span>
        </div>

        <div className="metric-grid">
          <div className="metric-pill">
            <span className="metric-label">রেফারেন্স বাষ্পীভবন ($ET_0$)</span>
            <span className="metric-value">{wb.fao56_et0_mm_day} মিমি/দিন</span>
            <span className="metric-sub">আদর্শ ঘাস আচ্ছাদনের দৈনিক বাষ্পীভবন</span>
          </div>

          <div className="metric-pill">
            <span className="metric-label">ফসলের সক্রিয় গুণক ($K_c$)</span>
            <span className="metric-value">{wb.calibrated_kc}</span>
            <span className="metric-sub">বিআরআরআই ক্যালিব্রেটেড বৃদ্ধির পর্যায়</span>
          </div>

          <div className="metric-pill">
            <span className="metric-label">ফসলের পানির দৈনিক চাহিদা ($ET_c$)</span>
            <span className="metric-value">{wb.crop_etc_mm_day} মিমি/দিন</span>
            <span className="metric-sub">$ET_c = K_c \times ET_0$</span>
          </div>
        </div>

        <div style={{ marginTop: 'var(--spacing-md)', fontSize: 'var(--font-size-caption)', color: 'var(--color-text-secondary)', display: 'flex', alignItems: 'center', gap: 6 }}>
          <HelpCircle size={14} />
          <span>সূত্র ও পদ্ধতি: জাতিসংঘের খাদ্য ও কৃষি সংস্থা (FAO Irrigation and Drainage Paper No. 56)।</span>
        </div>
      </div>
    </div>
  )
}
