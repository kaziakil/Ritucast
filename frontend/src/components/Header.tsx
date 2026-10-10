import React, { useState, useEffect, useRef } from 'react'
import {
  Sprout,
  AlertTriangle,
  CloudSun,
  Droplets,
  Waves,
  FileText,
  Compass,
  Monitor,
  Sun,
  Moon,
  Menu,
  X,
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
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false)
  const headerRef = useRef<HTMLElement>(null)

  const isReady = readiness?.status === 'ready' && readiness?.data_store_ready

  const navItems = [
    { id: 'advisories', label: t('nav_advisories'), icon: Compass },
    { id: 'weather', label: t('nav_weather'), icon: CloudSun },
    { id: 'water-balance', label: t('nav_water_balance'), icon: Droplets },
    { id: 'flood', label: t('nav_flood'), icon: Waves },
    { id: 'provenance', label: t('nav_provenance'), icon: FileText },
  ]

  // Close mobile menu on Escape key press
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && isMobileMenuOpen) {
        setIsMobileMenuOpen(false)
      }
    }
    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [isMobileMenuOpen])

  // Close mobile menu when viewport expands to desktop
  useEffect(() => {
    const handleResize = () => {
      if (window.innerWidth >= 1024 && isMobileMenuOpen) {
        setIsMobileMenuOpen(false)
      }
    }
    window.addEventListener('resize', handleResize)
    return () => window.removeEventListener('resize', handleResize)
  }, [isMobileMenuOpen])

  // Close mobile menu when clicking outside header
  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (
        isMobileMenuOpen &&
        headerRef.current &&
        !headerRef.current.contains(e.target as Node)
      ) {
        setIsMobileMenuOpen(false)
      }
    }
    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [isMobileMenuOpen])

  const handleNavClick = (tabId: string) => {
    setActiveTab(tabId)
    setIsMobileMenuOpen(false)
  }

  return (
    <header className="app-header" ref={headerRef}>
      <div className="header-container">
        <div className="header-inner">
          {/* 1. Brand Logo & Title */}
          <div
            className="brand-logo"
            onClick={() => handleNavClick('advisories')}
            onKeyDown={(e) => {
              if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault()
                handleNavClick('advisories')
              }
            }}
            role="button"
            tabIndex={0}
            aria-label={t('home_aria_label')}
          >
            <div className="brand-icon-box" aria-hidden="true">
              <Sprout size={20} className="brand-sprout-icon" />
            </div>
            <div className="brand-text-group">
              <span className="brand-title">
                {language === 'bn' ? 'ঋতুকাস্ট' : 'Ritucast'}
              </span>
              <span className="brand-subtitle">
                {language === 'bn' ? 'Ritucast' : 'ঋতুকাস্ট'}
              </span>
            </div>
          </div>

          {/* 2. Desktop Navigation Items (Single Line, Never Wrapping) */}
          <nav className="desktop-nav" aria-label="Main Navigation">
            <ul className="nav-links">
              {navItems.map((item) => {
                const Icon = item.icon
                const isActive = activeTab === item.id
                return (
                  <li key={item.id}>
                    <button
                      type="button"
                      className={`nav-link ${isActive ? 'active' : ''}`}
                      onClick={() => handleNavClick(item.id)}
                      aria-current={isActive ? 'page' : undefined}
                    >
                      <Icon size={16} className="nav-icon" aria-hidden="true" />
                      <span className="nav-label">{item.label}</span>
                    </button>
                  </li>
                )
              })}
            </ul>
          </nav>

          {/* 3. Header Action Controls: Language, Theme, Status & Mobile Toggle */}
          <div className="header-actions">
            {/* Language Switcher (Bangla / English) */}
            <div
              className="segmented-control lang-control"
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
              className="segmented-control theme-control"
              role="radiogroup"
              aria-label={t('theme_label')}
            >
              <button
                type="button"
                role="radio"
                aria-checked={theme === 'system'}
                className={`segmented-btn icon-btn ${theme === 'system' ? 'active' : ''}`}
                onClick={() => setTheme('system')}
                title={`${t('theme_system')} (${theme === 'system' ? 'Active' : ''})`}
                aria-label={t('theme_system')}
              >
                <Monitor size={14} aria-hidden="true" />
              </button>
              <button
                type="button"
                role="radio"
                aria-checked={theme === 'light'}
                className={`segmented-btn icon-btn ${theme === 'light' ? 'active' : ''}`}
                onClick={() => setTheme('light')}
                title={`${t('theme_light')} (${theme === 'light' ? 'Active' : ''})`}
                aria-label={t('theme_light')}
              >
                <Sun size={14} aria-hidden="true" />
              </button>
              <button
                type="button"
                role="radio"
                aria-checked={theme === 'dark'}
                className={`segmented-btn icon-btn ${theme === 'dark' ? 'active' : ''}`}
                onClick={() => setTheme('dark')}
                title={`${t('theme_dark')} (${theme === 'dark' ? 'Active' : ''})`}
                aria-label={t('theme_dark')}
              >
                <Moon size={14} aria-hidden="true" />
              </button>
            </div>

            {/* Live Readiness Pill (Subtle & Compact) */}
            <div className="status-badge-container">
              {loadingReadiness ? (
                <span className="status-badge checking">
                  <span className="status-dot checking-dot" aria-hidden="true" />
                  <span className="status-badge-text">{t('status_checking')}</span>
                </span>
              ) : isReady ? (
                <span className="status-badge live" title={t('status_live_title')}>
                  <span className="status-pulse-wrapper" aria-hidden="true">
                    <span className="status-ping" />
                    <span className="status-dot live-dot" />
                  </span>
                  <span className="status-badge-text">{t('status_live')}</span>
                </span>
              ) : (
                <span className="status-badge unready" title={t('status_degraded_title')}>
                  <AlertTriangle size={13} aria-hidden="true" />
                  <span className="status-badge-text">{t('status_degraded')}</span>
                </span>
              )}
            </div>

            {/* Mobile Menu Toggle Button */}
            <button
              type="button"
              className="mobile-menu-btn"
              onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
              aria-expanded={isMobileMenuOpen}
              aria-controls="mobile-nav-panel"
              aria-label={isMobileMenuOpen ? t('nav_menu_close') : t('nav_menu_open')}
            >
              {isMobileMenuOpen ? (
                <X size={20} aria-hidden="true" />
              ) : (
                <Menu size={20} aria-hidden="true" />
              )}
            </button>
          </div>
        </div>

        {/* 4. Progressive Mobile & Tablet Navigation Drawer */}
        {isMobileMenuOpen && (
          <div
            id="mobile-nav-panel"
            className="mobile-nav-panel"
            role="region"
            aria-label="Mobile Navigation"
          >
            <nav>
              <ul className="mobile-nav-links">
                {navItems.map((item) => {
                  const Icon = item.icon
                  const isActive = activeTab === item.id
                  return (
                    <li key={item.id}>
                      <button
                        type="button"
                        className={`mobile-nav-link ${isActive ? 'active' : ''}`}
                        onClick={() => handleNavClick(item.id)}
                        aria-current={isActive ? 'page' : undefined}
                      >
                        <div className="mobile-nav-icon-wrap" aria-hidden="true">
                          <Icon size={18} />
                        </div>
                        <span className="mobile-nav-text">{item.label}</span>
                        {isActive && <span className="mobile-active-pill" />}
                      </button>
                    </li>
                  )
                })}
              </ul>
            </nav>

            <div className="mobile-drawer-footer">
              <div className="mobile-status-summary">
                {isReady ? (
                  <span className="status-badge live">
                    <span className="status-pulse-wrapper" aria-hidden="true">
                      <span className="status-ping" />
                      <span className="status-dot live-dot" />
                    </span>
                    <span>{t('status_live')}</span>
                  </span>
                ) : (
                  <span className="status-badge unready">
                    <AlertTriangle size={13} aria-hidden="true" />
                    <span>{t('status_degraded')}</span>
                  </span>
                )}
              </div>
            </div>
          </div>
        )}
      </div>
    </header>
  )
}

export default Header
