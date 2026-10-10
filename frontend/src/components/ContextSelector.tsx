import React from 'react'
import { MapPin, Wheat, Calendar, RefreshCw, AlertCircle } from 'lucide-react'
import type { UpazilaSummary, CropInfo } from '../types/api'

interface ContextSelectorProps {
  upazilas: UpazilaSummary[]
  selectedUpazilaId: string
  setSelectedUpazilaId: (id: string) => void
  crops: CropInfo[]
  selectedCropId: string
  setSelectedCropId: (id: string) => void
  growthStages: string[]
  selectedStage: string
  setSelectedStage: (stage: string) => void
  onRefresh: () => void
  loading: boolean
}

const STAGE_LABELS_BN: Record<string, string> = {
  Tillering: 'কুশি পর্যায় (বৃদ্ধি)',
  Booting: 'থোর পর্যায় (গর্ভকাল)',
  Flowering: 'ফুল ফোটা পর্যায় (পরাগায়ন)',
  Dough: 'দুধ/দানা গঠন পর্যায়',
  Maturity: 'পাকা পর্যায় (কর্তন)',
}

export const ContextSelector: React.FC<ContextSelectorProps> = ({
  upazilas,
  selectedUpazilaId,
  setSelectedUpazilaId,
  crops,
  selectedCropId,
  setSelectedCropId,
  growthStages,
  selectedStage,
  setSelectedStage,
  onRefresh,
  loading,
}) => {
  const currentUpazila = upazilas.find((u) => u.upazila_id === selectedUpazilaId)

  return (
    <section
      aria-label="Context Selection"
      style={{
        backgroundColor: 'var(--color-bg-surface)',
        borderBottom: '1px solid var(--color-border-default)',
        padding: 'var(--spacing-lg) 0',
        boxShadow: 'var(--shadow-sm)',
        marginBottom: 'var(--spacing-xl)',
      }}
    >
      <div className="app-container">
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr)) auto',
            gap: 'var(--spacing-md)',
            alignItems: 'flex-end',
          }}
        >
          {/* Upazila Selector */}
          <div className="form-group" style={{ marginBottom: 0 }}>
            <label className="form-label" htmlFor="upazila-select">
              <MapPin size={14} style={{ display: 'inline', marginRight: 4, verticalAlign: 'middle' }} />
              উপজেলা (পাইলট অঞ্চল):
            </label>
            <select
              id="upazila-select"
              className="form-select"
              value={selectedUpazilaId}
              onChange={(e) => setSelectedUpazilaId(e.target.value)}
            >
              {upazilas.map((u) => (
                <option key={u.upazila_id} value={u.upazila_id}>
                  {u.name_bn} ({u.name_en}) — {u.district_name} ({u.aez_code === 26 ? 'বরেন্দ্র' : 'হাওড়'})
                </option>
              ))}
            </select>
          </div>

          {/* Crop Selector */}
          <div className="form-group" style={{ marginBottom: 0 }}>
            <label className="form-label" htmlFor="crop-select">
              <Wheat size={14} style={{ display: 'inline', marginRight: 4, verticalAlign: 'middle' }} />
              ফসল (ক্যালিব্রেটেড):
            </label>
            <select
              id="crop-select"
              className="form-select"
              value={selectedCropId}
              onChange={(e) => setSelectedCropId(e.target.value)}
            >
              {crops.map((c) => (
                <option key={c.crop_id} value={c.crop_id}>
                  {c.name_bn} ({c.name_en})
                </option>
              ))}
            </select>
          </div>

          {/* Phenological Stage Selector */}
          <div className="form-group" style={{ marginBottom: 0 }}>
            <label className="form-label" htmlFor="stage-select">
              <Calendar size={14} style={{ display: 'inline', marginRight: 4, verticalAlign: 'middle' }} />
              ফসলের বৃদ্ধির বর্তমান পর্যায় (DEC-17):
            </label>
            <select
              id="stage-select"
              className="form-select"
              value={selectedStage}
              onChange={(e) => setSelectedStage(e.target.value)}
            >
              {growthStages.map((stage) => (
                <option key={stage} value={stage}>
                  {STAGE_LABELS_BN[stage] || stage}
                </option>
              ))}
            </select>
          </div>

          {/* Refresh Action */}
          <div style={{ marginBottom: 0 }}>
            <button
              className="btn btn-primary"
              onClick={onRefresh}
              disabled={loading}
              aria-busy={loading}
              style={{ width: '100%', minWidth: '160px' }}
              aria-label="হালনাগাদ তথ্য আনুন"
            >
              <RefreshCw size={16} className={loading ? 'animate-spin' : ''} />
              <span>{loading ? 'লোড হচ্ছে...' : 'বিশ্লেষণ হালনাগাদ'}</span>
            </button>
          </div>
        </div>

        {/* Selected Zone Pill and Contextual Status */}
        <div
          aria-live="polite"
          style={{
            marginTop: 'var(--spacing-md)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            flexWrap: 'wrap',
            gap: 'var(--spacing-sm)',
            fontSize: 'var(--font-size-caption)',
            color: 'var(--color-text-secondary)',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--spacing-sm)' }}>
            <span style={{ fontWeight: 600 }}>বর্তমান অঞ্চল:</span>
            <span
              style={{
                backgroundColor: currentUpazila?.aez_code === 26 ? 'var(--primitive-amber-100)' : 'var(--primitive-sky-100)',
                color: currentUpazila?.aez_code === 26 ? 'var(--primitive-amber-900)' : 'var(--primitive-sky-900)',
                padding: '2px 8px',
                borderRadius: 'var(--radius-sm)',
                fontWeight: 600,
              }}
            >
              {currentUpazila?.aez_name} (AEZ-{currentUpazila?.aez_code})
            </span>
            <span>• মূল প্রাকৃতিক ঝুঁকি: <strong>{currentUpazila?.primary_risk === 'FLASH_FLOOD' ? 'আকস্মিক বন্যা' : 'ভূগর্ভস্থ পানির ঘাটতি ও খরা'}</strong></span>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: 4, color: 'var(--primitive-green-800)' }}>
            <AlertCircle size={14} />
            <span>প্রসঙ্গ-ভিত্তিক যাচাই (DEC-17): সক্রিয় ও সম্পূর্ণ</span>
          </div>
        </div>
      </div>
    </section>
  )
}
