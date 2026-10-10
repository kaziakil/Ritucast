import React from 'react'
import { Sprout, ShieldAlert } from 'lucide-react'
import { useLanguage } from '../context/LanguageContext'

export const Footer: React.FC = () => {
  const { t } = useLanguage()

  return (
    <footer className="app-footer">
      <div className="app-container">
        <div className="footer-inner">
          <div>
            <div
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: 6,
                fontWeight: 700,
                color: 'var(--color-brand-primary)',
                marginBottom: 4,
              }}
            >
              <Sprout size={18} />
              <span>{t('footer_platform_desc')}</span>
            </div>
            <p style={{ margin: 0, fontSize: '0.8rem', color: 'var(--color-text-muted)' }}>
              {t('footer_sub')}
            </p>
          </div>

          <div style={{ textAlign: 'right', fontSize: '0.8rem' }}>
            <p style={{ margin: 0, color: 'var(--color-text-secondary)' }}>
              {t('footer_partners')}
            </p>
            <p style={{ margin: '4px 0 0', color: 'var(--color-text-muted)' }}>
              {t('footer_version')}
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
          <span>{t('footer_disclaimer')}</span>
        </div>
      </div>
    </footer>
  )
}
export default Footer
