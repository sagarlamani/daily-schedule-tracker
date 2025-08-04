# 📅 Daily Schedule Tracker

A comprehensive web application for tracking daily schedules, tasks, and building streaks. Built with Next.js frontend and FastAPI backend.

## ✨ Features

- 🔐 **User Authentication** - Email/password and Google OAuth
- 📝 **Task Management** - Create, edit, complete, and delete tasks
- 🏷️ **Categories** - Organize tasks by categories (Work, Study, Exercise, etc.)
- ⏰ **Time Scheduling** - Set start times and durations for tasks
- ✅ **Task Completion** - Mark tasks as complete with visual feedback
- 🔥 **Streak Tracking** - Build and maintain streaks for motivation
- 📱 **Mobile Responsive** - Works perfectly on all devices
- 🎨 **Modern UI** - Beautiful interface with Tailwind CSS

## 🚀 Tech Stack

### Frontend
- **Next.js 14** - React framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **Framer Motion** - Animations
- **NextAuth.js** - Authentication

### Backend
- **FastAPI** - Python web framework
- **SQLAlchemy** - ORM
- **SQLite** - Database (local) / PostgreSQL (production)
- **JWT** - Authentication tokens
- **Pydantic** - Data validation

## 📦 Installation

### Prerequisites
- Node.js 18+ 
- Python 3.12+
- Git

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/daily-schedule-tracker.git
   cd daily-schedule-tracker
   ```

2. **Setup Backend**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   python setup_database.py --reset
   python main.py
   ```

3. **Setup Frontend**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## 🔧 Environment Variables

### Backend (.env)
```env
DATABASE_URL=sqlite:///./schedule_tracker.db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALLOWED_ORIGINS=http://localhost:3000
ENVIRONMENT=development
```

### Frontend (.env.local)
```env
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=your-nextauth-secret
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
BACKEND_URL=http://localhost:8000
```

## 🚀 Deployment

### Frontend (Vercel)
1. Connect your GitHub repository to Vercel
2. Set environment variables in Vercel dashboard
3. Deploy automatically on push to main branch

### Backend (Railway/Render)
1. Connect your GitHub repository
2. Set environment variables
3. Configure build command: `pip install -r requirements.txt`
4. Set start command: `python main.py`

## 📁 Project Structure

```
daily-schedule-tracker/
├── frontend/                 # Next.js application
│   ├── app/                 # App router pages
│   ├── components/          # React components
│   └── package.json
├── backend/                 # FastAPI application
│   ├── models/             # Database models
│   ├── services/           # Business logic
│   ├── database/           # Database setup
│   └── main.py            # FastAPI app
├── README.md
└── .gitignore
```

## 🔌 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `POST /api/auth/google` - Google OAuth

### Tasks
- `GET /api/tasks` - Get user tasks
- `POST /api/tasks` - Create new task
- `PUT /api/tasks/{id}` - Update task
- `DELETE /api/tasks/{id}` - Delete task
- `POST /api/tasks/{id}/complete` - Mark task complete
- `POST /api/tasks/{id}/uncomplete` - Mark task incomplete

### Categories
- `GET /api/categories` - Get all categories

### Streaks
- `GET /api/streaks` - Get user streaks

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with Next.js and FastAPI
- Styled with Tailwind CSS
- Icons from Lucide React
- Charts with Recharts

## 📞 Support

If you have any questions or need help, please open an issue on GitHub.

---

Made with ❤️ for better productivity and schedule management! 