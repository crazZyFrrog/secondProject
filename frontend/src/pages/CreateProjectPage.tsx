import { useState } from 'react'
import { useNavigate, useLocation } from 'react-router-dom'
import Header from '../components/Header'
import { TEMPLATES } from '../data/templates'
import { useProjectStore, Project } from '../store/projectStore'
import { ArrowRight, Crown } from 'lucide-react'

export default function CreateProjectPage() {
  const location = useLocation()
  const navigate = useNavigate()
  const addProject = useProjectStore(state => state.addProject)
  
  const preselectedTemplateId = location.state?.templateId
  const [selectedTemplateId, setSelectedTemplateId] = useState(preselectedTemplateId || '')
  const [projectName, setProjectName] = useState('')

  const handleCreate = () => {
    if (!selectedTemplateId || !projectName) {
      alert('Выберите шаблон и введите название проекта')
      return
    }

    const newProject: Project = {
      id: Date.now().toString(),
      name: projectName,
      templateId: selectedTemplateId,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
      status: 'draft',
      thumbnailUrl: TEMPLATES.find(t => t.id === selectedTemplateId)?.previewImage || '',
      data: {
        company: { name: '', logo: '', description: '', mission: '', values: [] },
        products: [],
        audience: [],
        benefits: [],
        pricing: [],
        contacts: { phone: '', email: '', address: '', socials: {} },
        cases: [],
        faq: []
      }
    }

    addProject(newProject)
    navigate(`/projects/${newProject.id}/edit`)
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />

      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">Создать новый проект</h1>

        {/* Project Name */}
        <div className="bg-white rounded-xl shadow-sm p-6 mb-8">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Название проекта
          </label>
          <input
            type="text"
            value={projectName}
            onChange={(e) => setProjectName(e.target.value)}
            placeholder="Например: Лендинг для IT-консалтинга"
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
          />
        </div>

        {/* Template Selection */}
        <div className="bg-white rounded-xl shadow-sm p-6 mb-8">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Выберите шаблон</h2>
          <div className="grid md:grid-cols-3 gap-6">
            {TEMPLATES.map(template => (
              <div
                key={template.id}
                onClick={() => setSelectedTemplateId(template.id)}
                className={`cursor-pointer rounded-lg overflow-hidden border-2 transition ${
                  selectedTemplateId === template.id
                    ? 'border-primary-600 shadow-md'
                    : 'border-gray-200 hover:border-gray-300'
                }`}
              >
                <div className="relative h-32">
                  <img
                    src={template.previewImage}
                    alt={template.name}
                    className="w-full h-full object-cover"
                  />
                  {template.isPremium && (
                    <div className="absolute top-2 right-2 bg-yellow-400 text-yellow-900 px-2 py-1 rounded text-xs font-semibold flex items-center space-x-1">
                      <Crown size={12} />
                      <span>Pro</span>
                    </div>
                  )}
                </div>
                <div className="p-4">
                  <h3 className="font-semibold text-gray-900 mb-1">{template.name}</h3>
                  <p className="text-xs text-gray-600">{template.category}</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex justify-end space-x-4">
          <button
            onClick={() => navigate('/dashboard')}
            className="px-6 py-3 border border-gray-300 rounded-lg hover:bg-gray-50 transition"
          >
            Отмена
          </button>
          <button
            onClick={handleCreate}
            disabled={!selectedTemplateId || !projectName}
            className="flex items-center space-x-2 bg-primary-600 text-white px-6 py-3 rounded-lg hover:bg-primary-700 transition font-medium disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span>Создать проект</span>
            <ArrowRight size={20} />
          </button>
        </div>
      </div>
    </div>
  )
}
