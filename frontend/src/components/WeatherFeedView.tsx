import React from 'react'
import { CloudRain, Sun, Wind, Droplet, Thermometer, CloudLightning, ShieldAlert } from 'lucide-react'
import type { WeatherFeedResponse } from '../types/api'

interface WeatherFeedViewProps {
  weather: WeatherFeedResponse | null
  loading: boolean
  error: string | null
}

export const WeatherFeedView: React.FC<WeatherFeedViewProps> = ({
  weather,
  loading,
  error,
}) => {
  if (loading) {
    return (
      <div className="card">
        <div className="skeleton" style={{ width: 220, height: 28, marginBottom: 16 }} />
        <div className="metric-grid" style={{ marginBottom: 24 }}>
          <div className="skeleton" style={{ height: 90 }} />
          <div className="skeleton" style={{ height: 90 }} />
          <div className="skeleton" style={{ height: 90 }} />
          <div className="skeleton" style={{ height: 90 }} />
        </div>
        <div className="skeleton" style={{ height: 160 }} />
      </div>
    )
  }

  if (error) {
    return (
      <div className="error-box">
        <CloudLightning size={40} style={{ margin: '0 auto 12px' }} />
        <h3 className="error-title">আবহাওয়া তথ্য লোড করা যায়নি</h3>
        <p>{error}</p>
      </div>
    )
  }

  if (!weather) {
    return null
  }

  const yesterday = weather.tier_1_observations.yesterday
  const forecasts = weather.tier_3_forecasts.daily_forecast

  return (
    <div>
      {/* Yesterday's Empirical Sensor Observations (Tier 1) */}
      <div className="card" style={{ marginBottom: 'var(--spacing-xl)' }}>
        <div className="card-header">
          <h3 className="card-title">
            <Sun size={20} color="var(--primitive-amber-600)" />
            <span>বিগত ২৪ ঘণ্টার প্রত্যক্ষ আবহাওয়া পর্যবেক্ষণ (Tier 1)</span>
          </h3>
          <span className="status-badge" style={{ backgroundColor: 'var(--primitive-sky-100)', color: 'var(--primitive-sky-800)' }}>
            উৎস: {weather.tier_1_observations.source}
          </span>
        </div>

        <p style={{ color: 'var(--color-text-secondary)', fontSize: 'var(--font-size-caption)', marginBottom: 'var(--spacing-md)' }}>
          হালনাগাদ সময়: {weather.tier_1_observations.updated_at_bst} • তারিখ: {yesterday.date}
        </p>

        <div className="metric-grid">
          <div className="metric-pill">
            <span className="metric-label">
              <Thermometer size={14} style={{ display: 'inline', marginRight: 4, verticalAlign: 'middle' }} />
              সর্বোচ্চ তাপমাত্রা
            </span>
            <span className="metric-value">{yesterday.temp_max_c}° সে.</span>
            <span className="metric-sub">দিনের সর্বোচ্চ</span>
          </div>

          <div className="metric-pill">
            <span className="metric-label">
              <Thermometer size={14} style={{ display: 'inline', marginRight: 4, verticalAlign: 'middle' }} />
              সর্বনিম্ন তাপমাত্রা
            </span>
            <span className="metric-value">{yesterday.temp_min_c}° সে.</span>
            <span className="metric-sub">রাত্রিকালীন সর্বনিম্ন</span>
          </div>

          <div className="metric-pill">
            <span className="metric-label">
              <CloudRain size={14} style={{ display: 'inline', marginRight: 4, verticalAlign: 'middle' }} />
              বৃষ্টিপাত (২৪ ঘণ্টা)
            </span>
            <span className="metric-value">{yesterday.precip_24h_mm} মিমি</span>
            <span className="metric-sub">মোট বৃষ্টি পরিমাণ</span>
          </div>

          <div className="metric-pill">
            <span className="metric-label">
              <Sun size={14} style={{ display: 'inline', marginRight: 4, verticalAlign: 'middle' }} />
              সৌর বিকিরণ
            </span>
            <span className="metric-value">{yesterday.solar_radiation_mj_m2} MJ/m²</span>
            <span className="metric-sub">দৈনিক মোট সৌরশক্তি</span>
          </div>

          <div className="metric-pill">
            <span className="metric-label">
              <Droplet size={14} style={{ display: 'inline', marginRight: 4, verticalAlign: 'middle' }} />
              গড় আপেক্ষিক আর্দ্রতা
            </span>
            <span className="metric-value">{yesterday.rh_mean_pct}%</span>
            <span className="metric-sub">বাতাসের আর্দ্রতা</span>
          </div>

          {yesterday.wind_speed_ms !== undefined && (
            <div className="metric-pill">
              <span className="metric-label">
                <Wind size={14} style={{ display: 'inline', marginRight: 4, verticalAlign: 'middle' }} />
                বাতাসের গতিবেগ (২ মি.)
              </span>
              <span className="metric-value">{yesterday.wind_speed_ms} মি/সে.</span>
              <span className="metric-sub">মাটির উপরিভাগের বায়ুপ্রবাহ</span>
            </div>
          )}
        </div>
      </div>

      {/* 72-Hour Numerical Weather Forecasts (Tier 3) */}
      <div className="card">
        <div className="card-header">
          <h3 className="card-title">
            <CloudRain size={20} color="var(--color-brand-primary)" />
            <span>আগামী ৭২ ঘণ্টার সম্ভাব্যতাভিত্তিক আবহাওয়া পূর্বাভাস (Tier 3)</span>
          </h3>
          <span style={{ fontSize: 'var(--font-size-caption)', color: 'var(--color-text-muted)' }}>
            মডেল এনসেম্বল বিস্তার: <strong>{weather.tier_3_forecasts.ensemble_spread_pct}%</strong>
          </span>
        </div>

        <p style={{ color: 'var(--color-text-secondary)', fontSize: 'var(--font-size-caption)', marginBottom: 'var(--spacing-md)' }}>
          মডেল সূত্র: {weather.tier_3_forecasts.model_sources.join(', ')} • ইস্যুর সময়: {weather.tier_3_forecasts.issued_at_bst}
        </p>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: 'var(--spacing-md)' }}>
          {forecasts.map((fcst, idx) => (
            <div
              key={idx}
              style={{
                border: '1px solid var(--color-border-default)',
                borderRadius: 'var(--radius-lg)',
                padding: 'var(--spacing-lg)',
                backgroundColor: 'var(--primitive-neutral-50)',
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: varSp(8) }}>
                <span style={{ fontWeight: 700, fontSize: '1.05rem', color: 'var(--primitive-neutral-900)' }}>
                  {fcst.date}
                </span>
                <span
                  style={{
                    backgroundColor: fcst.confidence === 'HIGH' ? 'var(--primitive-green-100)' : 'var(--primitive-amber-100)',
                    color: fcst.confidence === 'HIGH' ? 'var(--primitive-green-800)' : 'var(--primitive-amber-800)',
                    padding: '2px 8px',
                    borderRadius: 'var(--radius-pill)',
                    fontSize: '0.75rem',
                    fontWeight: 600,
                  }}
                >
                  {fcst.lead_time_h} ঘণ্টা • {fcst.confidence === 'HIGH' ? 'উচ্চ আস্থা' : 'মাঝারি আস্থা'}
                </span>
              </div>

              <div style={{ display: 'flex', alignItems: 'baseline', gap: 8, margin: '12px 0' }}>
                <span style={{ fontSize: '1.4rem', fontWeight: 700, color: 'var(--primitive-neutral-900)' }}>
                  {fcst.qpf_precip_mm} মিমি
                </span>
                <span style={{ color: 'var(--color-text-muted)', fontSize: 'var(--font-size-caption)' }}>
                  বৃষ্টিপাতের পূর্বাভাস (QPF)
                </span>
              </div>

              {/* Rain Probability Progress Bar */}
              <div style={{ marginBottom: 12 }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 'var(--font-size-caption)', marginBottom: 4 }}>
                  <span>বৃষ্টির সম্ভাবনা:</span>
                  <strong style={{ color: 'var(--color-brand-primary)' }}>{fcst.precip_probability_pct}%</strong>
                </div>
                <div style={{ height: 8, backgroundColor: 'var(--primitive-neutral-200)', borderRadius: varRad(4), overflow: 'hidden' }}>
                  <div
                    style={{
                      height: '100%',
                      width: `${fcst.precip_probability_pct}%`,
                      backgroundColor: 'var(--primitive-sky-600)',
                      borderRadius: varRad(4),
                    }}
                  />
                </div>
              </div>

              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 'var(--font-size-caption)', color: 'var(--color-text-secondary)', borderTop: '1px solid var(--color-border-default)', paddingTop: 8 }}>
                <span>তাপমাত্রা পরিসীমা:</span>
                <strong>{fcst.temp_min_c}° - {fcst.temp_max_c}° সে.</strong>
              </div>
            </div>
          ))}
        </div>

        <div style={{ marginTop: 'var(--spacing-lg)', display: 'flex', alignItems: 'center', gap: 6, fontSize: 'var(--font-size-caption)', color: 'var(--color-text-muted)' }}>
          <ShieldAlert size={14} />
          <span>পূর্বাভাস উপাত্ত প্রতি ৬ ঘণ্টা অন্তর ইসিএমডব্লিউএফ ও জিএফএস গ্লোবাল মডেল থেকে স্বয়ংক্রিয়ভাবে নবায়ন করা হয়।</span>
        </div>
      </div>
    </div>
  )
}

function varSp(px: number) {
  return `${px}px`
}

function varRad(px: number) {
  return `${px}px`
}
