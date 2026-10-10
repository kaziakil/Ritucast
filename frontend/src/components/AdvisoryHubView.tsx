import React from 'react'
import {
  ShieldCheck,
  AlertOctagon,
  Sparkles,
  Info,
  Layers,
  ThermometerSnowflake,
  CheckCircle,
} from 'lucide-react'
import type { AdvisoryResponse, RiskEvaluationResponse } from '../types/api'
import { useLanguage } from '../context/LanguageContext'

interface AdvisoryHubViewProps {
  advisory: AdvisoryResponse | null
  risk: RiskEvaluationResponse | null
  loading: boolean
  error: string | null
}

export const AdvisoryHubView: React.FC<AdvisoryHubViewProps> = ({
  advisory,
  risk,
  loading,
  error,
}) => {
  const { language, t } = useLanguage()

  if (loading) {
    return (
      <div className="card" data-testid="advisory-loading-skeleton">
        <div className="card-header">
          <div className="skeleton" style={{ width: 240, height: 28 }} />
          <div className="skeleton" style={{ width: 120, height: 24 }} />
        </div>
        <div className="skeleton" style={{ width: '100%', height: 140, marginBottom: 16 }} />
        <div className="skeleton" style={{ width: '100%', height: 180 }} />
      </div>
    )
  }

  if (error) {
    return (
      <div className="error-box" role="alert" aria-live="assertive">
        <AlertOctagon size={40} style={{ margin: '0 auto 12px' }} />
        <h3 className="error-title">{t('advisory_error_title')}</h3>
        <p>{error}</p>
      </div>
    )
  }

  if (!advisory) {
    return null
  }

  const rec = advisory.tier_4_recommendation

  return (
    <div>
      {/* Automated Suppression Banner (DEC-10) */}
      {rec.is_suppressed && (
        <div className="suppression-alert" role="alert">
          <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--spacing-sm)', marginBottom: 8 }}>
            <AlertOctagon size={22} color="var(--primitive-amber-800)" />
            <strong style={{ fontSize: '1.1rem' }}>{t('suppression_title')}</strong>
          </div>
          <p style={{ margin: 0, lineHeight: 1.5 }}>
            {t('suppression_body')}
          </p>
        </div>
      )}

      {/* Primary Tier 4 Actionable Recommendation Card */}
      <div className={`card tier-4 severity-${rec.severity}`} style={{ marginBottom: 'var(--spacing-xl)' }}>
        <div className="card-header" style={{ marginBottom: 'var(--spacing-sm)' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--spacing-sm)' }}>
            <span className="tier-badge tier-4-badge">{t('tier_4_title')}</span>
            <span style={{ fontSize: 'var(--font-size-caption)', color: 'var(--color-text-muted)' }}>
              {t('rule_id_prefix')} <strong>{rec.rule_id}</strong>
            </span>
          </div>

          {rec.confidence && (
            <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--spacing-xs)' }}>
              <span
                style={{
                  backgroundColor: rec.confidence.color_hex || 'var(--primitive-green-700)',
                  color: '#fff',
                  padding: '2px 8px',
                  borderRadius: 'var(--radius-pill)',
                  fontSize: 'var(--font-size-meta)',
                  fontWeight: 600,
                }}
              >
                {language === 'en' ? rec.confidence.tier : rec.confidence.tier_bn} ({Math.round(rec.confidence.score * 100)}%)
              </span>
            </div>
          )}
        </div>

        {/* Headline & Body */}
        <h2 className="advisory-hero-title">
          {rec.headline_bn}
        </h2>
        <p className="advisory-hero-body">
          {rec.body_bn}
        </p>

        {/* Structured Content Grid: Action Directives & Technical Rationale */}
        <div className="advisory-content-layout">
          {/* Action Directives Checklist */}
          {rec.action_items_bn && rec.action_items_bn.length > 0 && (
            <div className="advisory-actions-panel">
              <strong style={{ fontSize: 'var(--font-size-body)', color: 'var(--color-text-primary)', display: 'block', marginBottom: 'var(--spacing-xs)' }}>
                {t('action_items_heading')}
              </strong>
              <ul style={{ listStyle: 'none', margin: 0, paddingLeft: 0 }}>
                {rec.action_items_bn.map((item, idx) => (
                  <li
                    key={idx}
                    style={{
                      display: 'flex',
                      alignItems: 'flex-start',
                      gap: 'var(--spacing-sm)',
                      marginBottom: 'var(--spacing-xs)',
                      fontSize: 'var(--font-size-body)',
                    }}
                  >
                    <CheckCircle size={18} color="var(--primitive-green-700)" style={{ flexShrink: 0, marginTop: 3 }} />
                    <span>{item}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Economic / Technical Rationale Breakdown */}
          {rec.rationale_breakdown && (
            <div
              className="advisory-rationale-panel"
              style={{
                backgroundColor: 'var(--color-bg-subtle)',
                border: '1px solid var(--color-border-default)',
                borderRadius: 'var(--radius-md)',
                padding: 'var(--spacing-md)',
                fontSize: 'var(--font-size-caption)',
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginBottom: 6, fontWeight: 600 }}>
                <Sparkles size={16} color="var(--primitive-green-800)" />
                <span>{t('rationale_heading')}</span>
              </div>
              <p style={{ margin: 0, color: 'var(--color-text-secondary)', lineHeight: 1.5 }}>
                {rec.rationale_breakdown.scientific_basis}
              </p>
              {rec.rationale_breakdown.pumping_savings_est_bdt && (
                <div style={{ marginTop: 'var(--spacing-sm)', padding: '4px 8px', backgroundColor: 'rgba(34, 197, 94, 0.12)', borderRadius: 'var(--radius-sm)', border: '1px solid rgba(34, 197, 94, 0.25)' }}>
                  <p style={{ margin: 0, fontWeight: 600, color: 'var(--primitive-green-900)' }}>
                    {t('pumping_savings_prefix')} {rec.rationale_breakdown.pumping_savings_est_bdt}
                  </p>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Mandatory Field Inspection Disclaimer (AGENTS.md) */}
        <div className="field-verification-box">
          <ShieldCheck size={18} color="var(--primitive-slate-700)" style={{ flexShrink: 0 }} />
          <span>
            <strong>{t('field_verification_heading')}</strong> {rec.mandatory_disclaimer_bn}
          </span>
        </div>
      </div>

      {/* 3-Tier Supporting Foundation Accordion / Cards (DEC-08) */}
      <div style={{ marginBottom: 'var(--spacing-xl)' }}>
        <h3 style={{ fontSize: 'var(--font-size-h2)', marginBottom: 'var(--spacing-md)', display: 'flex', alignItems: 'center', gap: 8 }}>
          <Layers size={20} color="var(--color-brand-primary)" />
          <span>{t('supporting_tiers_heading')}</span>
        </h3>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: 'var(--spacing-md)' }}>
          {/* Tier 1 Card: Sensor Observations */}
          <div className="card tier-card tier-1">
            <span className="tier-badge tier-1-badge">{t('tier_1_title')}</span>
            <p style={{ fontSize: 'var(--font-size-body)', marginBottom: 'var(--spacing-sm)' }}>
              {advisory.tier_1_observations.summary_bn}
            </p>
            <div style={{ fontSize: 'var(--font-size-caption)', color: 'var(--color-text-muted)' }}>
              <span>{t('tier_1_source_label')}</span>
              {advisory.tier_1_observations.rainfall_7d_total_mm !== undefined && (
                <div>{t('tier_1_rainfall_7d')} <strong>{advisory.tier_1_observations.rainfall_7d_total_mm} {language === 'en' ? 'mm' : 'মিমি'}</strong></div>
              )}
            </div>
          </div>

          {/* Tier 2 Card: Derived Physical Indicators */}
          <div className="card tier-card tier-2">
            <span className="tier-badge tier-2-badge">{t('tier_2_title')}</span>
            <p style={{ fontSize: 'var(--font-size-body)', marginBottom: 'var(--spacing-sm)' }}>
              {advisory.tier_2_indicators.summary_bn}
            </p>
            <div style={{ fontSize: 'var(--font-size-caption)', color: 'var(--color-text-muted)' }}>
              <span>{t('tier_2_method_label')}</span>
              {advisory.tier_2_indicators.soil_water_deficit_dt_mm !== undefined && (
                <div>{t('tier_2_deficit_label')} <strong>{advisory.tier_2_indicators.soil_water_deficit_dt_mm} {language === 'en' ? 'mm' : 'মিমি'}</strong></div>
              )}
            </div>
          </div>

          {/* Tier 3 Card: Probabilistic Forecasts */}
          <div className="card tier-card tier-3">
            <span className="tier-badge tier-3-badge">{t('tier_3_title')}</span>
            <p style={{ fontSize: 'var(--font-size-body)', marginBottom: 'var(--spacing-sm)' }}>
              {advisory.tier_3_predictions.summary_bn}
            </p>
            <div style={{ fontSize: 'var(--font-size-caption)', color: 'var(--color-text-muted)' }}>
              <span>{t('tier_3_model_label')}</span>
              {advisory.tier_3_predictions.rain_probability_48h_pct !== undefined && (
                <div>{t('tier_3_rain_prob_label')} <strong>{advisory.tier_3_predictions.rain_probability_48h_pct}%</strong></div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Physical Hazard Evaluation Section (DEC-06 Safe) */}
      {risk && risk.hazard_assessments && (
        <div className="card" style={{ marginBottom: 'var(--spacing-xl)' }}>
          <div className="card-header">
            <h3 className="card-title">
              <ThermometerSnowflake size={20} color="var(--primitive-amber-700)" />
              <span>{t('hazard_eval_heading')}</span>
            </h3>
            <span
              style={{
                backgroundColor:
                  risk.overall_hazard_tier === 'CRITICAL'
                    ? 'var(--primitive-red-100)'
                    : risk.overall_hazard_tier === 'HIGH'
                    ? 'var(--primitive-amber-100)'
                    : 'var(--primitive-green-100)',
                color:
                  risk.overall_hazard_tier === 'CRITICAL'
                    ? 'var(--primitive-red-800)'
                    : risk.overall_hazard_tier === 'HIGH'
                    ? 'var(--primitive-amber-800)'
                    : 'var(--primitive-green-800)',
                padding: '4px 10px',
                borderRadius: 'var(--radius-pill)',
                fontWeight: 600,
                fontSize: 'var(--font-size-caption)',
              }}
            >
              {t('hazard_eval_overall')} {language === 'en' ? risk.overall_hazard_tier : risk.overall_hazard_tier_bn}
            </span>
          </div>

          <div className="metric-grid">
            {risk.hazard_assessments.map((hazard, i) => (
              <div key={i} className="metric-pill">
                <span className="metric-label">{language === 'en' ? hazard.hazard_tier : hazard.hazard_tier_bn}</span>
                <span className="metric-value">
                  {hazard.primary_metric_name === 'soil_water_deficit_dt_mm'
                    ? `${hazard.primary_metric_value} ${language === 'en' ? 'mm' : 'মিমি'}`
                    : hazard.primary_metric_name === 'haor_flood_index_iflood'
                    ? `${hazard.primary_metric_value}`
                    : `${hazard.primary_metric_value}° ${language === 'en' ? 'C' : 'সে.'}`}
                </span>
                <span className="metric-sub">
                  {language === 'en' ? 'Metric' : 'নির্ণায়ক'}: {hazard.primary_metric_name} ({language === 'en' ? 'threshold' : 'সীমা'}: {hazard.threshold_applied})
                </span>
                <span style={{ marginTop: 6, fontSize: '0.75rem', fontWeight: 600, color: hazard.action_warranted ? 'var(--primitive-red-700)' : 'var(--primitive-green-700)' }}>
                  {hazard.action_warranted
                    ? `• ${t('hazard_action_warranted')}`
                    : `• ${t('hazard_action_not_warranted')}`}
                </span>
              </div>
            ))}
          </div>

          <div style={{ marginTop: 'var(--spacing-md)', fontSize: 'var(--font-size-caption)', color: 'var(--color-text-muted)', display: 'flex', alignItems: 'center', gap: 6 }}>
            <Info size={14} />
            <span>{risk.scientific_disclaimer_bn}</span>
          </div>
        </div>
      )}
    </div>
  )
}
export default AdvisoryHubView
