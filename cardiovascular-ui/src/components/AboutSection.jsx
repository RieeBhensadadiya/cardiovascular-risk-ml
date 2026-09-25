import styles from './AboutSection.module.css'
import { Clock, Ruler, Weight, Users, Droplets, Heart, Cigarette, Wine, Activity, FlaskConical } from 'lucide-react'

const features = [
  { icon: <Clock size={18}/>,      label: 'Age',             desc: 'Patient age in days',                  type: 'Objective' },
  { icon: <Users size={18}/>,      label: 'Gender',          desc: 'Biological sex of the patient',        type: 'Objective' },
  { icon: <Ruler size={18}/>,      label: 'Height',          desc: 'Height in centimetres',                type: 'Objective' },
  { icon: <Weight size={18}/>,     label: 'Weight',          desc: 'Weight in kilograms',                  type: 'Objective' },
  { icon: <Droplets size={18}/>,   label: 'Systolic BP',     desc: 'ap_hi — upper blood pressure reading', type: 'Examination' },
  { icon: <Droplets size={18}/>,   label: 'Diastolic BP',    desc: 'ap_lo — lower blood pressure reading', type: 'Examination' },
  { icon: <FlaskConical size={18}/>,label: 'Cholesterol',    desc: 'Normal / Above Normal / Well Above',   type: 'Examination' },
  { icon: <FlaskConical size={18}/>,label: 'Glucose',        desc: 'Blood glucose level category',         type: 'Examination' },
  { icon: <Cigarette size={18}/>,  label: 'Smoking',         desc: 'Whether the patient smokes',           type: 'Subjective' },
  { icon: <Wine size={18}/>,       label: 'Alcohol Intake',  desc: 'Regular alcohol consumption',          type: 'Subjective' },
  { icon: <Activity size={18}/>,   label: 'Physical Activity',desc: 'Regular physical activity status',   type: 'Subjective' },
]

const typeColor = {
  Objective:   '#6366f1',
  Examination: '#f59e0b',
  Subjective:  '#22c55e',
}

export default function AboutSection() {
  return (
    <section className={styles.section} id="about">
      <div className={styles.inner}>

        <div className={styles.sectionHeader}>
          <span className={styles.sectionTag}>Dataset</span>
          <h2 className={styles.sectionTitle}>11 Clinical Features</h2>
          <p className={styles.sectionSub}>
            Based on the Kaggle Cardiovascular Disease Dataset — 70,000 patient records
            across three feature categories.
          </p>
        </div>

        {/* Legend */}
        <div className={styles.legend}>
          {Object.entries(typeColor).map(([type, color]) => (
            <span key={type} className={styles.legendItem}>
              <span className={styles.legendDot} style={{ background: color }} />
              {type}
            </span>
          ))}
        </div>

        {/* Cards grid */}
        <div className={styles.grid}>
          {features.map((f, i) => (
            <div key={i} className={styles.card}>
              <div className={styles.cardTop}>
                <span className={styles.cardIcon} style={{ color: typeColor[f.type] }}>
                  {f.icon}
                </span>
                <span className={styles.badge} style={{ color: typeColor[f.type], borderColor: typeColor[f.type] + '55', background: typeColor[f.type] + '11' }}>
                  {f.type}
                </span>
              </div>
              <p className={styles.cardLabel}>{f.label}</p>
              <p className={styles.cardDesc}>{f.desc}</p>
            </div>
          ))}

          {/* Target card */}
          <div className={`${styles.card} ${styles.targetCard}`}>
            <div className={styles.cardTop}>
              <span className={styles.cardIcon} style={{ color: '#e63946' }}>
                <Heart size={18} />
              </span>
              <span className={styles.badge} style={{ color: '#e63946', borderColor: '#e6394655', background: '#e6394611' }}>
                Target
              </span>
            </div>
            <p className={styles.cardLabel}>Cardiovascular Disease</p>
            <p className={styles.cardDesc}>Binary — presence (1) or absence (0) of the disease</p>
          </div>
        </div>
      </div>
    </section>
  )
}
