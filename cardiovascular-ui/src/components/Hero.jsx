import styles from './Hero.module.css'
import { ShieldCheck, Zap, BarChart2 } from 'lucide-react'

const stats = [
  { icon: <ShieldCheck size={18}/>, value: '94.2%', label: 'Accuracy' },
  { icon: <Zap size={18}/>,        value: '<1s',   label: 'Prediction Time' },
  { icon: <BarChart2 size={18}/>,  value: '70k+',  label: 'Patients Trained' },
]

export default function Hero() {
  return (
    <section className={styles.hero} id="hero">
      {/* background glow blobs */}
      <div className={styles.blob1} />
      <div className={styles.blob2} />

      <div className={styles.inner}>
        <div className={styles.badge}>
          <span className={styles.pulse} />
          AI-Powered Cardiovascular Analysis
        </div>

        <h1 className={styles.heading}>
          Detect Heart Disease<br />
          <span className={styles.accent}>Before It Strikes</span>
        </h1>

        <p className={styles.subtext}>
          Enter patient clinical data below and let our machine learning model
          assess the risk of cardiovascular disease — instantly, accurately, and securely.
        </p>

        <div className={styles.actions}>
          <a href="#predict" className={styles.btnPrimary}>Start Prediction →</a>
          <a href="#about"   className={styles.btnGhost}>Learn More</a>
        </div>

        <div className={styles.statsRow}>
          {stats.map((s) => (
            <div key={s.label} className={styles.statCard}>
              <span className={styles.statIcon}>{s.icon}</span>
              <span className={styles.statValue}>{s.value}</span>
              <span className={styles.statLabel}>{s.label}</span>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
