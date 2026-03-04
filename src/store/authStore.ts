import { create } from 'zustand'

interface User {
  id: string
  name: string
  email: string
  avatar: string
  subscription: 'free' | 'pro' | 'enterprise'
}

interface AuthState {
  user: User | null
  isAuthenticated: boolean
  login: (email: string, password: string) => Promise<void>
  signup: (name: string, email: string, password: string, plan: string) => Promise<void>
  logout: () => void
}

// Mock user data
const MOCK_USER: User = {
  id: '1',
  name: 'Иван Петров',
  email: 'ivan@example.com',
  avatar: 'https://ui-avatars.com/api/?name=Ivan+Petrov&background=0ea5e9&color=fff',
  subscription: 'free'
}

export const useAuthStore = create<AuthState>((set) => ({
  user: localStorage.getItem('user') ? JSON.parse(localStorage.getItem('user')!) : null,
  isAuthenticated: !!localStorage.getItem('user'),
  
  login: async (email: string, _password: string) => {
    // Mock login - в реальном приложении здесь будет API запрос
    await new Promise(resolve => setTimeout(resolve, 500))
    
    const user = { ...MOCK_USER, email }
    localStorage.setItem('user', JSON.stringify(user))
    localStorage.setItem('token', 'mock-token-' + Date.now())
    
    set({ user, isAuthenticated: true })
  },
  
  signup: async (name: string, email: string, _password: string, plan: string) => {
    await new Promise(resolve => setTimeout(resolve, 500))
    
    const user: User = {
      id: Date.now().toString(),
      name,
      email,
      avatar: `https://ui-avatars.com/api/?name=${encodeURIComponent(name)}&background=0ea5e9&color=fff`,
      subscription: plan as 'free' | 'pro' | 'enterprise'
    }
    
    localStorage.setItem('user', JSON.stringify(user))
    localStorage.setItem('token', 'mock-token-' + Date.now())
    
    set({ user, isAuthenticated: true })
  },
  
  logout: () => {
    localStorage.removeItem('user')
    localStorage.removeItem('token')
    set({ user: null, isAuthenticated: false })
  }
}))
