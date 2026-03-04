import { useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import Header from '../components/Header'
import { useProjectStore } from '../store/projectStore'
import { Download, FileText, Code, File, ArrowLeft } from 'lucide-react'

type ExportFormat = 'pdf' | 'html' | 'docx'

export default function ExportPage() {
  const { id } = useParams<{ id: string }>()
  const project = useProjectStore(state => state.getProjectById(id!))
  const [format, setFormat] = useState<ExportFormat>('pdf')
  const [exporting, setExporting] = useState(false)

  const handleExport = () => {
    setExporting(true)
    
    setTimeout(() => {
      alert(`Экспорт в ${format.toUpperCase()} завершен! (это демо-версия)`)
      setExporting(false)
    }, 2000)
  }

  const formats = [
    {
      id: 'pdf',
      name: 'PDF',
      icon: <FileText className="w-8 h-8 text-red-500" />,
      description: 'Универсальный формат для печати и просмотра'
    },
    {
      id: 'html',
      name: 'HTML',
      icon: <Code className="w-8 h-8 text-blue-500" />,
      description: 'Готовый сайт для размещения на хостинге'
    },
    {
      id: 'docx',
      name: 'DOCX',
      icon: <File className="w-8 h-8 text-blue-600" />,
      description: 'Документ Word для редактирования'
    }
  ]

  if (!project) {
    return <div className="min-h-screen flex items-center justify-center">Проект не найден</div>
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />

      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <Link
          to={`/projects/${id}/edit`}
          className="inline-flex items-center space-x-2 text-gray-600 hover:text-gray-900 mb-6"
        >
          <ArrowLeft size={20} />
          <span>Назад к проекту</span>
        </Link>

        <h1 className="text-3xl font-bold text-gray-900 mb-2">Экспорт проекта</h1>
        <p className="text-gray-600 mb-8">{project.name}</p>

        {/* Format Selection */}
        <div className="bg-white rounded-xl shadow-sm p-8 mb-8">
          <h2 className="text-xl font-semibold mb-6">Выберите формат экспорта</h2>
          
          <div className="grid md:grid-cols-3 gap-6 mb-8">
            {formats.map(fmt => (
              <button
                key={fmt.id}
                onClick={() => setFormat(fmt.id as ExportFormat)}
                className={`p-6 rounded-xl border-2 transition text-left ${
                  format === fmt.id
                    ? 'border-primary-600 bg-primary-50'
                    : 'border-gray-200 hover:border-gray-300'
                }`}
              >
                <div className="mb-3">{fmt.icon}</div>
                <h3 className="text-lg font-semibold mb-2">{fmt.name}</h3>
                <p className="text-sm text-gray-600">{fmt.description}</p>
              </button>
            ))}
          </div>

          {/* Export Options */}
          <div className="border-t border-gray-200 pt-6">
            <h3 className="font-semibold mb-4">Настройки экспорта</h3>
            
            {format === 'pdf' && (
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Размер страницы
                  </label>
                  <select className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500">
                    <option>A4</option>
                    <option>Letter</option>
                    <option>A3</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Ориентация
                  </label>
                  <select className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500">
                    <option>Портретная</option>
                    <option>Альбомная</option>
                  </select>
                </div>
              </div>
            )}

            {format === 'html' && (
              <div className="space-y-4">
                <label className="flex items-center space-x-2">
                  <input type="checkbox" className="rounded" defaultChecked />
                  <span className="text-sm text-gray-700">Включить CSS inline</span>
                </label>
                <label className="flex items-center space-x-2">
                  <input type="checkbox" className="rounded" />
                  <span className="text-sm text-gray-700">Минифицировать код</span>
                </label>
              </div>
            )}

            {format === 'docx' && (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Стиль документа
                </label>
                <select className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500">
                  <option>Стандартный</option>
                  <option>Деловой</option>
                  <option>Современный</option>
                </select>
              </div>
            )}
          </div>
        </div>

        {/* Export Button */}
        <button
          onClick={handleExport}
          disabled={exporting}
          className="w-full bg-primary-600 text-white py-4 rounded-lg hover:bg-primary-700 transition font-medium text-lg flex items-center justify-center space-x-2 disabled:opacity-50"
        >
          <Download size={24} />
          <span>{exporting ? 'Экспорт...' : `Скачать ${format.toUpperCase()}`}</span>
        </button>

        {/* Export History */}
        <div className="mt-12 bg-white rounded-xl shadow-sm p-8">
          <h2 className="text-xl font-semibold mb-6">История экспортов</h2>
          <div className="space-y-3">
            {[
              { date: '04 мар 2026', format: 'PDF', size: '2.3 MB' },
              { date: '01 мар 2026', format: 'HTML', size: '1.1 MB' }
            ].map((exp, idx) => (
              <div key={idx} className="flex items-center justify-between p-4 border border-gray-200 rounded-lg hover:bg-gray-50">
                <div className="flex items-center space-x-4">
                  <FileText className="text-gray-400" size={24} />
                  <div>
                    <div className="font-medium text-gray-900">{exp.format}</div>
                    <div className="text-sm text-gray-500">{exp.date} • {exp.size}</div>
                  </div>
                </div>
                <button className="text-primary-600 hover:text-primary-700 font-medium">
                  Скачать
                </button>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
