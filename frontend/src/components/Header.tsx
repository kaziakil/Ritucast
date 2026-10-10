import React from 'react'
import { Sprout, CheckCircle2, AlertTriangle, CloudSun, Droplets, Waves, FileText, Compass } from 'lucide-react'
import type { ReadinessResponse } from '../types/api'

interface HeaderProps {
  activeTab: string
  setActiveTab: (tab: string) => void
  readiness: ReadinessResponse | null
  loadingReadiness: boolean
}

export const Header: React.FC<HeaderProps> = ({
  activeTab,
  setActiveTab,
  readiness,
  loadingReadiness,
}) => {
  const isReady = readiness?.status === 'ready' && readiness?.data_store_ready

  return (
    <header className="app-header">
      <div className="app-container">
        <div className="header-inner">
          <div
            className="brand-logo"
            onClick={() => setActiveTab('advisories')}
            onKeyDown={(e) => {
              if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault()
                setActiveTab('advisories')
              }
            }}
            role="button"
            tabIndex={0}
            aria-label="ঋতুকাস্ট হোমপেইজে যান"
          >
            <Sprout size={28} color="var(--primitive-green-700)" />
            <span>ঋতুকাস্ট <span style={{ fontSize: '0.9rem', color: 'var(--color-text-muted)', fontWeight: 500 }}>Ritucast</span></span>
          </div>

          <nav aria-label="Main Navigation">
            <ul className="nav-links">
              <li>
                <button
                  className={`nav-link ${activeTab === 'advisories' ? 'active' : ''}`}
                  onClick={() => setActiveTab('advisories')}
                  aria-current={activeTab === 'advisories' ? 'page' : undefined}
                >
                  <Compass size={18} />
                  <span>পরামর্শ কেন্দ্র</span>
                </button>
              </li>
              <li>
                <button
                  className={`nav-link ${activeTab === 'weather' ? 'active' : ''}`}
                  onClick={() => setActiveTab('weather')}
                  aria-current={activeTab === 'weather' ? 'page' : undefined}
                >
                  <CloudSun size={18} />
                  <span>আবহাওয়া</span>
                </button>
              </li>
              <li>
                <button
                  className={`nav-link ${activeTab === 'water-balance' ? 'active' : ''}`}
                  onClick={() => setActiveTab('water-balance')}
                  aria-current={activeTab === 'water-balance' ? 'page' : undefined}
                >
                  <Droplets size={18} />
                  <span>মাটির আর্দ্রতা (AWD)</span>
                </button>
              </li>
              <li>
                <button
                  className={`nav-link ${activeTab === 'flood' ? 'active' : ''}`}
                  onClick={() => setActiveTab('flood')}
                  aria-current={activeTab === 'flood' ? 'page' : undefined}
                >
                  <Waves size={18} />
                  <span>হাওড় বন্যা ঝুঁকি</span>
                </button>
              </li>
              <li>
                <button
                  className={`nav-link ${activeTab === 'provenance' ? 'active' : ''}`}
                  onClick={() => setActiveTab('provenance')}
                  aria-current={activeTab === 'provenance' ? 'page' : undefined}
                >
                  <FileText size={18} />
                  <span>স্বচ্ছতা ও তথ্যসূত্র</span>
                </button>
              </li>
            </ul>
          </nav>

          <div style={{ display: 'flex', alignItems: 'center' }}>
            {loadingReadiness ? (
              <span className="status-badge" style={{ backgroundColor: 'var(--primitive-slate-100)' }}>
                যাচাই হচ্ছে...
              </span>
            ) : isReady ? (
              <span className="status-badge live" title="সবগুলো ডেটাসেট ও অ্যানালিটিক্স সচল রয়েছে">
                <CheckCircle2 size={14} />
                <span>সচল (লাইভ)</span>
              </span>
            ) : (
              <span className="status-badge unready" title="কিছু নির্ভরতা অনুপস্থিত">
                <AlertTriangle size={14} />
                <span>সীমাবদ্ধ</span>
              </span>
            )}
          </div>
        </div>
      </div>
    </header>
  )
}
