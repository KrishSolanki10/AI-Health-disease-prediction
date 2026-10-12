import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Login from './pages/Login.jsx'
import Dashboard from './pages/Dashboard.jsx'
import Prediction from './pages/Prediction.jsx'
import Chatbot from './pages/Chatbot.jsx'
import Reports from './pages/Reports.jsx'
import Admin from './pages/Admin.jsx'

// Phase 1: routes wired up as placeholders.
// Real auth-guarding + layout gets added in Phase 2.
function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/predict" element={<Prediction />} />
        <Route path="/chatbot" element={<Chatbot />} />
        <Route path="/reports" element={<Reports />} />
        <Route path="/admin" element={<Admin />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
