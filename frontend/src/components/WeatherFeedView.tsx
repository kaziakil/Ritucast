import React from 'react'
import { CloudRain, Sun, Wind, Droplet, Thermometer, CloudLightning, ShieldAlert } from 'lucide-react'
import type { WeatherFeedResponse } from '../types/api'
import { useLanguage } from '../context/LanguageContext'

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
  const { language, t } = useLanguage()

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
      <div className="error-box" role="alert" aria-live="assertive">
        <CloudLightning size={40} style={{ margin: '0 auto 12px' }} />
        <h3 className="error-title">{t('weather_error_title')}</h3>
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
            <span>{t('weather_obs_title')}</span>
          </h3>
          <span className="status-badge" style={{ backgroundColor: 'var(--primitive-sky-100)', color: 'var(--primitive-sky-800)' }}>
            {t('weather_obs_source')} {weather.tier_1_observations.source}
          </span>
        </div>

        <p style={{ color: 'var(--color-text-secondary)', fontSize: 'var(--font-size-caption)', marginBottom: 'var(--spacing-md)' }}>
          {language === 'en' ? 'Last Updated:' : 'হালনাগাদ সময়:'} {weather.tier_1_observations.updated_at_bst} • {language === 'en' ? 'Date:' : 'তারিখ:'} {yesterday.date}
        </p>

        <div className="metric-grid">
          <div className="metric-pill">
            <span className="metric-label">
              <Thermometer size={14} style={{ display: 'inline', marginRight: 4, verticalAlign: 'middle' }} />
              {t('weather_max_temp')}
            </span>
            <span className="metric-value">{yesterday.temp_max_c}° {language === 'en' ? 'C' : 'সে.'}</span>
            <span className="metric-sub">{language === 'en' ? 'Daily maximum' : 'দিনের সর্বোচ্চ'}</span>
          </div>

          <div className="metric-pill">
            <span className="metric-label">
              <Thermometer size={14} style={{ display: 'inline', marginRight: 4, verticalAlign: 'middle' }} />
              {t('weather_min_temp')}
            </span>
            <span className="metric-value">{yesterday.temp_min_c}° {language === 'en' ? 'C' : 'সে.'}</span>
            <span className="metric-sub">{language === 'en' ? 'Nighttime minimum' : 'রাত্রিকালীন সর্বনিম্ন'}</span>
          </div>

          <div className="metric-pill">
            <span className="metric-label">
              <CloudRain size={14} style={{ display: 'inline', marginRight: 4, verticalAlign: 'middle' }} />
              {t('weather_precip_24h')}
            </span>
            <span className="metric-value">{yesterday.precip_24h_mm} {language === 'en' ? 'mm' : 'মিমি'}</span>
            <span className="metric-sub">{language === 'en' ? 'Cumulative precipitation' : 'মোট বৃষ্টি পরিমাণ'}</span>
          </div>

          <div className="metric-pill">
            <span className="metric-label">
              <Sun size={14} style={{ display: 'inline', marginRight: 4, verticalAlign: 'middle' }} />
              {t('weather_solar_rad')}
            </span>
            <span className="metric-value">{yesterday.solar_radiation_mj_m2} MJ/m²</span>
            <span className="metric-sub">{language === 'en' ? 'Daily solar irradiance' : 'দৈনিক মোট সৌরশক্তি'}</span>
          </div>

          <div className="metric-pill">
            <span className="metric-label">
              <Droplet size={14} style={{ display: 'inline', marginRight: 4, verticalAlign: 'middle' }} />
              {t('weather_rh_mean')}
            </span>
            <span className="metric-value">{yesterday.rh_mean_pct}%</span>
            <span className="metric-sub">{language === 'en' ? 'Atmospheric humidity' : 'বাতাসের আর্দ্রতা'}</span>
          </div>

          {yesterday.wind_speed_ms !== undefined && (
            <div className="metric-pill">
              <span className="metric-label">
                <Wind size={14} style={{ display: 'inline', marginRight: 4, verticalAlign: 'middle' }} />
                {t('weather_wind_speed')}
              </span>
              <span className="metric-value">{yesterday.wind_speed_ms} {language === 'en' ? 'm/s' : 'মি/সে.'}</span>
              <span className="metric-sub">{language === 'en' ? 'Surface 2m anemometer' : 'মাটির উপরিভাগের বায়ুপ্রবাহ'}</span>
            </div>
          )}
        </div>
      </div>

      {/* 72-Hour Numerical Weather Forecasts (Tier 3) */}
      <div className="card">
        <div className="card-header">
          <h3 className="card-title">
            <CloudRain size={20} color="var(--color-brand-primary)" />
            <span>{t('weather_fcst_title')}</span>
          </h3>
          <span style={{ fontSize: 'var(--font-size-caption)', color: 'var(--color-text-muted)' }}>
            {language === 'en' ? 'Ensemble Spread:' : 'মডেল এনসেম্বল বিস্তার:'} <strong>{weather.tier_3_forecasts.ensemble_spread_pct}%</strong>
          </span>
        </div>

        <p style={{ color: 'var(--color-text-secondary)', fontSize: 'var(--font-size-caption)', marginBottom: 'var(--spacing-md)' }}>
          {language === 'en' ? 'Model Feeds:' : 'মডেল সূত্র:'} {weather.tier_3_forecasts.model_sources.join(', ')} • {language === 'en' ? 'Issued At:' : 'ইস্যুর সময়:'} {weather.tier_3_forecasts.issued_at_bst}
        </p>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: 'var(--spacing-md)' }}>
          {forecasts.map((fcst, idx) => (
            <div
              key={idx}
              style={{
                border: '1px solid var(--color-border-default)',
                borderRadius: 'var(--radius-lg)',
                padding: 'var(--spacing-lg)',
                backgroundColor: 'var(--color-bg-subtle)',
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
                <span style={{ fontWeight: 700, fontSize: '1.05rem', color: 'var(--color-text-primary)' }}>
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
                  {fcst.lead_time_h} {language === 'en' ? 'h' : 'ঘণ্টা'} • {fcst.confidence === 'HIGH' ? (language === 'en' ? 'High Confidence' : 'উচ্চ আস্থা') : (language === 'en' ? 'Moderate Confidence' : 'মাঝারি আস্থা')}
                </span>
              </div>

              <div style={{ display: 'flex', alignItems: 'baseline', gap: 8, margin: '12px 0' }}>
                <span style={{ fontSize: '1.4rem', fontWeight: 700, color: 'var(--color-text-primary)' }}>
                  {fcst.qpf_precip_mm} {language === 'en' ? 'mm' : 'মিমি'}
                </span>
                <span style={{ color: 'var(--color-text-muted)', fontSize: 'var(--font-size-caption)' }}>
                  {t('weather_qpf')}
                </span>
              </div>

              {/* Rain Probability Progress Bar */}
              <div style={{ marginBottom: 12 }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 'var(--font-size-caption)', marginBottom: 4 }}>
                  <span>{t('weather_rain_prob')}:</span>
                  <strong style={{ color: 'var(--color-brand-primary)' }}>{fcst.precip_probability_pct}%</strong>
                </div>
                <div style={{ height: 8, backgroundColor: 'var(--color-border-default)', borderRadius: '4px', overflow: 'hidden' }}>
                  <div
                    style={{
                      height: '100%',
                      width: `${fcst.precip_probability_pct}%`,
                      backgroundColor: 'var(--color-brand-sky)',
                      borderRadius: '4px',
                    }}
                  />
                </div>
              </div>

              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 'var(--font-size-caption)', color: 'var(--color-text-secondary)', borderTop: '1px solid var(--color-border-default)', paddingTop: 8 }}>
                <span>{language === 'en' ? 'Temp Range:' : 'তাপমাত্রা পরিসীমা:'}</span>
                <strong>{fcst.temp_min_c}° - {fcst.temp_max_c}° {language === 'en' ? 'C' : 'সে.'}</strong>
              </div>
            </div>
          ))}
        </div>

        <div style={{ marginTop: 'var(--spacing-lg)', display: 'flex', alignItems: 'center', gap: 6, fontSize: 'var(--font-size-caption)', color: 'var(--color-text-muted)' }}>
          <ShieldAlert size={14} />
          <span>
            {language === 'en'
              ? 'Forecast models are refreshed automatically every 6 hours from ECMWF and GFS global ensembles.'
              : 'পূর্বাভাস উপাত্ত প্রতি ৬ ঘণ্টা অন্তর ইসিএমডব্লিউএফ ও জিএফএস গ্লোবাল মডেল থেকে স্বয়ংক্রিয়ভাবে নবায়ন করা হয়।'}
          </span>
        </div>
      </div>
    </div>
  )
}
export default WeatherFeedView
