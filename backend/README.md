# Backend - Landing Constructor API

Бэкенд для конструктора лендингов.

## Планируемый стек

- **Node.js** + **Express** или **NestJS**
- **PostgreSQL** / **MongoDB** для базы данных
- **JWT** для аутентификации
- **OpenAI API** для AI-генерации контента
- **AWS S3** / **Cloudinary** для хранения изображений

## Структура (планируется)

```
backend/
├── src/
│   ├── controllers/     # Контроллеры API
│   ├── models/          # Модели данных
│   ├── routes/          # Роуты API
│   ├── services/        # Бизнес-логика
│   ├── middleware/      # Middleware (auth, validation)
│   ├── config/          # Конфигурация
│   └── utils/           # Утилиты
├── package.json
└── README.md
```

## API Endpoints (планируется)

### Аутентификация
- `POST /api/auth/register` - Регистрация
- `POST /api/auth/login` - Вход
- `POST /api/auth/logout` - Выход
- `GET /api/auth/me` - Получить текущего пользователя

### Проекты
- `GET /api/projects` - Список проектов пользователя
- `POST /api/projects` - Создать проект
- `GET /api/projects/:id` - Получить проект
- `PUT /api/projects/:id` - Обновить проект
- `DELETE /api/projects/:id` - Удалить проект

### Шаблоны
- `GET /api/templates` - Список шаблонов
- `GET /api/templates/:id` - Получить шаблон

### AI-генерация
- `POST /api/ai/generate` - Генерация контента через AI

### Экспорт
- `POST /api/export/pdf` - Экспорт в PDF
- `POST /api/export/html` - Экспорт в HTML
- `POST /api/export/docx` - Экспорт в DOCX

## Установка (когда будет реализовано)

```bash
cd backend
npm install
npm run dev
```

## Переменные окружения

```env
PORT=5000
DATABASE_URL=postgresql://...
JWT_SECRET=your-secret-key
OPENAI_API_KEY=your-openai-key
AWS_ACCESS_KEY_ID=your-aws-key
AWS_SECRET_ACCESS_KEY=your-aws-secret
```

---

**Статус:** В разработке
