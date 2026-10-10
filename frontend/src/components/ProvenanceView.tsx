import React from 'react'
import { FileText, Database, BookOpen, ShieldCheck, CheckCircle2, Lock } from 'lucide-react'
import type { SystemProvenanceResponse } from '../types/api'

interface ProvenanceViewProps {
  provenance: SystemProvenanceResponse | null
  loading: boolean
  error: string | null
}

export const ProvenanceView: React.FC<ProvenanceViewProps> = ({
  provenance,
  loading,
  error,
}) => {
  if (loading) {
    return (
      <div className="card">
        <div className="skeleton" style={{ width: 280, height: 28, marginBottom: 16 }} />
        <div className="skeleton" style={{ width: '100%', height: 220 }} />
      </div>
    )
  }

  if (error) {
    return (
      <div className="error-box" role="alert" aria-live="assertive">
        <FileText size={40} style={{ margin: '0 auto 12px' }} />
        <h3 className="error-title">তথ্যসূত্র ও স্বচ্ছতা বিবরণী লোড করা যায়নি</h3>
        <p>{error}</p>
      </div>
    )
  }

  if (!provenance) {
    return null
  }

  return (
    <div>
      {/* System Overview Header */}
      <div className="card" style={{ marginBottom: 'var(--spacing-xl)' }}>
        <div className="card-header">
          <h3 className="card-title">
            <FileText size={20} color="var(--color-brand-primary)" />
            <span>সিস্টেম স্বচ্ছতা ও বৈজ্ঞানিক তথ্যসূত্র (System Provenance)</span>
          </h3>
          <span className="status-badge" style={{ backgroundColor: 'var(--primitive-green-100)', color: 'var(--primitive-green-800)' }}>
            সংস্করণ: {provenance.version}
          </span>
        </div>
        <p style={{ color: 'var(--color-text-secondary)' }}>
          ঋতুকাস্ট প্ল্যাটফর্মের প্রতিটি পর্যবেক্ষণ, হিসাবকৃত সূচক এবং পরামর্শের উৎস সম্পূর্ণ স্বচ্ছ এবং নিরীক্ষণযোগ্য। উপগ্রহ পর্যবেক্ষণ বা আবহাওয়া পূর্বাভাসের কোনো অনুমানের ক্ষেত্রে কৃত্রিম নির্ভুলতা বা ভ্রান্ত নিশ্চয়তা প্রদর্শন করা হয় না।
        </p>
        <div style={{ fontSize: 'var(--font-size-caption)', color: 'var(--color-text-muted)' }}>
          রিপোর্ট প্রস্তুতের সময়: {provenance.generated_at_bst} • পাইলট অঞ্চল: {provenance.pilot_regions.join('; ')}
        </div>
      </div>

      {/* Dataset Inventory & Freshness */}
      <div className="card" style={{ marginBottom: 'var(--spacing-xl)' }}>
        <div className="card-header">
          <h3 className="card-title">
            <Database size={20} color="var(--primitive-sky-700)" />
            <span>সংগৃহীত উপাত্তের তালিকা ও হালনাগাদ স্থিতি (Data Ingestion & Freshness)</span>
          </h3>
          <span style={{ fontSize: 'var(--font-size-caption)', color: 'var(--color-text-muted)' }}>
            সর্বোচ্চ গ্রহণযোগ্য বিলম্ব: ৩৬ ঘণ্টা (DEC-10)
          </span>
        </div>

        <div style={{ overflowX: 'auto' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: 'var(--font-size-caption)', textAlign: 'left' }}>
            <thead>
              <tr style={{ borderBottom: '2px solid var(--color-border-default)', color: 'var(--color-text-secondary)' }}>
                <th style={{ padding: '8px 12px' }}>আইডি</th>
                <th style={{ padding: '8px 12px' }}>ডেটাসেটের নাম</th>
                <th style={{ padding: '8px 12px' }}>উৎস সংস্থা</th>
                <th style={{ padding: '8px 12px' }}>আপডেট বিলম্ব</th>
                <th style={{ padding: '8px 12px' }}>লাইসেন্স</th>
                <th style={{ padding: '8px 12px' }}>স্থিতি</th>
              </tr>
            </thead>
            <tbody>
              {provenance.datasets.map((ds) => (
                <tr key={ds.dataset_id} style={{ borderBottom: '1px solid var(--color-border-default)' }}>
                  <td style={{ padding: '10px 12px', fontWeight: 600, color: 'var(--color-brand-primary)' }}>
                    {ds.dataset_id}
                  </td>
                  <td style={{ padding: '10px 12px' }}>
                    <strong>{ds.dataset_name}</strong>
                    <div style={{ color: 'var(--color-text-muted)', fontSize: '0.75rem' }}>
                      কভারেজ: {ds.spatial_coverage} • বিরতি: {ds.temporal_resolution}
                    </div>
                  </td>
                  <td style={{ padding: '10px 12px' }}>{ds.source_agency}</td>
                  <td style={{ padding: '10px 12px' }}>
                    <span style={{ fontWeight: 600, color: ds.latency_hours <= 36 ? 'var(--primitive-green-800)' : 'var(--primitive-amber-800)' }}>
                      {ds.latency_hours} ঘণ্টা
                    </span>
                  </td>
                  <td style={{ padding: '10px 12px', color: 'var(--color-text-muted)' }}>{ds.license}</td>
                  <td style={{ padding: '10px 12px' }}>
                    <span style={{ display: 'inline-flex', alignItems: 'center', gap: 4, color: 'var(--primitive-green-700)', fontWeight: 600 }}>
                      <CheckCircle2 size={12} />
                      {ds.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Scientific Methodologies & Calibrations */}
      <div className="card" style={{ marginBottom: 'var(--spacing-xl)' }}>
        <div className="card-header">
          <h3 className="card-title">
            <BookOpen size={20} color="var(--primitive-green-700)" />
            <span>বৈজ্ঞানিক সূত্র ও মডেল ক্যাটালগ (Scientific Methodologies)</span>
          </h3>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: 'var(--spacing-md)' }}>
          {provenance.scientific_methodologies.map((m) => (
            <div
              key={m.method_id}
              style={{
                border: '1px solid var(--color-border-default)',
                borderRadius: 'var(--radius-md)',
                padding: 'var(--spacing-md)',
                backgroundColor: 'var(--primitive-neutral-50)',
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 4 }}>
                <span style={{ fontWeight: 700, color: 'var(--color-brand-primary)' }}>{m.method_id}</span>
                <span style={{ fontSize: '0.75rem', color: 'var(--primitive-green-800)', fontWeight: 600 }}>
                  {m.calibration_status}
                </span>
              </div>
              <h4 style={{ fontSize: '0.95rem', marginBottom: 4, color: 'var(--primitive-neutral-900)' }}>
                {m.title}
              </h4>
              <p style={{ margin: 0, fontSize: '0.75rem', color: 'var(--color-text-muted)' }}>
                রেফারেন্স মানদণ্ড: {m.reference_standard}
              </p>
            </div>
          ))}
        </div>
      </div>

      {/* Scope Boundaries & Non-Goals (DEC-06) */}
      <div className="card" style={{ backgroundColor: 'var(--primitive-slate-50)', borderLeft: '4px solid var(--primitive-slate-800)' }}>
        <div className="card-header">
          <h3 className="card-title">
            <Lock size={20} color="var(--primitive-slate-800)" />
            <span>সিস্টেমের পরিধি ও সুস্পষ্ট অ-লক্ষ্যসমূহ (DEC-06 Non-Goals)</span>
          </h3>
        </div>
        <p style={{ fontSize: 'var(--font-size-caption)', color: 'var(--color-text-secondary)', marginBottom: 'var(--spacing-md)' }}>
          কৃষকদের নিরাপত্তা এবং বৈজ্ঞানিক বস্তুনিষ্ঠতা বজায় রাখতে নিম্নলিখিত কার্যাবলি ঋতুকাস্টের পরিধির বাইরে রাখা হয়েছে:
        </p>

        <ul style={{ listStyle: 'none', paddingLeft: 0, fontSize: 'var(--font-size-caption)' }}>
          <li style={{ marginBottom: 8, display: 'flex', alignItems: 'flex-start', gap: 8 }}>
            <ShieldCheck size={16} color="var(--primitive-slate-700)" style={{ flexShrink: 0, marginTop: 2 }} />
            <span><strong>প্লট-ভিত্তিক ফলন পূর্বাভাস নয়:</strong> উপগ্রহ রিমোট সেন্সিংয়ের সীমাবদ্ধতার কারণে শতভাগ নিশ্চয়তাসহ ব্যক্তিবিশেষের জমির ফলন অনুমান করা হয় না।</span>
          </li>
          <li style={{ marginBottom: 8, display: 'flex', alignItems: 'flex-start', gap: 8 }}>
            <ShieldCheck size={16} color="var(--primitive-slate-700)" style={{ flexShrink: 0, marginTop: 2 }} />
            <span><strong>কীটনাশকের স্বয়ংক্রিয় প্রেসক্রিপশন নয়:</strong> উপগ্রহের মাধ্যমে রোগ নির্ণয় করে স্বয়ংক্রিয় রাসায়নিক বা কীটনাশক ব্যবহারের নির্দেশ দেওয়া হয় না।</span>
          </li>
          <li style={{ display: 'flex', alignItems: 'flex-start', gap: 8 }}>
            <ShieldCheck size={16} color="var(--primitive-slate-700)" style={{ flexShrink: 0, marginTop: 2 }} />
            <span><strong>সরাসরি পাম্প নিয়ন্ত্রণ নয়:</strong> প্ল্যাটফর্মটি সিদ্ধান্ত সহায়তা প্রদান করে; নলকূপের মোটরের সাথে কোনো হার্ডওয়্যার সংযুক্ত নয়।</span>
          </li>
        </ul>
      </div>
    </div>
  )
}
