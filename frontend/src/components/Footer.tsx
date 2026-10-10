import React from 'react'
import { Sprout, ShieldAlert } from 'lucide-react'

export const Footer: React.FC = () => {
  return (
    <footer className="app-footer">
      <div className="app-container">
        <div className="footer-inner">
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: 6, fontWeight: 700, color: 'var(--color-brand-primary)', marginBottom: 4 }}>
              <Sprout size={18} />
              <span>ঋতুকাস্ট (Ritucast) • বাংলাদেশ কৃষি আবহাওয়া প্ল্যাটফর্ম</span>
            </div>
            <p style={{ margin: 0, fontSize: '0.8rem', color: 'var(--color-text-muted)' }}>
              উপগ্রহ পর্যবেক্ষণ, সংখ্যাসূচক আবহাওয়া পূর্বাভাস ও মৃত্তিকা আর্দ্রতা মডেলের সমন্বয়।
            </p>
          </div>

          <div style={{ textAlign: 'right', fontSize: '0.8rem' }}>
            <p style={{ margin: 0, color: 'var(--color-text-secondary)' }}>
              সহযোগী সংস্থা: <strong>কৃষি সম্প্রসারণ অধিদপ্তর (DAE) • বিআরআরআই (BRRI) • বিএমডি (BMD)</strong>
            </p>
            <p style={{ margin: '4px 0 0', color: 'var(--color-text-muted)' }}>
              সংস্করণ: <strong>১.০.০ (ফেজ ১১ ফ্রন্টএন্ড কোর)</strong> • লাইসেন্স: ওপেন অ্যাক্সেস
            </p>
          </div>
        </div>

        <div
          style={{
            marginTop: 'var(--spacing-lg)',
            paddingTop: 'var(--spacing-md)',
            borderTop: '1px solid var(--color-border-default)',
            fontSize: '0.75rem',
            color: 'var(--color-text-muted)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            gap: 6,
          }}
        >
          <ShieldAlert size={14} color="var(--primitive-slate-500)" />
          <span>
            সতর্কতা: ঋতুকাস্ট একটি বৈজ্ঞানিক সিদ্ধান্ত সহায়তা ব্যবস্থা। মাঠে যেকোনো চূড়ান্ত পদক্ষেপ নেওয়ার পূর্বে আইল ও মাটির রস সরাসরি পরীক্ষা করুন।
          </span>
        </div>
      </div>
    </footer>
  )
}
