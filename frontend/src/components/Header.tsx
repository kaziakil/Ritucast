import React from 'react'
import {
  Sprout,
  CheckCircle2,
  AlertTriangle,
  CloudSun,
  Droplets,
  Waves,
  FileText,
  Compass,
  Monitor,
  Sun,
  Moon,
} from 'lucide-react'
import type { ReadinessResponse } from '../types/api'
import { useLanguage } from '../context/LanguageContext'
import { useTheme } from '../context/ThemeContext'

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
  const { language, setLanguage, t } = useLanguage()
  const { theme, setTheme } = useTheme()
  const isReady = readiness?.status === 'ready' && readiness?.data_store_ready

  return (
    <header className="app-header">
      <div className="app-container">
        <div className="header-inner">
          {/* Brand Logo & Title */}
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
            aria-label={t('home_aria_label')}
          >
            <Sprout size={28} color="var(--color-brand-primary)" />
            <span>
              {language === 'bn' ? (
                <>
                  ঋতুকাস্ট{' '}
                  <span style={{ fontSize: '0.9rem', color: 'var(--color-text-muted)', fontWeight: 500 }}>
                    Ritucast
                  </span>
                </>
              ) : (
                <>
                  Ritucast{' '}
                  <span style={{ fontSize: '0.9rem', color: 'var(--color-text-muted)', fontWeight: 500 }}>
                    ঋতুকাস্ট
                  </span>
                </>
              )}
            </span>
          </div>

          {/* Navigation Links */}
          <nav aria-label="Main Navigation">
            <ul className="nav-links">
              <li>
                <button
                  className={`nav-link ${activeTab === 'advisories' ? 'active' : ''}`}
                  onClick={() => setActiveTab('advisories')}
                  aria-current={activeTab === 'advisories' ? 'page' : undefined}
                >
                  <Compass size={18} />
                  <span>{t('nav_advisories')}</span>
                </button>
              </li>
              <li>
                <button
                  className={`nav-link ${activeTab === 'weather' ? 'active' : ''}`}
                  onClick={() => setActiveTab('weather')}
                  aria-current={activeTab === 'weather' ? 'page' : undefined}
                >
                  <CloudSun size={18} />
                  <span>{t('nav_weather')}</span>
                </button>
              </li>
              <li>
                <button
                  className={`nav-link ${activeTab === 'water-balance' ? 'active' : ''}`}
                  onClick={() => setActiveTab('water-balance')}
                  aria-current={activeTab === 'water-balance' ? 'page' : undefined}
                >
                  <Droplets size={18} />
                  <span>{t('nav_water_balance')}</span>
                </button>
              </li>
              <li>
                <button
                  className={`nav-link ${activeTab === 'flood' ? 'active' : ''}`}
                  onClick={() => setActiveTab('flood')}
                  aria-current={activeTab === 'flood' ? 'page' : undefined}
                >
                  <Waves size={18} />
                  <span>{t('nav_flood')}</span>
                </button>
              </li>
              <li>
                <button
                  className={`nav-link ${activeTab === 'provenance' ? 'active' : ''}`}
                  onClick={() => setActiveTab('provenance')}
                  aria-current={activeTab === 'provenance' ? 'page' : undefined}
                >
                  <FileText size={18} />
                  <span>{t('nav_provenance')}</span>
                </button>
              </li>
            </ul>
          </nav>

          {/* Header Action Bar: Language Toggle, Theme Toggle & Status Badge */}
          <div className="header-actions">
            {/* Language Switcher (Bangla / English) */}
            <div
              className="segmented-control"
              role="radiogroup"
              aria-label={t('lang_label')}
            >
              <button
                type="button"
                role="radio"
                aria-checked={language === 'bn'}
                className={`segmented-btn ${language === 'bn' ? 'active' : ''}`}
                onClick={() => setLanguage('bn')}
                title="বাংলা (Bangla)"
                aria-label="বাংলা"
              >
                বাং
              </button>
              <button
                type="button"
                role="radio"
                aria-checked={language === 'en'}
                className={`segmented-btn ${language === 'en' ? 'active' : ''}`}
                onClick={() => setLanguage('en')}
                title="English"
                aria-label="English"
              >
                EN
              </button>
            </div>

            {/* Theme Toggle (System / Light / Dark) */}
            <div
              className="segmented-control"
              role="radiogroup"
              aria-label={t('theme_label')}
            >
              <button
                type="button"
                role="radio"
                aria-checked={theme === 'system'}
                className={`segmented-btn ${theme === 'system' ? 'active' : ''}`}
                onClick={() => setTheme('system')}
                title={`${t('theme_system')} (${theme === 'system' ? 'Active' : ''})`}
                aria-label={t('theme_system')}
              >
                <Monitor size={15} />
              </button>
              <button
                type="button"
                role="radio"
                aria-checked={theme === 'light'}
                className={`segmented-btn ${theme === 'light' ? 'active' : ''}`}
                onClick={() => setTheme('light')}
                title={`${t('theme_light')} (${theme === 'light' ? 'Active' : ''})`}
                aria-label={t('theme_light')}
              >
                <Sun size={15} />
              </button>
              <button
                type="button"
                role="radio"
                aria-checked={theme === 'dark'}
                className={`segmented-btn ${theme === 'dark' ? 'active' : ''}`}
                onClick={() => setTheme('dark')}
                title={`${t('theme_dark')} (${theme === 'dark' ? 'Active' : ''})`}
                aria-label={t('theme_dark')}
              >
                <Moon size={15} />
              </button>
            </div>

            {/* Live Readiness Pill */}
            <div>
              {loadingReadiness ? (
                <span
                  className="status-badge"
                  style={{ backgroundColor: 'var(--color-bg-subtle)', color: 'var(--color-text-muted)' }}
                >
                  {t('status_checking')}
                </span>
              ) : isReady ? (
                <span className="status-badge live" title={t('status_live_title')}>
                  <CheckCircle2 size={14} />
                  <span>{t('status_live')}</span>
                </span>
              ) : (
                <span className="status-badge unready" title={t('status_degraded_title')}>
                  <AlertTriangle size={14} />
                  <span>{t('status_degraded')}</span>
                </span>
              )}
            </div>
          </div>
        </div>
      </div>
    </header>
  )
}
export default Header
