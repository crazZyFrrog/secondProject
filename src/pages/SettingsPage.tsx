import { useState } from 'react'
import Header from '../components/Header'
import { useAuthStore } from '../store/authStore'
import { User, Lock, CreditCard, Bell, Crown } from 'lucide-react'

type Tab = 'profile' | 'security' | 'subscription' | 'notifications'

export default function SettingsPage() {
  const [activeTab, setActiveTab] = useState<Tab>('profile')
  const user = useAuthStore(state => state.user)

  const tabs = [
    { id: 'profile', name: 'Профиль', icon: <User size={20} /> },
    { id: 'security', name: 'Безопасность', icon: <Lock size={20} /> },
    { id: 'subscription', name: 'Подписка', icon: <CreditCard size={20} /> },
    { id: 'notifications', name: 'Уведомления', icon: <Bell size={20} /> }
  ]

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />

      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">Настройки</h1>

        <div className="flex flex-col md:flex-row gap-8">
          {/* Tabs Sidebar */}
          <div className="md:w-64">
            <nav className="space-y-1">
              {tabs.map(tab => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id as Tab)}
                  className={`w-full flex items-center space-x-3 px-4 py-3 rounded-lg transition ${
                    activeTab === tab.id
                      ? 'bg-primary-50 text-primary-700 font-medium'
                      : 'text-gray-700 hover:bg-gray-100'
                  }`}
                >
                  {tab.icon}
                  <span>{tab.name}</span>
                </button>
              ))}
            </nav>
          </div>

          {/* Content Area */}
          <div className="flex-1">
            {/* Profile Tab */}
            {activeTab === 'profile' && (
              <div className="bg-white rounded-xl shadow-sm p-8">
                <h2 className="text-2xl font-bold mb-6">Профиль</h2>
                
                <div className="space-y-6">
                  <div className="flex items-center space-x-4 mb-6">
                    <img src={user?.avatar} alt={user?.name} className="w-20 h-20 rounded-full" />
                    <button className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50">
                      Изменить фото
                    </button>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Имя</label>
                    <input
                      type="text"
                      defaultValue={user?.name}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Email</label>
                    <input
                      type="email"
                      defaultValue={user?.email}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Компания</label>
                    <input
                      type="text"
                      placeholder="Название вашей компании"
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
                    />
                  </div>

                  <button className="bg-primary-600 text-white px-6 py-2 rounded-lg hover:bg-primary-700 transition">
                    Сохранить изменения
                  </button>
                </div>
              </div>
            )}

            {/* Security Tab */}
            {activeTab === 'security' && (
              <div className="bg-white rounded-xl shadow-sm p-8">
                <h2 className="text-2xl font-bold mb-6">Безопасность</h2>
                
                <div className="space-y-6">
                  <div>
                    <h3 className="font-semibold mb-4">Изменить пароль</h3>
                    <div className="space-y-4">
                      <input
                        type="password"
                        placeholder="Текущий пароль"
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
                      />
                      <input
                        type="password"
                        placeholder="Новый пароль"
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
                      />
                      <input
                        type="password"
                        placeholder="Подтвердите новый пароль"
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
                      />
                    </div>
                  </div>

                  <div className="border-t border-gray-200 pt-6">
                    <h3 className="font-semibold mb-4">Двухфакторная аутентификация</h3>
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-gray-700">Включить 2FA для дополнительной защиты</p>
                        <p className="text-sm text-gray-500">Требуется приложение-аутентификатор</p>
                      </div>
                      <button className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50">
                        Настроить
                      </button>
                    </div>
                  </div>

                  <button className="bg-primary-600 text-white px-6 py-2 rounded-lg hover:bg-primary-700 transition">
                    Обновить пароль
                  </button>
                </div>
              </div>
            )}

            {/* Subscription Tab */}
            {activeTab === 'subscription' && (
              <div className="space-y-6">
                <div className="bg-white rounded-xl shadow-sm p-8">
                  <h2 className="text-2xl font-bold mb-6">Текущая подписка</h2>
                  
                  <div className="flex items-center justify-between p-6 bg-gradient-to-r from-primary-50 to-primary-100 rounded-lg mb-6">
                    <div className="flex items-center space-x-4">
                      <Crown className="w-10 h-10 text-primary-600" />
                      <div>
                        <h3 className="text-xl font-bold text-gray-900 capitalize">
                          {user?.subscription} Plan
                        </h3>
                        <p className="text-gray-600">
                          {user?.subscription === 'free' ? 'Бесплатный тариф' : 'Активна до 04 апр 2026'}
                        </p>
                      </div>
                    </div>
                    {user?.subscription === 'free' && (
                      <button className="bg-primary-600 text-white px-6 py-2 rounded-lg hover:bg-primary-700 transition">
                        Обновить до Pro
                      </button>
                    )}
                  </div>

                  <div className="grid md:grid-cols-2 gap-4">
                    <div className="p-4 border border-gray-200 rounded-lg">
                      <div className="text-sm text-gray-600 mb-1">Проекты</div>
                      <div className="text-2xl font-bold text-gray-900">
                        {user?.subscription === 'free' ? '1 / 3' : '5 / ∞'}
                      </div>
                    </div>
                    <div className="p-4 border border-gray-200 rounded-lg">
                      <div className="text-sm text-gray-600 mb-1">Экспорты в месяц</div>
                      <div className="text-2xl font-bold text-gray-900">
                        {user?.subscription === 'free' ? '5 / 10' : '45 / ∞'}
                      </div>
                    </div>
                  </div>
                </div>

                {/* Billing History */}
                <div className="bg-white rounded-xl shadow-sm p-8">
                  <h3 className="text-xl font-semibold mb-4">История платежей</h3>
                  <div className="space-y-3">
                    {user?.subscription !== 'free' ? (
                      [
                        { date: '04 фев 2026', amount: '1990 ₽', status: 'Оплачено' },
                        { date: '04 янв 2026', amount: '1990 ₽', status: 'Оплачено' }
                      ].map((payment, idx) => (
                        <div key={idx} className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
                          <div>
                            <div className="font-medium text-gray-900">{payment.date}</div>
                            <div className="text-sm text-gray-500">{payment.amount}</div>
                          </div>
                          <span className="text-sm text-green-600 font-medium">{payment.status}</span>
                        </div>
                      ))
                    ) : (
                      <p className="text-gray-500 text-center py-8">История платежей пуста</p>
                    )}
                  </div>
                </div>
              </div>
            )}

            {/* Notifications Tab */}
            {activeTab === 'notifications' && (
              <div className="bg-white rounded-xl shadow-sm p-8">
                <h2 className="text-2xl font-bold mb-6">Уведомления</h2>
                
                <div className="space-y-6">
                  {[
                    { label: 'Email уведомления о новых функциях', checked: true },
                    { label: 'Уведомления об экспорте проектов', checked: true },
                    { label: 'Маркетинговые рассылки', checked: false },
                    { label: 'Советы по использованию платформы', checked: true }
                  ].map((notif, idx) => (
                    <label key={idx} className="flex items-center justify-between p-4 border border-gray-200 rounded-lg hover:bg-gray-50 cursor-pointer">
                      <span className="text-gray-700">{notif.label}</span>
                      <input
                        type="checkbox"
                        defaultChecked={notif.checked}
                        className="w-5 h-5 text-primary-600 rounded focus:ring-primary-500"
                      />
                    </label>
                  ))}
                </div>

                <button className="mt-6 bg-primary-600 text-white px-6 py-2 rounded-lg hover:bg-primary-700 transition">
                  Сохранить настройки
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
