import styles from './Footer.module.css'
import { Activity, Heart } from 'lucide-react'

export default function Footer() {
  return (
    <footer className={styles.footer}>
      <div className={styles.inner}>
        <div className={styles.logo}>
          <span className={styles.logoIcon}><Activity size={16} strokeWidth={2.5} /></span>
          <span>CardioScan</span>
        </div>
        <p className={styles.copy}>
          Built with <Heart size={12} className={styles.heartIcon} /> for ML Project · Dataset by{' '}
          <a href="https://www.kaggle.com/datasets/sulianova/cardiovascular-disease-dataset" target="_blank" rel="noreferrer">
            Kaggle / Sulianova
          </a>
        </p>
        <p className={styles.disclaimer}>
          For educational and research purposes only. Not a substitute for medical advice.
        </p>
      </div>
    </footer>
  )
}
