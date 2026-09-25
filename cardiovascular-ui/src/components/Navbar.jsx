import { NavLink } from 'react-router-dom'
import { Activity } from 'lucide-react'
import styles from './Navbar.module.css'

export default function Navbar() {
  return (
    <nav className={styles.nav}>
      <div className={styles.inner}>
        <NavLink to="/" className={styles.logo}>
          <span className={styles.logoIcon}><Activity size={18} strokeWidth={2.5} /></span>
          <span className={styles.logoText}>CardioScan</span>
        </NavLink>

        <ul className={styles.links}>
          <li>
            <NavLink to="/" end className={({ isActive }) => isActive ? `${styles.link} ${styles.active}` : styles.link}>
              Home
            </NavLink>
          </li>
          <li>
            <NavLink to="/about" className={({ isActive }) => isActive ? `${styles.link} ${styles.active}` : styles.link}>
              Dataset
            </NavLink>
          </li>
          <li>
            <NavLink to="/predict" className={({ isActive }) => isActive ? `${styles.link} ${styles.active}` : styles.link}>
              Predict
            </NavLink>
          </li>
        </ul>

        <NavLink to="/predict" className={styles.cta}>Run Prediction</NavLink>
      </div>
    </nav>
  )
}
