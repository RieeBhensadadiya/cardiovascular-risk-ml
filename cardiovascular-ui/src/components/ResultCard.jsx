import { useEffect, useRef } from 'react'
import styles from './ResultCard.module.css'
import { CheckCircle2, AlertTriangle, Info, Activity, ShieldCheck } from 'lucide-react'

const defaultTips = {
  positive: [
    'Schedule a cardiologist consultation immediately.',
    'Monitor blood pressure daily.',
    'Adopt a low-sodium, heart-healthy diet.',
    'Engage in light to moderate physical activity as advised.',
    'Consider medication review with your physician.',
  ],
  negative: [
    'Maintain regular annual check-ups.',
    'Keep a balanced diet rich in vegetables and fruits.',
    'Stay physically active for at least 30 min/day.',
    'Avoid smoking and limit alcohol intake.',
    'Manage stress through mindfulness or yoga.',
  ],
}

export default function ResultCard({ result }) {
  const { score, positive, risk_level, model_name, risk_factors, protective_factors } = result
  const cardRef = useRef(null)

  useEffect(() => {
    cardRef.current?.scrollIntoView({ behavior: 'smooth', block: 'center' })
  }, [result])

  const deg = (score / 100) * 180  // for the half-circle gauge

  const displayTips = positive
    ? (risk_factors && risk_factors.length > 0 ? risk_factors : defaultTips.positive)
    : (protective_factors && protective_factors.length > 0 ? protective_factors : defaultTips.negative)

  return (
    <div
      className={`${styles.card} ${positive ? styles.cardDanger : styles.cardSafe}`}
      ref={cardRef}
    >
      {/* Header */}
      <div className={styles.header}>
        <div className={`${styles.icon} ${positive ? styles.iconDanger : styles.iconSafe}`}>
          {positive ? <AlertTriangle size={26} /> : <CheckCircle2 size={26} />}
        </div>
        <div style={{ flex: 1 }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '8px' }}>
            <p className={styles.verdict}>
              {positive ? 'Cardiovascular Disease Risk Detected' : 'Low Cardiovascular Risk'}
            </p>
            {risk_level && (
              <span style={{
                fontSize: '0.75rem',
                fontWeight: 700,
                padding: '4px 10px',
                borderRadius: '20px',
                backgroundColor: positive ? 'rgba(230,57,70,0.15)' : 'rgba(34,197,94,0.15)',
                color: positive ? 'var(--red)' : '#22c55e',
                border: `1px solid ${positive ? 'rgba(230,57,70,0.3)' : 'rgba(34,197,94,0.3)'}`
              }}>
                {risk_level}
              </span>
            )}
          </div>
          <p className={styles.sub}>
            {positive
              ? 'This patient exhibits high risk indicators for cardiovascular disease. Medical consultation is advised.'
              : 'Clinical biometrics are within safe baseline ranges for cardiovascular health.'}
          </p>
        </div>
      </div>

      {/* Gauge + Score */}
      <div className={styles.gaugeSection}>
        <div className={styles.gauge}>
          <svg viewBox="0 0 200 110" className={styles.gaugeSvg}>
            {/* Track */}
            <path
              d="M10,100 A90,90 0 0,1 190,100"
              fill="none" stroke="#1e1e35" strokeWidth="14" strokeLinecap="round"
            />
            {/* Fill */}
            <path
              d="M10,100 A90,90 0 0,1 190,100"
              fill="none"
              stroke={positive ? '#e63946' : '#22c55e'}
              strokeWidth="14"
              strokeLinecap="round"
              strokeDasharray="283"
              strokeDashoffset={283 - (score / 100) * 283}
              style={{ transition: 'stroke-dashoffset 1.2s ease' }}
            />
            {/* Needle */}
            <line
              x1="100" y1="100"
              x2={100 + 75 * Math.cos(Math.PI - (deg * Math.PI / 180))}
              y2={100 - 75 * Math.sin(Math.PI - (deg * Math.PI / 180))}
              stroke={positive ? '#e63946' : '#22c55e'}
              strokeWidth="3" strokeLinecap="round"
              style={{ transition: 'all 1.2s ease' }}
            />
            <circle cx="100" cy="100" r="5" fill={positive ? '#e63946' : '#22c55e'} />
            {/* Labels */}
            <text x="10"  y="118" fontSize="10" fill="#4a4a6a">Low</text>
            <text x="172" y="118" fontSize="10" fill="#4a4a6a">High</text>
          </svg>
          <div className={styles.scoreLabel}>
            <span className={`${styles.scoreNum} ${positive ? styles.scoreRed : styles.scoreGreen}`}>
              {score}%
            </span>
            <span className={styles.scoreCaption}>Risk Probability</span>
          </div>
        </div>

        {/* Risk Bands */}
        <div className={styles.bands}>
          {[
            { label: 'Low Risk',      range: '0–25%',   color: '#22c55e', active: score <= 25 },
            { label: 'Moderate',      range: '26–49%',  color: '#f59e0b', active: score > 25 && score <= 49 },
            { label: 'High Risk',     range: '50–69%',  color: '#f97316', active: score > 49 && score <= 69 },
            { label: 'Critical',      range: '70–100%', color: '#e63946', active: score > 69 },
          ].map(b => (
            <div key={b.label} className={`${styles.band} ${b.active ? styles.bandActive : ''}`}>
              <span className={styles.bandDot} style={{ background: b.color }} />
              <span className={styles.bandLabel}>{b.label}</span>
              <span className={styles.bandRange}>{b.range}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Dynamic Factors / Insights */}
      <div className={styles.tips}>
        <p className={styles.tipsTitle}>
          <Info size={14} />
          {positive ? 'Key Risk Factors & Observations' : 'Protective Health Indicators'}
        </p>
        <ul className={styles.tipsList}>
          {displayTips.map((t, i) => (
            <li key={i} className={styles.tipItem}>
              <span className={`${styles.tipBullet} ${positive ? styles.tipBulletRed : styles.tipBulletGreen}`} />
              {t}
            </li>
          ))}
        </ul>
      </div>

      <div style={{
        padding: '12px 28px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        background: 'rgba(255,255,255,0.02)',
        borderBottom: '1px solid var(--border)',
        fontSize: '0.78rem',
        color: 'var(--text-muted)'
      }}>
        <span>Engine: <strong style={{ color: 'var(--text-secondary)' }}>{model_name || 'Ensemble Model'}</strong></span>
        <span>Confidence: <strong style={{ color: 'var(--text-secondary)' }}>{Math.max(score, 100 - score)}%</strong></span>
      </div>

      <p className={styles.disclaimer}>
        ⚠ This result is generated by a machine learning model for clinical decision support. Always verify findings with qualified healthcare professionals.
      </p>
    </div>
  )
}
