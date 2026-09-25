import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import Footer from './components/Footer'
import Home    from './pages/Home'
import About   from './pages/About'
import Predict from './pages/Predict'
import './App.css'

export default function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <main>
        <Routes>
          <Route path="/"        element={<Home />} />
          <Route path="/about"   element={<About />} />
          <Route path="/predict" element={<Predict />} />
          {/* 404 fallback */}
          <Route path="*" element={
            <div style={{ textAlign:'center', padding:'160px 24px', color:'var(--text-secondary)' }}>
              <h2 style={{ fontFamily:'var(--font-head)', fontSize:'2rem', marginBottom:'12px', color:'var(--text-primary)' }}>
                404 — Page not found
              </h2>
              <a href="/" style={{ color:'var(--red)' }}>← Go Home</a>
            </div>
          } />
        </Routes>
      </main>
      <Footer />
    </BrowserRouter>
  )
}
