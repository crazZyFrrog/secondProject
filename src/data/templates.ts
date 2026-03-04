export interface Template {
  id: string
  name: string
  category: string
  isPremium: boolean
  previewImage: string
  description: string
}

export const TEMPLATES: Template[] = [
  {
    id: 'modern-business',
    name: 'Современный Бизнес',
    category: 'Бизнес',
    isPremium: false,
    previewImage: 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=600',
    description: 'Минималистичный шаблон для B2B компаний'
  },
  {
    id: 'creative-agency',
    name: 'Креативное Агентство',
    category: 'Дизайн',
    isPremium: true,
    previewImage: 'https://images.unsplash.com/photo-1561070791-2526d30994b5?w=600',
    description: 'Яркий шаблон для креативных студий'
  },
  {
    id: 'tech-startup',
    name: 'Tech Стартап',
    category: 'IT',
    isPremium: false,
    previewImage: 'https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=600',
    description: 'Современный шаблон для технологических компаний'
  },
  {
    id: 'medical-clinic',
    name: 'Медицинская Клиника',
    category: 'Медицина',
    isPremium: true,
    previewImage: 'https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?w=600',
    description: 'Профессиональный шаблон для медицинских учреждений'
  },
  {
    id: 'real-estate',
    name: 'Недвижимость',
    category: 'Недвижимость',
    isPremium: false,
    previewImage: 'https://images.unsplash.com/photo-1560518883-ce09059eeffa?w=600',
    description: 'Элегантный шаблон для агентств недвижимости'
  },
  {
    id: 'education',
    name: 'Образовательный Центр',
    category: 'Образование',
    isPremium: true,
    previewImage: 'https://images.unsplash.com/photo-1524178232363-1fb2b075b655?w=600',
    description: 'Дружелюбный шаблон для образовательных проектов'
  }
]

export const CATEGORIES = ['Все', 'Бизнес', 'IT', 'Дизайн', 'Медицина', 'Недвижимость', 'Образование']
