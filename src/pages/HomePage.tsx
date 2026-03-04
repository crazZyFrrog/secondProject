import { Link } from 'react-router-dom'
import Header from '../components/Header'
import { Sparkles, FileText, Download, Zap, ArrowRight } from 'lucide-react'

export default function HomePage() {
  const features = [
    {
      icon: <FileText className="w-8 h-8 text-primary-600" />,
      title: 'База шаблонов',
      description: 'Более 50 готовых профессиональных шаблонов для любой ниши'
    },
    {
      icon: <Sparkles className="w-8 h-8 text-primary-600" />,
      title: 'AI-генерация',
      description: 'Автоматическое создание контента на основе данных вашей компании'
    },
    {
      icon: <Download className="w-8 h-8 text-primary-600" />,
      title: 'Экспорт документов',
      description: 'Выгрузка в PDF, HTML и DOCX одним кликом'
    },
    {
      icon: <Zap className="w-8 h-8 text-primary-600" />,
      title: 'Без кода',
      description: 'Создавайте лендинги без знаний программирования'
    }
  ]

  const steps = [
    { number: '1', text: 'Выберите шаблон из галереи' },
    { number: '2', text: 'Заполните информацию о компании' },
    { number: '3', text: 'Настройте дизайн и контент' },
    { number: '4', text: 'Экспортируйте готовый лендинг' }
  ]

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />

      {/* Hero Section */}
      <section className="bg-gradient-to-br from-primary-600 to-primary-800 text-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-3xl mx-auto">
            <h1 className="text-5xl font-bold mb-6">
              Создавайте продающие лендинги за минуты
            </h1>
            <p className="text-xl mb-8 text-primary-100">
              Конструктор лендингов и коммерческих предложений с AI-генерацией контента
            </p>
            <Link
              to="/signup"
              className="inline-flex items-center space-x-2 bg-white text-primary-600 px-8 py-4 rounded-lg text-lg font-semibold hover:bg-gray-100 transition"
            >
              <span>Начать бесплатно</span>
              <ArrowRight size={20} />
            </Link>
            <p className="mt-4 text-sm text-primary-200">
              Без кредитной карты • 3 бесплатных проекта
            </p>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-center mb-12">Возможности платформы</h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, idx) => (
              <div key={idx} className="bg-white p-6 rounded-xl shadow-sm hover:shadow-md transition">
                <div className="mb-4">{feature.icon}</div>
                <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
                <p className="text-gray-600">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* How it works */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-center mb-12">Как это работает</h2>
          <div className="grid md:grid-cols-4 gap-8">
            {steps.map((step, idx) => (
              <div key={idx} className="text-center">
                <div className="w-16 h-16 bg-primary-100 text-primary-600 rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-4">
                  {step.number}
                </div>
                <p className="text-gray-700">{step.text}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-primary-600 text-white">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-4xl font-bold mb-6">
            Готовы создать свой первый лендинг?
          </h2>
          <p className="text-xl mb-8 text-primary-100">
            Присоединяйтесь к тысячам компаний, которые уже используют наш конструктор
          </p>
          <Link
            to="/signup"
            className="inline-flex items-center space-x-2 bg-white text-primary-600 px-8 py-4 rounded-lg text-lg font-semibold hover:bg-gray-100 transition"
          >
            <span>Начать бесплатно</span>
            <ArrowRight size={20} />
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-gray-300 py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-4 gap-8">
            <div>
              <h3 className="text-white font-semibold mb-4">LandingBuilder</h3>
              <p className="text-sm">Конструктор лендингов нового поколения</p>
            </div>
            <div>
              <h4 className="text-white font-semibold mb-4">Продукт</h4>
              <ul className="space-y-2 text-sm">
                <li><Link to="/templates" className="hover:text-white">Шаблоны</Link></li>
                <li><Link to="/pricing" className="hover:text-white">Тарифы</Link></li>
              </ul>
            </div>
            <div>
              <h4 className="text-white font-semibold mb-4">Компания</h4>
              <ul className="space-y-2 text-sm">
                <li><a href="#" className="hover:text-white">О нас</a></li>
                <li><a href="#" className="hover:text-white">Контакты</a></li>
              </ul>
            </div>
            <div>
              <h4 className="text-white font-semibold mb-4">Поддержка</h4>
              <ul className="space-y-2 text-sm">
                <li><a href="#" className="hover:text-white">Помощь</a></li>
                <li><a href="#" className="hover:text-white">Документация</a></li>
              </ul>
            </div>
          </div>
          <div className="border-t border-gray-800 mt-8 pt-8 text-center text-sm">
            <p>&copy; 2026 LandingBuilder. Все права защищены.</p>
          </div>
        </div>
      </footer>
    </div>
  )
}
