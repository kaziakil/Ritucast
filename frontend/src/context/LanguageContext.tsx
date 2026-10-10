import React, { createContext, useContext, useState, useEffect, useMemo, useCallback } from 'react'
import { translations, type Language, type TranslationDictionary } from '../i18n/translations'

interface LanguageContextType {
  language: Language
  setLanguage: (lang: Language) => void
  t: (key: keyof TranslationDictionary) => string
}

const STORAGE_KEY = 'ritucast_lang'

const LanguageContext = createContext<LanguageContextType | undefined>(undefined)

export const LanguageProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [language, setLanguageState] = useState<Language>(() => {
    try {
      const stored = localStorage.getItem(STORAGE_KEY)
      if (stored === 'bn' || stored === 'en') {
        return stored
      }
    } catch {
      // Ignore storage errors in restricted contexts
    }
    return 'bn'
  })

  const setLanguage = useCallback((lang: Language) => {
    setLanguageState(lang)
    try {
      localStorage.setItem(STORAGE_KEY, lang)
    } catch {
      // Ignore storage errors
    }
  }, [])

  useEffect(() => {
    document.documentElement.setAttribute('lang', language)
  }, [language])

  const t = useCallback(
    (key: keyof TranslationDictionary): string => {
      const dict = translations[language] || translations.bn
      return dict[key] || translations.bn[key] || String(key)
    },
    [language]
  )

  const value = useMemo(
    () => ({
      language,
      setLanguage,
      t,
    }),
    [language, setLanguage, t]
  )

  return <LanguageContext.Provider value={value}>{children}</LanguageContext.Provider>
}

export const useLanguage = (): LanguageContextType => {
  const context = useContext(LanguageContext)
  if (!context) {
    // Resilient fallback for isolated component testing
    return {
      language: 'bn',
      setLanguage: () => {},
      t: (key: keyof TranslationDictionary) => translations.bn[key] || String(key),
    }
  }
  return context
}
