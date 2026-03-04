import { create } from 'zustand'

export interface Project {
  id: string
  name: string
  templateId: string
  createdAt: string
  updatedAt: string
  status: 'draft' | 'completed'
  thumbnailUrl: string
  data: {
    company: {
      name: string
      logo: string
      description: string
      mission: string
      values: string[]
    }
    products: Array<{
      id: string
      name: string
      description: string
      price: string
      image: string
    }>
    audience: Array<{
      id: string
      segment: string
      description: string
      pains: string[]
      needs: string[]
    }>
    benefits: Array<{
      id: string
      icon: string
      title: string
      description: string
    }>
    pricing: Array<{
      id: string
      name: string
      price: string
      period: string
      features: string[]
      isRecommended: boolean
    }>
    contacts: {
      phone: string
      email: string
      address: string
      socials: { [key: string]: string }
    }
    cases: Array<{
      id: string
      title: string
      client: string
      challenge: string
      solution: string
      results: string
      images: string[]
    }>
    faq: Array<{
      id: string
      question: string
      answer: string
    }>
  }
}

interface ProjectState {
  projects: Project[]
  currentProject: Project | null
  addProject: (project: Project) => void
  updateProject: (id: string, updates: Partial<Project>) => void
  deleteProject: (id: string) => void
  setCurrentProject: (id: string) => void
  getProjectById: (id: string) => Project | undefined
}

// Mock projects
const MOCK_PROJECTS: Project[] = [
  {
    id: '1',
    name: 'IT Консалтинг Проект',
    templateId: 'modern-business',
    createdAt: '2026-03-01T10:00:00Z',
    updatedAt: '2026-03-04T15:30:00Z',
    status: 'draft',
    thumbnailUrl: 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=400',
    data: {
      company: {
        name: 'TechSolutions',
        logo: '',
        description: 'Мы помогаем компаниям внедрять современные IT-решения',
        mission: 'Делать технологии доступными для каждого бизнеса',
        values: ['Инновации', 'Качество', 'Клиентоориентированность']
      },
      products: [],
      audience: [],
      benefits: [],
      pricing: [],
      contacts: { phone: '', email: '', address: '', socials: {} },
      cases: [],
      faq: []
    }
  }
]

export const useProjectStore = create<ProjectState>((set, get) => ({
  projects: localStorage.getItem('projects') 
    ? JSON.parse(localStorage.getItem('projects')!) 
    : MOCK_PROJECTS,
  currentProject: null,
  
  addProject: (project) => {
    set(state => {
      const newProjects = [...state.projects, project]
      localStorage.setItem('projects', JSON.stringify(newProjects))
      return { projects: newProjects }
    })
  },
  
  updateProject: (id, updates) => {
    set(state => {
      const newProjects = state.projects.map(p => 
        p.id === id ? { ...p, ...updates, updatedAt: new Date().toISOString() } : p
      )
      localStorage.setItem('projects', JSON.stringify(newProjects))
      return { 
        projects: newProjects,
        currentProject: state.currentProject?.id === id 
          ? { ...state.currentProject, ...updates } 
          : state.currentProject
      }
    })
  },
  
  deleteProject: (id) => {
    set(state => {
      const newProjects = state.projects.filter(p => p.id !== id)
      localStorage.setItem('projects', JSON.stringify(newProjects))
      return { projects: newProjects }
    })
  },
  
  setCurrentProject: (id) => {
    const project = get().projects.find(p => p.id === id)
    set({ currentProject: project || null })
  },
  
  getProjectById: (id) => {
    return get().projects.find(p => p.id === id)
  }
}))
