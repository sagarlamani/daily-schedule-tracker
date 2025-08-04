# 🚀 Deployment Guide

This guide will help you deploy your Daily Schedule Tracker application to production.

## 📋 Prerequisites

- GitHub account
- Vercel account (free tier available)
- Railway account (free tier available) or Render account
- Google OAuth credentials (optional but recommended)

## 🎯 Deployment Strategy

We'll deploy:
- **Frontend**: Vercel (Next.js optimized)
- **Backend**: Railway/Render (Python FastAPI)
- **Database**: PostgreSQL (provided by Railway/Render)

## 🔧 Step 1: Prepare Your Repository

### 1.1 Initialize Git Repository
```bash
cd daily-schedule-tracker
git init
git add .
git commit -m "Initial commit"
```

### 1.2 Create GitHub Repository
1. Go to [GitHub](https://github.com)
2. Click "New repository"
3. Name it `daily-schedule-tracker`
4. Don't initialize with README (we already have one)
5. Click "Create repository"

### 1.3 Push to GitHub
```bash
git remote add origin https://github.com/yourusername/daily-schedule-tracker.git
git branch -M main
git push -u origin main
```

## 🔐 Step 2: Set Up Google OAuth (Optional)

### 2.1 Create Google OAuth Credentials
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable Google+ API
4. Go to "Credentials" → "Create Credentials" → "OAuth 2.0 Client IDs"
5. Set application type to "Web application"
6. Add authorized redirect URIs:
   - `http://localhost:3000/api/auth/callback/google` (development)
   - `https://your-app.vercel.app/api/auth/callback/google` (production)
7. Copy Client ID and Client Secret

## 🚀 Step 3: Deploy Backend (Railway)

### 3.1 Deploy to Railway
1. Go to [Railway](https://railway.app/)
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your `daily-schedule-tracker` repository
5. Set root directory to `backend`
6. Click "Deploy"

### 3.2 Configure Environment Variables
In Railway dashboard, add these environment variables:

```env
DATABASE_URL=postgresql://... (Railway will provide this)
SECRET_KEY=your-super-secret-key-here-make-it-long-and-random
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALLOWED_ORIGINS=https://your-frontend-domain.vercel.app
ENVIRONMENT=production
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
```

### 3.3 Get Backend URL
Railway will provide a URL like: `https://your-app-production.up.railway.app`

## 🌐 Step 4: Deploy Frontend (Vercel)

### 4.1 Deploy to Vercel
1. Go to [Vercel](https://vercel.com/)
2. Sign up with GitHub
3. Click "New Project"
4. Import your `daily-schedule-tracker` repository
5. Set root directory to `frontend`
6. Click "Deploy"

### 4.2 Configure Environment Variables
In Vercel dashboard, add these environment variables:

```env
NEXTAUTH_URL=https://your-app.vercel.app
NEXTAUTH_SECRET=your-nextauth-secret-key-here
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
BACKEND_URL=https://your-backend-url.up.railway.app
NODE_ENV=production
```

### 4.3 Update CORS Settings
Update your backend's `ALLOWED_ORIGINS` to include your Vercel domain:
```env
ALLOWED_ORIGINS=https://your-app.vercel.app
```

## 🔄 Step 5: Update Frontend API Calls

### 5.1 Update API URLs
Update all frontend API calls to use the production backend URL:

```typescript
// Instead of http://localhost:8000
const API_BASE = process.env.BACKEND_URL || 'https://your-backend-url.up.railway.app'
```

### 5.2 Commit and Push Changes
```bash
git add .
git commit -m "Update for production deployment"
git push
```

## ✅ Step 6: Test Your Deployment

### 6.1 Test Frontend
1. Visit your Vercel URL
2. Test registration/login
3. Test task creation and completion
4. Test on mobile device

### 6.2 Test Backend
1. Visit `https://your-backend-url.up.railway.app/health`
2. Should return `{"status": "healthy"}`

### 6.3 Test API Documentation
1. Visit `https://your-backend-url.up.railway.app/docs`
2. Test API endpoints

## 🔧 Alternative: Deploy to Render

If you prefer Render over Railway:

### Render Backend Deployment
1. Go to [Render](https://render.com/)
2. Create new "Web Service"
3. Connect your GitHub repository
4. Set root directory to `backend`
5. Build command: `pip install -r requirements.txt`
6. Start command: `python main.py`
7. Add environment variables (same as Railway)

## 🚨 Troubleshooting

### Common Issues

1. **CORS Errors**
   - Check `ALLOWED_ORIGINS` in backend
   - Ensure frontend URL is included

2. **Database Connection**
   - Verify `DATABASE_URL` is correct
   - Check if database is accessible

3. **Authentication Issues**
   - Verify Google OAuth credentials
   - Check redirect URIs

4. **Build Failures**
   - Check Python version (3.12+)
   - Verify all dependencies in requirements.txt

### Debug Commands

```bash
# Check backend logs
railway logs

# Check frontend build
vercel logs

# Test API locally
curl https://your-backend-url.up.railway.app/health
```

## 📱 PWA Features

Your app is already PWA-ready! Users can:
- Install it on their mobile devices
- Use it offline (basic functionality)
- Get app-like experience

## 🔄 Continuous Deployment

Both Vercel and Railway will automatically redeploy when you push to the main branch.

## 📊 Monitoring

- **Vercel**: Built-in analytics and performance monitoring
- **Railway**: Logs and metrics in dashboard
- **Custom**: Add monitoring tools like Sentry for error tracking

## 🎉 Congratulations!

Your Daily Schedule Tracker is now live and ready to use! 

**Frontend**: https://your-app.vercel.app  
**Backend**: https://your-backend-url.up.railway.app  
**API Docs**: https://your-backend-url.up.railway.app/docs

---

Need help? Check the troubleshooting section or open an issue on GitHub! 