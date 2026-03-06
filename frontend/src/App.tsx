import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { useAuthStore } from './store/authStore'

// Public pages
import HomePage from './pages/HomePage'
import LoginPage from './pages/LoginPage'
import SignupPage from './pages/SignupPage'
import TemplatesPage from './pages/TemplatesPage'
import PricingPage from './pages/PricingPage'

// Private pages
import DashboardPage from './pages/DashboardPage'
import CreateProjectPage from './pages/CreateProjectPage'
import EditorPage from './pages/EditorPage'
import PreviewPage from './pages/PreviewPage'
import ExportPage from './pages/ExportPage'
import SettingsPage from './pages/SettingsPage'
import AIGeneratePage from './pages/AIGeneratePage'

function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const isAuthenticated = useAuthStore(state => state.isAuthenticated)
  return isAuthenticated ? <>{children}</> : <Navigate to="/login" />
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Public routes */}
        <Route path="/" element={<HomePage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/signup" element={<SignupPage />} />
        <Route path="/templates" element={<TemplatesPage />} />
        <Route path="/pricing" element={<PricingPage />} />

        {/* Protected routes */}
        <Route path="/dashboard" element={<ProtectedRoute><DashboardPage /></ProtectedRoute>} />
        <Route path="/projects/new" element={<ProtectedRoute><CreateProjectPage /></ProtectedRoute>} />
        <Route path="/projects/:id/edit" element={<ProtectedRoute><EditorPage /></ProtectedRoute>} />
        <Route path="/projects/:id/preview" element={<ProtectedRoute><PreviewPage /></ProtectedRoute>} />
        <Route path="/projects/:id/export" element={<ProtectedRoute><ExportPage /></ProtectedRoute>} />
        <Route path="/projects/:id/ai-generate" element={<ProtectedRoute><AIGeneratePage /></ProtectedRoute>} />
        <Route path="/settings" element={<ProtectedRoute><SettingsPage /></ProtectedRoute>} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
