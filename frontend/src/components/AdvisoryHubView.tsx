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
      <div className="error-box">
        <AlertOctagon size={40} style={{ margin: '0 auto 12px' }} />
        <h3 className="error-title">পরামর্শ লোড করা সম্ভব হয়নি</h3>
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
            <strong style={{ fontSize: '1.1rem' }}>পরামর্শ সাময়িকভাবে স্থগিত (স্বয়ংক্রিয় সুরক্ষা নীতি DEC-10)</strong>
          </div>
          <p style={{ margin: 0, lineHeight: 1.5 }}>
            আবহাওয়া পূর্বাভাস মডেলসমূহের মধ্যকার অনিশ্চয়তা ($\ge 50\%$) অথবা সংগৃহীত উপাত্তের সময়কাল ৩৬ ঘণ্টার বেশি হওয়ায় কৃষকদের সুরক্ষার্থে এই পরামর্শটি স্থগিত করা হয়েছে। সেচ বা কর্তন সংক্রান্ত যেকোনো জরুরি সিদ্ধান্তে স্থানীয় উপসহকারী কৃষি কর্মকর্তার (SAAO) সরাসরি পরামর্শ গ্রহণ করুন।
          </p>
        </div>
      )}

      {/* Primary Tier 4 Actionable Recommendation Card */}
      <div className={`card tier-4 severity-${rec.severity}`} style={{ marginBottom: 'var(--spacing-xl)' }}>
        <div className="card-header" style={{ marginBottom: 'var(--spacing-sm)' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--spacing-sm)' }}>
            <span className="tier-badge tier-4-badge">চতুর্থ স্তর: কার্যকর পরামর্শ (Tier 4)</span>
            <span style={{ fontSize: 'var(--font-size-caption)', color: 'var(--color-text-muted)' }}>
              বিধি নং: <strong>{rec.rule_id}</strong>
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
                {rec.confidence.tier_bn} ({Math.round(rec.confidence.score * 100)}%)
              </span>
            </div>
          )}
        </div>

        {/* Headline & Body */}
        <h2 style={{ fontSize: '1.35rem', marginBottom: 'var(--spacing-sm)', color: 'var(--primitive-neutral-900)' }}>
          {rec.headline_bn}
        </h2>
        <p style={{ fontSize: '1.05rem', lineHeight: 1.6, color: 'var(--color-text-primary)' }}>
          {rec.body_bn}
        </p>

        {/* Action Directives Checklist */}
        {rec.action_items_bn && rec.action_items_bn.length > 0 && (
          <div style={{ marginTop: 'var(--spacing-md)' }}>
            <strong style={{ fontSize: 'var(--font-size-body)', color: 'var(--primitive-neutral-900)' }}>
              করণীয় পদক্ষেপসমূহ:
            </strong>
            <ul style={{ listStyle: 'none', marginTop: 'var(--spacing-xs)', paddingLeft: 0 }}>
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
            style={{
              backgroundColor: 'rgba(255, 255, 255, 0.7)',
              border: '1px solid var(--color-border-default)',
              borderRadius: 'var(--radius-md)',
              padding: 'var(--spacing-md)',
              marginTop: 'var(--spacing-md)',
              fontSize: 'var(--font-size-caption)',
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginBottom: 4, fontWeight: 600 }}>
              <Sparkles size={16} color="var(--primitive-green-800)" />
              <span>বৈজ্ঞানিক ও অর্থনৈতিক বিশ্লেষণ:</span>
            </div>
            <p style={{ margin: 0, color: 'var(--color-text-secondary)' }}>
              {rec.rationale_breakdown.scientific_basis}
            </p>
            {rec.rationale_breakdown.pumping_savings_est_bdt && (
              <p style={{ margin: '4px 0 0', fontWeight: 600, color: 'var(--primitive-green-800)' }}>
                সম্ভাব্য জ্বালানি ও সেচ খরচ সাশ্রয়: {rec.rationale_breakdown.pumping_savings_est_bdt}
              </p>
            )}
          </div>
        )}

        {/* Mandatory Field Inspection Disclaimer (AGENTS.md) */}
        <div className="field-verification-box">
          <ShieldCheck size={18} color="var(--primitive-slate-700)" style={{ flexShrink: 0 }} />
          <span>
            <strong>মাঠ যাচাইয়ের বাধ্যবাধকতা:</strong> {rec.mandatory_disclaimer_bn}
          </span>
        </div>
      </div>

      {/* 3-Tier Supporting Foundation Accordion / Cards (DEC-08) */}
      <div style={{ marginBottom: 'var(--spacing-xl)' }}>
        <h3 style={{ fontSize: 'var(--font-size-h2)', marginBottom: 'var(--spacing-md)', display: 'flex', alignItems: 'center', gap: 8 }}>
          <Layers size={20} color="var(--color-brand-primary)" />
          <span>পরামর্শের ৩-স্তর ভিত্তি ও প্রমাণ বিশ্লেষণ (DEC-08)</span>
        </h3>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: 'var(--spacing-md)' }}>
          {/* Tier 1 Card: Sensor Observations */}
          <div className="card tier-card tier-1">
            <span className="tier-badge tier-1-badge">১ম স্তর: প্রত্যক্ষ পর্যবেক্ষণ (Tier 1)</span>
            <p style={{ fontSize: 'var(--font-size-body)', marginBottom: 'var(--spacing-sm)' }}>
              {advisory.tier_1_observations.summary_bn}
            </p>
            <div style={{ fontSize: 'var(--font-size-caption)', color: 'var(--color-text-muted)' }}>
              <span>উৎস: NASA POWER / বিএমডি রাডার ও বৃষ্টিমাপক</span>
              {advisory.tier_1_observations.rainfall_7d_total_mm !== undefined && (
                <div>বিগত ৭ দিনের মোট বৃষ্টি: <strong>{advisory.tier_1_observations.rainfall_7d_total_mm} মিমি</strong></div>
              )}
            </div>
          </div>

          {/* Tier 2 Card: Derived Physical Indicators */}
          <div className="card tier-card tier-2">
            <span className="tier-badge tier-2-badge">২য় স্তর: হিসাবকৃত সূচক (Tier 2)</span>
            <p style={{ fontSize: 'var(--font-size-body)', marginBottom: 'var(--spacing-sm)' }}>
              {advisory.tier_2_indicators.summary_bn}
            </p>
            <div style={{ fontSize: 'var(--font-size-caption)', color: 'var(--color-text-muted)' }}>
              <span>পদ্ধতি: FAO-56 পেনম্যান-মন্টিথ $ET_0$ ও মাটির আর্দ্রতা ঘাটতি ($D_t$)</span>
              {advisory.tier_2_indicators.soil_water_deficit_dt_mm !== undefined && (
                <div>বর্তমান ঘাটতি ($D_t$): <strong>{advisory.tier_2_indicators.soil_water_deficit_dt_mm} মিমি</strong></div>
              )}
            </div>
          </div>

          {/* Tier 3 Card: Probabilistic Forecasts */}
          <div className="card tier-card tier-3">
            <span className="tier-badge tier-3-badge">৩য় স্তর: আবহাওয়া পূর্বাভাস (Tier 3)</span>
            <p style={{ fontSize: 'var(--font-size-body)', marginBottom: 'var(--spacing-sm)' }}>
              {advisory.tier_3_predictions.summary_bn}
            </p>
            <div style={{ fontSize: 'var(--font-size-caption)', color: 'var(--color-text-muted)' }}>
              <span>মডেল: ECMWF IFS / NOAA GFS এনসেম্বল</span>
              {advisory.tier_3_predictions.rain_probability_48h_pct !== undefined && (
                <div>বৃষ্টির সম্ভাবনা (৪৮ ঘণ্টা): <strong>{advisory.tier_3_predictions.rain_probability_48h_pct}%</strong></div>
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
              <span>পরিবেশগত চরম ঝুঁকি মূল্যায়ন (Physical Hazard Evaluation)</span>
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
              সামগ্রিক ঝুঁকি: {risk.overall_hazard_tier_bn}
            </span>
          </div>

          <div className="metric-grid">
            {risk.hazard_assessments.map((hazard, i) => (
              <div key={i} className="metric-pill">
                <span className="metric-label">{hazard.hazard_tier_bn}</span>
                <span className="metric-value">
                  {hazard.primary_metric_name === 'soil_water_deficit_dt_mm'
                    ? `${hazard.primary_metric_value} মিমি`
                    : hazard.primary_metric_name === 'haor_flood_index_iflood'
                    ? `${hazard.primary_metric_value}`
                    : `${hazard.primary_metric_value}° সে.`}
                </span>
                <span className="metric-sub">
                  নির্ণায়ক: {hazard.primary_metric_name} (সীমা: {hazard.threshold_applied})
                </span>
                <span style={{ marginTop: 6, fontSize: '0.75rem', fontWeight: 600, color: hazard.action_warranted ? 'var(--primitive-red-700)' : 'var(--primitive-green-700)' }}>
                  {hazard.action_warranted ? '• প্রতিরোধমূলক ব্যবস্থা প্রয়োজন' : '• সহনীয় সীমার মধ্যে'}
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
