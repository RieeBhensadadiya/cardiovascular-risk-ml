import { useState } from 'react'
import styles from './PredictionForm.module.css'
import ResultCard from './ResultCard'
import {
  User, Ruler, Weight, Droplets, Activity,
  Cigarette, Wine, Heart, ChevronRight, RotateCcw, AlertCircle, RefreshCw
} from 'lucide-react'

const initialState = {
  age: '', gender: '', height: '', weight: '',
  ap_hi: '', ap_lo: '', cholesterol: '', gluc: '',
  smoke: '', alco: '', active: '',
}

export default function PredictionForm() {
  const [form, setForm]         = useState(initialState)
  const [result, setResult]     = useState(null)
  const [loading, setLoading]   = useState(false)
  const [errors, setErrors]     = useState({})
  const [apiError, setApiError] = useState(null)

  const handle = (e) => {
    setForm(f => ({ ...f, [e.target.name]: e.target.value }))
    setErrors(er => ({ ...er, [e.target.name]: '' }))
    if (apiError) setApiError(null)
  }

  const validate = () => {
    const err = {}
    Object.entries(form).forEach(([k, v]) => {
      if (v === '' || v === null || v === undefined) err[k] = 'Required'
    })
    if (form.ap_hi && form.ap_lo && parseInt(form.ap_hi) < parseInt(form.ap_lo)) {
      err.ap_hi = 'Systolic must be ≥ Diastolic'
    }
    return err
  }

  const submit = async (e) => {
    e.preventDefault()
    const err = validate()
    if (Object.keys(err).length) { setErrors(err); return }
    setLoading(true)
    setResult(null)
    setApiError(null)

    const payload = {
      age: parseFloat(form.age),
      gender: parseInt(form.gender),
      height: parseFloat(form.height),
      weight: parseFloat(form.weight),
      ap_hi: parseFloat(form.ap_hi),
      ap_lo: parseFloat(form.ap_lo),
      cholesterol: parseInt(form.cholesterol),
      gluc: parseInt(form.gluc),
      smoke: parseInt(form.smoke),
      alco: parseInt(form.alco),
      active: parseInt(form.active)
    }

    try {
      const API_BASE = import.meta.env.VITE_API_URL || ''
      const endpoint = API_BASE ? `${API_BASE.replace(/\/$/, '')}/api/predict` : '/api/predict'

      let response
      try {
        response = await fetch(endpoint, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        })
      } catch (err) {
        response = null
      }

      // If proxy failed or returned error and we are on localhost, try direct port 5000 then 8000
      if ((!response || !response.ok) && !API_BASE) {
        try {
          response = await fetch('http://127.0.0.1:5000/api/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
          })
        } catch {
          try {
            response = await fetch('http://127.0.0.1:8000/api/predict', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify(payload)
            })
          } catch {
            response = null
          }
        }
      }

      if (!response) {
        throw new Error('Could not connect to the ML Backend on port 5000 or 8000. Please start the backend.')
      }

      if (!response.ok) {
        const errData = await response.json().catch(() => ({}))
        throw new Error(errData.detail || errData.error || `Server responded with status ${response.status}`)
      }

      const data = await response.json()
      setResult(data)
    } catch (err) {
      console.error('Prediction API Error:', err)
      const targetHost = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'
      setApiError(
        err.message?.includes('Failed to fetch') || err.message?.includes('NetworkError')
          ? `Unable to connect to ML Backend server (${targetHost}). Please make sure the backend is active.`
          : `Prediction error: ${err.message}`
      )
    } finally {
      setLoading(false)
    }
  }

  const reset = () => { 
    setForm(initialState)
    setResult(null)
    setErrors({})
    setApiError(null)
  }

  const bmi = form.height && form.weight
    ? (parseFloat(form.weight) / ((parseInt(form.height) / 100) ** 2)).toFixed(1)
    : null

  return (
    <section className={styles.section} id="predict">
      <div className={styles.inner}>
        <div className={styles.sectionHeader}>
          <span className={styles.sectionTag}>Prediction Engine</span>
          <h2 className={styles.sectionTitle}>Patient Risk Assessment</h2>
          <p className={styles.sectionSub}>
            Fill in patient data from the medical examination. All 11 dataset features are used by the ML model.
          </p>
        </div>

        {apiError && (
          <div style={{
            margin: '0 0 20px 0',
            padding: '12px 16px',
            backgroundColor: 'rgba(230, 57, 70, 0.1)',
            border: '1px solid rgba(230, 57, 70, 0.35)',
            borderRadius: '10px',
            display: 'flex',
            alignItems: 'center',
            gap: '10px',
            color: '#ff6b6b',
            fontSize: '0.88rem'
          }}>
            <AlertCircle size={18} style={{ flexShrink: 0 }} />
            <div style={{ flex: 1 }}>{apiError}</div>
            <button 
              type="button" 
              onClick={submit}
              style={{
                background: 'transparent',
                border: '1px solid rgba(230, 57, 70, 0.5)',
                color: '#ff6b6b',
                padding: '3px 8px',
                borderRadius: '6px',
                cursor: 'pointer',
                fontSize: '0.78rem'
              }}
            >
              Retry
            </button>
          </div>
        )}

        <form className={styles.form} onSubmit={submit} noValidate>

          {/* ── Row 1: Objective Features ── */}
          <fieldset className={styles.fieldset}>
            <legend className={styles.legend}>
              <User size={15} /> Objective Features
            </legend>
            <div className={styles.grid4}>

              {/* Age */}
              <div className={styles.field}>
                <label className={styles.label}>Age <span className={styles.unit}>(years)</span></label>
                <input
                  className={`${styles.input} ${errors.age ? styles.inputErr : ''}`}
                  type="number" name="age" placeholder="e.g. 45"
                  value={form.age} onChange={handle} min="1" max="120"
                />
                {errors.age && <span className={styles.errMsg}>{errors.age}</span>}
              </div>

              {/* Gender */}
              <div className={styles.field}>
                <label className={styles.label}>Gender</label>
                <select className={`${styles.select} ${errors.gender ? styles.inputErr : ''}`}
                  name="gender" value={form.gender} onChange={handle}>
                  <option value="">Select</option>
                  <option value="1">Female</option>
                  <option value="2">Male</option>
                </select>
                {errors.gender && <span className={styles.errMsg}>{errors.gender}</span>}
              </div>

              {/* Height */}
              <div className={styles.field}>
                <label className={styles.label}>Height <span className={styles.unit}>(cm)</span></label>
                <input
                  className={`${styles.input} ${errors.height ? styles.inputErr : ''}`}
                  type="number" name="height" placeholder="e.g. 168"
                  value={form.height} onChange={handle} min="100" max="250"
                />
                {errors.height && <span className={styles.errMsg}>{errors.height}</span>}
              </div>

              {/* Weight */}
              <div className={styles.field}>
                <label className={styles.label}>Weight <span className={styles.unit}>(kg)</span></label>
                <input
                  className={`${styles.input} ${errors.weight ? styles.inputErr : ''}`}
                  type="number" name="weight" placeholder="e.g. 62"
                  value={form.weight} onChange={handle} min="20" max="300"
                />
                {bmi && (
                  <span className={`${styles.hint} ${parseFloat(bmi) > 30 ? styles.hintWarn : parseFloat(bmi) > 25 ? styles.hintCaution : styles.hintOk}`}>
                    BMI: {bmi}
                  </span>
                )}
                {errors.weight && <span className={styles.errMsg}>{errors.weight}</span>}
              </div>
            </div>
          </fieldset>

          {/* ── Row 2: Examination Features ── */}
          <fieldset className={styles.fieldset}>
            <legend className={styles.legend}>
              <Droplets size={15} /> Examination Features
            </legend>
            <div className={styles.grid4}>

              {/* Systolic BP */}
              <div className={styles.field}>
                <label className={styles.label}>Systolic BP <span className={styles.unit}>(ap_hi mmHg)</span></label>
                <input
                  className={`${styles.input} ${errors.ap_hi ? styles.inputErr : ''}`}
                  type="number" name="ap_hi" placeholder="e.g. 120"
                  value={form.ap_hi} onChange={handle}
                />
                {errors.ap_hi && <span className={styles.errMsg}>{errors.ap_hi}</span>}
              </div>

              {/* Diastolic BP */}
              <div className={styles.field}>
                <label className={styles.label}>Diastolic BP <span className={styles.unit}>(ap_lo mmHg)</span></label>
                <input
                  className={`${styles.input} ${errors.ap_lo ? styles.inputErr : ''}`}
                  type="number" name="ap_lo" placeholder="e.g. 80"
                  value={form.ap_lo} onChange={handle}
                />
                {errors.ap_lo && <span className={styles.errMsg}>{errors.ap_lo}</span>}
              </div>

              {/* Cholesterol */}
              <div className={styles.field}>
                <label className={styles.label}>Cholesterol</label>
                <select className={`${styles.select} ${errors.cholesterol ? styles.inputErr : ''}`}
                  name="cholesterol" value={form.cholesterol} onChange={handle}>
                  <option value="">Select level</option>
                  <option value="1">1 — Normal</option>
                  <option value="2">2 — Above Normal</option>
                  <option value="3">3 — Well Above Normal</option>
                </select>
                {errors.cholesterol && <span className={styles.errMsg}>{errors.cholesterol}</span>}
              </div>

              {/* Glucose */}
              <div className={styles.field}>
                <label className={styles.label}>Glucose</label>
                <select className={`${styles.select} ${errors.gluc ? styles.inputErr : ''}`}
                  name="gluc" value={form.gluc} onChange={handle}>
                  <option value="">Select level</option>
                  <option value="1">1 — Normal</option>
                  <option value="2">2 — Above Normal</option>
                  <option value="3">3 — Well Above Normal</option>
                </select>
                {errors.gluc && <span className={styles.errMsg}>{errors.gluc}</span>}
              </div>
            </div>
          </fieldset>

          {/* ── Row 3: Subjective Features ── */}
          <fieldset className={styles.fieldset}>
            <legend className={styles.legend}>
              <Activity size={15} /> Subjective Features
            </legend>
            <div className={styles.grid3}>

              {/* Smoking */}
              <div className={styles.field}>
                <label className={styles.label}><Cigarette size={13}/> Smoking</label>
                <div className={styles.toggleGroup}>
                  {[['0','Non-smoker'],['1','Smoker']].map(([v, label]) => (
                    <label key={v} className={`${styles.toggle} ${form.smoke === v ? styles.toggleActive : ''}`}>
                      <input type="radio" name="smoke" value={v} onChange={handle} checked={form.smoke === v} />
                      {label}
                    </label>
                  ))}
                </div>
                {errors.smoke && <span className={styles.errMsg}>{errors.smoke}</span>}
              </div>

              {/* Alcohol */}
              <div className={styles.field}>
                <label className={styles.label}><Wine size={13}/> Alcohol Intake</label>
                <div className={styles.toggleGroup}>
                  {[['0','No'],['1','Yes']].map(([v, label]) => (
                    <label key={v} className={`${styles.toggle} ${form.alco === v ? styles.toggleActive : ''}`}>
                      <input type="radio" name="alco" value={v} onChange={handle} checked={form.alco === v} />
                      {label}
                    </label>
                  ))}
                </div>
                {errors.alco && <span className={styles.errMsg}>{errors.alco}</span>}
              </div>

              {/* Physical Activity */}
              <div className={styles.field}>
                <label className={styles.label}><Activity size={13}/> Physical Activity</label>
                <div className={styles.toggleGroup}>
                  {[['1','Active'],['0','Inactive']].map(([v, label]) => (
                    <label key={v} className={`${styles.toggle} ${form.active === v ? styles.toggleActive : ''}`}>
                      <input type="radio" name="active" value={v} onChange={handle} checked={form.active === v} />
                      {label}
                    </label>
                  ))}
                </div>
                {errors.active && <span className={styles.errMsg}>{errors.active}</span>}
              </div>
            </div>
          </fieldset>

          {/* Actions */}
          <div className={styles.actions}>
            <button type="button" className={styles.btnReset} onClick={reset}>
              <RotateCcw size={15}/> Reset
            </button>
            <button type="submit" className={styles.btnSubmit} disabled={loading}>
              {loading
                ? <><span className={styles.spinner}/> Analyzing with ML Model…</>
                : <><Heart size={16}/> Predict Risk <ChevronRight size={16}/></>
              }
            </button>
          </div>
        </form>

        {/* Result */}
        {result && <ResultCard result={result} />}
      </div>
    </section>
  )
}
