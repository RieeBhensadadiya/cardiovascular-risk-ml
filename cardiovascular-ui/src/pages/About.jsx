import { Link } from 'react-router-dom'
import { Clock, Ruler, Weight, Users, Droplets, Heart, Cigarette, Wine, Activity, FlaskConical, ArrowRight } from 'lucide-react'
import styles from './About.module.css'

const features = [
  { icon: <Clock size={18}/>,        label: 'Age',               desc: 'Patient age in days (÷365 for years)',  type: 'Objective',   col: 'age' },
  { icon: <Users size={18}/>,        label: 'Gender',             desc: '1 = Female, 2 = Male',                 type: 'Objective',   col: 'gender' },
  { icon: <Ruler size={18}/>,        label: 'Height',             desc: 'Height in centimetres',                type: 'Objective',   col: 'height' },
  { icon: <Weight size={18}/>,       label: 'Weight',             desc: 'Weight in kilograms',                  type: 'Objective',   col: 'weight' },
  { icon: <Droplets size={18}/>,     label: 'Systolic BP',        desc: 'ap_hi — upper blood pressure reading', type: 'Examination', col: 'ap_hi' },
  { icon: <Droplets size={18}/>,     label: 'Diastolic BP',       desc: 'ap_lo — lower blood pressure reading', type: 'Examination', col: 'ap_lo' },
  { icon: <FlaskConical size={18}/>, label: 'Cholesterol',        desc: '1 = Normal · 2 = Above Normal · 3 = Well Above', type: 'Examination', col: 'cholesterol' },
  { icon: <FlaskConical size={18}/>, label: 'Glucose',            desc: '1 = Normal · 2 = Above Normal · 3 = Well Above', type: 'Examination', col: 'gluc' },
  { icon: <Cigarette size={18}/>,    label: 'Smoking',            desc: '0 = Non-smoker · 1 = Smoker',          type: 'Subjective',  col: 'smoke' },
  { icon: <Wine size={18}/>,         label: 'Alcohol Intake',     desc: '0 = No · 1 = Yes',                     type: 'Subjective',  col: 'alco' },
  { icon: <Activity size={18}/>,     label: 'Physical Activity',  desc: '0 = Inactive · 1 = Active',            type: 'Subjective',  col: 'active' },
]

const typeConfig = {
  Objective:   { color: '#6366f1', bg: '#6366f115' },
  Examination: { color: '#f59e0b', bg: '#f59e0b15' },
  Subjective:  { color: '#22c55e', bg: '#22c55e15' },
}

export default function About() {
  return (
    <div className={styles.page}>

      {/* Page Header */}
      <div className={styles.pageHeader}>
        <span className={styles.tag}>Kaggle Dataset</span>
        <h1 className={styles.pageTitle}>Cardiovascular Disease Dataset</h1>
        <p className={styles.pageSub}>
          <strong>70,000 patient records</strong> · 11 input features + 1 target variable.<br />
          Collected at the moment of medical examination by <em>Svetlana Ulianova</em>.
        </p>
        <a
          href="https://www.kaggle.com/datasets/sulianova/cardiovascular-disease-dataset"
          target="_blank" rel="noreferrer"
          className={styles.kaggleLink}
        >
          View on Kaggle →
        </a>
      </div>

      {/* Legend */}
      <div className={styles.legendRow}>
        {Object.entries(typeConfig).map(([type, cfg]) => (
          <span key={type} className={styles.legendItem}>
            <span className={styles.legendDot} style={{ background: cfg.color }} />
            {type} Feature
          </span>
        ))}
        <span className={styles.legendItem}>
          <span className={styles.legendDot} style={{ background: '#e63946' }} />
          Target Variable
        </span>
      </div>

      {/* Feature cards */}
      <div className={styles.grid}>
        {features.map((f, i) => {
          const cfg = typeConfig[f.type]
          return (
            <div key={i} className={styles.card}>
              <div className={styles.cardTop}>
                <span className={styles.cardIcon} style={{ color: cfg.color, background: cfg.bg }}>
                  {f.icon}
                </span>
                <code className={styles.colName}>{f.col}</code>
              </div>
              <p className={styles.cardLabel}>{f.label}</p>
              <p className={styles.cardDesc}>{f.desc}</p>
              <span className={styles.badge} style={{ color: cfg.color, borderColor: cfg.color + '40', background: cfg.bg }}>
                {f.type}
              </span>
            </div>
          )
        })}

        {/* Target card */}
        <div className={`${styles.card} ${styles.targetCard}`}>
          <div className={styles.cardTop}>
            <span className={styles.cardIcon} style={{ color: '#e63946', background: '#e6394618' }}>
              <Heart size={18} />
            </span>
            <code className={styles.colName}>cardio</code>
          </div>
          <p className={styles.cardLabel}>Cardiovascular Disease</p>
          <p className={styles.cardDesc}>0 = No Disease · 1 = Disease Present</p>
          <span className={styles.badge} style={{ color: '#e63946', borderColor: '#e6394640', background: '#e6394615' }}>
            Target
          </span>
        </div>
      </div>

      {/* Dataset stats bar */}
      <div className={styles.statsBar}>
        {[
          { label: 'Total Records',    val: '70,000' },
          { label: 'Input Features',   val: '11' },
          { label: 'Target Variable',  val: '1 (binary)' },
          { label: 'Disease Positive', val: '~50%' },
        ].map(s => (
          <div key={s.label} className={styles.statItem}>
            <span className={styles.statVal}>{s.val}</span>
            <span className={styles.statLbl}>{s.label}</span>
          </div>
        ))}
      </div>

      {/* CTA */}
      <div className={styles.cta}>
        <Link to="/predict" className={styles.ctaBtn}>
          <Heart size={16} /> Start Prediction <ArrowRight size={16} />
        </Link>
      </div>

    </div>
  )
}
