import { Link } from 'react-router-dom'
import { ShieldCheck, Zap, BarChart2, ArrowRight, Heart, Brain, Database } from 'lucide-react'
import styles from './Home.module.css'

const stats = [
  { icon: <ShieldCheck size={20} />, value: '94.2%', label: 'Model Accuracy' },
  { icon: <Zap size={20} />,         value: '<1s',   label: 'Prediction Time' },
  { icon: <Database size={20} />,    value: '70k+',  label: 'Records Trained' },
  { icon: <BarChart2 size={20} />,   value: '11',    label: 'Clinical Features' },
]

const cards = [
  {
    icon: <Brain size={22} />,
    title: 'ML-Powered Analysis',
    desc: 'Trained on 70,000 real patient records using advanced machine learning algorithms.',
    color: '#6366f1',
  },
  {
    icon: <Heart size={22} />,
    title: 'Instant Risk Scoring',
    desc: 'Get a cardiovascular risk score in under a second with a detailed breakdown.',
    color: '#e63946',
  },
  {
    icon: <ShieldCheck size={22} />,
    title: 'Clinically Grounded',
    desc: 'Uses blood pressure, cholesterol, glucose, BMI and lifestyle factors for holistic assessment.',
    color: '#22c55e',
  },
]

export default function Home() {
  return (
    <div className={styles.page}>

      {/* ── Hero ── */}
      <section className={styles.hero}>
        <div className={styles.blob1} />
        <div className={styles.blob2} />

        <div className={styles.heroInner}>
          <div className={styles.badge}>
            <span className={styles.pulse} />
            AI-Powered Cardiovascular Analysis
          </div>

          <h1 className={styles.heading}>
            Detect Heart Disease<br />
            <span className={styles.accent}>Before It Strikes</span>
          </h1>

          <p className={styles.subtext}>
            Enter patient clinical data and let our machine learning model instantly
            assess cardiovascular disease risk — accurately, and securely.
          </p>

          <div className={styles.heroActions}>
            <Link to="/predict" className={styles.btnPrimary}>
              <Heart size={16} /> Start Prediction <ArrowRight size={16} />
            </Link>
            <Link to="/about" className={styles.btnGhost}>
              View Dataset →
            </Link>
          </div>
        </div>
      </section>

      {/* ── Stats ── */}
      <section className={styles.statsSection}>
        <div className={styles.statsGrid}>
          {stats.map((s) => (
            <div key={s.label} className={styles.statCard}>
              <span className={styles.statIcon}>{s.icon}</span>
              <span className={styles.statValue}>{s.value}</span>
              <span className={styles.statLabel}>{s.label}</span>
            </div>
          ))}
        </div>
      </section>

      {/* ── Feature Cards ── */}
      <section className={styles.featuresSection}>
        <div className={styles.sectionHead}>
          <h2 className={styles.sectionTitle}>Why CardioScan?</h2>
          <p className={styles.sectionSub}>
            A complete cardiovascular risk assessment tool built on real clinical data.
          </p>
        </div>
        <div className={styles.cardsGrid}>
          {cards.map((c) => (
            <div key={c.title} className={styles.featureCard}>
              <span className={styles.featureIcon} style={{ color: c.color, background: c.color + '18' }}>
                {c.icon}
              </span>
              <h3 className={styles.featureTitle}>{c.title}</h3>
              <p className={styles.featureDesc}>{c.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* ── CTA Banner ── */}
      <section className={styles.ctaBanner}>
        <div className={styles.ctaInner}>
          <h2 className={styles.ctaTitle}>Ready to assess a patient?</h2>
          <p className={styles.ctaSub}>Fill in the clinical form and get an instant risk report.</p>
          <Link to="/predict" className={styles.btnPrimary}>
            Go to Prediction Tool <ArrowRight size={16} />
          </Link>
        </div>
      </section>

    </div>
  )
}
