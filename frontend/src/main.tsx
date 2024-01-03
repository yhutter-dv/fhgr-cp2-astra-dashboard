import React from 'react'
import ReactDOM from 'react-dom/client'
import Dashboard from './components/Dashboard.tsx'
import './index.css'
import Header from './components/Header.tsx'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <>
    <React.StrictMode>
      <Header />
    </React.StrictMode>

    {/* 
    
      Disable Strict Mode here so the requests do not run twice (see https://upmostly.com/tutorials/why-is-my-useeffect-hook-running-twice-in-react)
    
    */}
    <Dashboard />
  </>


)
