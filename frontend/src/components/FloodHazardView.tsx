import React from 'react'
import { Waves, AlertTriangle, CloudRain, Eye, ArrowUpRight, Info } from 'lucide-react'
import type { FloodHazardResponse } from '../types/api'

interface FloodHazardViewProps {
  flood: FloodHazardResponse | null
  loading: boolean
  error: string | null
}

export const FloodHazardView: React.FC<FloodHazardViewProps> = ({
  flood,
  loading,
  error,
}) => {
  if (loading) {
    return (
      <div className="card">
        <div className="skeleton" style={{ width: 280, height: 28, marginBottom: 16 }} />
        <div className="skeleton" style={{ width: '100%', height: 160, marginBottom: 20 }} />
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
        <Waves size={40} style={{ margin: '0 auto 12px' }} />
        <h3 className="error-title">বন্যা ঝুঁকি নির্দেশক পাওয়া যায়নি</h3>
        <p>{error}</p>
      </div>
    )
  }

  if (!flood) {
    return null
  }

  const f = flood.tier_2_indicators
  const isNotApplicable = f.hazard_tier === 'NOT_APPLICABLE'

  if (isNotApplicable) {
    return (
      <div className="card" style={{ borderLeft: '4px solid var(--primitive-slate-500)' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--spacing-md)' }}>
          <Info size={32} color="var(--primitive-slate-600)" style={{ flexShrink: 0 }} />
          <div>
            <h3 style={{ fontSize: '1.2rem', marginBottom: 4 }}>
              হাওড় আকস্মিক বন্যা ঝুঁকি সূচক প্রযোজ্য নয়
            </h3>
            <p style={{ margin: 0, color: 'var(--color-text-secondary)' }}>
              নির্বাচিত উপজেলাটি (<strong>{flood.name_bn}</strong>) উচ্চ বরেন্দ্র অঞ্চলের (AEZ-26) অন্তর্গত। এখানে ভূগর্ভস্থ পানির ঘাটতি ও খরা প্রধান ঝুঁকি; হাওড় নদী অববাহিকার আকস্মিক বন্যা ঝুঁকি শুধুমাত্র সিলেট বিভাগের হাওড় অঞ্চলের (AEZ-21: তাহিরপুর, সুনামগঞ্জ সদর) জন্য কার্যকর।
            </p>
          </div>
        </div>
      </div>
    )
  }

  const isEmergency = f.hazard_tier === 'EMERGENCY'
  const isWarning = f.hazard_tier === 'WARNING'
  const indexPct = Math.round(f.flood_hazard_index_iflood * 100)

  return (
    <div>
      {/* Early Harvest Alert Banner */}
      {f.trigger_early_harvest && (
        <div
          className="card"
          style={{
            backgroundColor: 'var(--primitive-red-50)',
            border: '2px solid var(--primitive-red-600)',
            marginBottom: 'var(--spacing-xl)',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--spacing-md)' }}>
            <AlertTriangle size={36} color="var(--primitive-red-700)" style={{ flexShrink: 0 }} />
            <div>
              <span
                style={{
                  backgroundColor: 'var(--primitive-red-700)',
                  color: '#fff',
                  padding: '2px 8px',
                  borderRadius: 'var(--radius-pill)',
                  fontSize: '0.75rem',
                  fontWeight: 700,
                  textTransform: 'uppercase',
                }}
              >
                জরুরি ফসল কর্তন সতর্কতা (RULE-FLD-01)
              </span>
              <h2 style={{ fontSize: '1.3rem', marginTop: 4, marginBottom: 4, color: 'var(--primitive-red-900)' }}>
                হাওড়ে আকস্মিক বন্যার আশঙ্কা: ৮০% পাকা ধান অবিলম্বে কর্তন করুন
              </h2>
              <p style={{ margin: 0, color: 'var(--primitive-red-800)', fontSize: 'var(--font-size-body)' }}>
                সুরমা নদীর পানি বিপৎসীমার কাছাকাছি উঠেছে এবং মেঘালয় পাহাড়ে ভারী বর্ষণ অব্যাহত রয়েছে। পরবর্তী ৪৮ ঘণ্টার মধ্যে বাঁধ উপচে ফসলি জমি প্লাবিত হওয়ার চরম ঝুঁকি রয়েছে।
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Flood Hazard Gauge & Severity */}
      <div className="card" style={{ marginBottom: 'var(--spacing-xl)' }}>
        <div className="card-header">
          <h3 className="card-title">
            <Waves size={20} color="var(--color-brand-primary)" />
            <span>হাওড় সমন্বিত আকস্মিক বন্যা ঝুঁকি সূচক (I_flood)</span>
          </h3>
          <span
            style={{
              backgroundColor: isEmergency
                ? 'var(--primitive-red-100)'
                : isWarning
                ? 'var(--primitive-amber-100)'
                : 'var(--primitive-green-100)',
              color: isEmergency
                ? 'var(--primitive-red-800)'
                : isWarning
                ? 'var(--primitive-amber-800)'
                : 'var(--primitive-green-800)',
              padding: '4px 12px',
              borderRadius: 'var(--radius-pill)',
              fontWeight: 700,
              fontSize: 'var(--font-size-caption)',
            }}
          >
            {f.hazard_tier_bn}
          </span>
        </div>

        <p style={{ fontSize: 'var(--font-size-caption)', color: 'var(--color-text-muted)', marginBottom: 'var(--spacing-lg)' }}>
          মূল্যায়ন সময়: {f.evaluation_timestamp_bst} • সমীকরণ: <strong>IDX-FLD-01</strong>
        </p>

        {/* Index Progress Bar */}
        <div style={{ margin: 'var(--spacing-xl) 0' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
            <span>সূচক মান: <strong>{f.flood_hazard_index_iflood}</strong> (০.০০ – ১.০০)</span>
            <span style={{ fontWeight: 600, color: isEmergency ? 'var(--primitive-red-700)' : 'var(--primitive-green-700)' }}>
              ঝুঁকি স্তর: {indexPct}%
            </span>
          </div>

          <div
            style={{
              height: 24,
              backgroundColor: 'var(--primitive-slate-200)',
              borderRadius: 'var(--radius-pill)',
              position: 'relative',
              overflow: 'hidden',
            }}
          >
            {/* Warning threshold line at 0.60 */}
            <div
              style={{
                position: 'absolute',
                left: '60%',
                top: 0,
                bottom: 0,
                width: 2,
                backgroundColor: 'var(--primitive-amber-600)',
                zIndex: 2,
              }}
              title="সতর্কতা সীমা (০.৬০)"
            />
            {/* Emergency threshold line at 0.75 */}
            <div
              style={{
                position: 'absolute',
                left: '75%',
                top: 0,
                bottom: 0,
                width: 2,
                backgroundColor: 'var(--primitive-red-600)',
                zIndex: 2,
              }}
              title="জরুরি সীমা (০.৭৫)"
            />

            <div
              style={{
                height: '100%',
                width: `${indexPct}%`,
                backgroundColor: isEmergency
                  ? 'var(--primitive-red-600)'
                  : isWarning
                  ? 'var(--primitive-amber-500)'
                  : 'var(--primitive-green-600)',
                borderRadius: 'var(--radius-pill)',
                transition: 'width 0.5s ease',
              }}
            />
          </div>

          <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: 6, fontSize: '0.75rem', color: 'var(--color-text-muted)' }}>
            <span>০.০০ (স্বাভাবিক)</span>
            <span>০.৬০ (সতর্কবার্তা)</span>
            <span style={{ color: 'var(--primitive-red-700)', fontWeight: 600 }}>০.৭৫ (জরুরি কর্তন সীমা)</span>
            <span>১.০০ (সর্বোচ্চ বন্যা)</span>
          </div>
        </div>

        {/* Sub-Indices Breakdown */}
        <div className="metric-grid">
          <div className="metric-pill">
            <span className="metric-label">
              <CloudRain size={14} style={{ display: 'inline', marginRight: 4, verticalAlign: 'middle' }} />
              মেঘালয় ক্যাচমেন্ট বৃষ্টিপাত (P_cat)
            </span>
            <span className="metric-value">
              {f.sub_indices.meghalaya_catchment_48h_rain_mm !== undefined
                ? `${f.sub_indices.meghalaya_catchment_48h_rain_mm} মিমি`
                : `${f.sub_indices.f_P || 0}`}
            </span>
            <span className="metric-sub">৪৮ ঘণ্টার পুঞ্জীভূত পাহাড়ি বৃষ্টি ($w_1 = 0.35$)</span>
          </div>

          <div className="metric-pill">
            <span className="metric-label">
              <ArrowUpRight size={14} style={{ display: 'inline', marginRight: 4, verticalAlign: 'middle' }} />
              সুরমা নদীর পানির স্তর ও বৃদ্ধির হার
            </span>
            <span className="metric-value">
              {f.sub_indices.surma_river_stage_m !== undefined
                ? `${f.sub_indices.surma_river_stage_m} মি.`
                : `${f.sub_indices.f_S || 0}`}
            </span>
            <span className="metric-sub">
              বিপৎসীমা: ৮.২৫ মি. • বৃদ্ধির হার: +০.৮৫ মি/দিন
            </span>
          </div>

          <div className="metric-pill">
            <span className="metric-label">
              <Eye size={14} style={{ display: 'inline', marginRight: 4, verticalAlign: 'middle' }} />
              রাডার স্যাটেলাইট প্লাবন অনুপাত ($f_I$)
            </span>
            <span className="metric-value">
              {f.sub_indices.sentinel1_sar_inundation_pct !== undefined
                ? `${f.sub_indices.sentinel1_sar_inundation_pct}%`
                : `${f.sub_indices.f_I || 0}`}
            </span>
            <span className="metric-sub">Sentinel-1 SAR C-band রাডার পরিমাপ</span>
          </div>
        </div>
      </div>
    </div>
  )
}
