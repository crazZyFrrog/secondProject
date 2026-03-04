import { Link, useNavigate } from 'react-router-dom'
import { useAuthStore } from '../store/authStore'
import { LogOut, Settings, LayoutDashboard } from 'lucide-react'

export default function Header() {
  const { isAuthenticated, user, logout } = useAuthStore()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/')
  }

  return (
    <header className="bg-white shadow-sm sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-primary-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-xl">L</span>
            </div>
            <span className="text-xl font-bold text-gray-900">LandingBuilder</span>
          </Link>

          {/* Navigation */}
          <nav className="hidden md:flex items-center space-x-8">
            <Link to="/templates" className="text-gray-600 hover:text-gray-900 transition">
              Шаблоны
            </Link>
            <Link to="/pricing" className="text-gray-600 hover:text-gray-900 transition">
              Тарифы
            </Link>
            
            {isAuthenticated ? (
              <>
                <Link to="/dashboard" className="flex items-center space-x-1 text-gray-600 hover:text-gray-900 transition">
                  <LayoutDashboard size={18} />
                  <span>Проекты</span>
                </Link>
                
                <div className="flex items-center space-x-4">
                  <Link to="/settings" className="text-gray-600 hover:text-gray-900 transition">
                    <Settings size={20} />
                  </Link>
                  
                  <div className="flex items-center space-x-3">
                    <img src={user?.avatar} alt={user?.name} className="w-8 h-8 rounded-full" />
                    <span className="text-sm text-gray-700">{user?.name}</span>
                  </div>
                  
                  <button
                    onClick={handleLogout}
                    className="flex items-center space-x-1 text-gray-600 hover:text-red-600 transition"
                  >
                    <LogOut size={18} />
                    <span>Выйти</span>
                  </button>
                </div>
              </>
            ) : (
              <div className="flex items-center space-x-4">
                <Link to="/login" className="text-gray-600 hover:text-gray-900 transition">
                  Войти
                </Link>
                <Link
                  to="/signup"
                  className="bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 transition"
                >
                  Начать бесплатно
                </Link>
              </div>
            )}
          </nav>
        </div>
      </div>
    </header>
  )
}
