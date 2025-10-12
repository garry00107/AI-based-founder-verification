# 🚀 AI Founder Verification App - Deployment Guide

This guide provides multiple free deployment options for the AI Founder Verification Flask application.

## 📋 Prerequisites

- Git repository with your code
- Python 3.12+ environment
- Required environment variables configured

## 🌐 Free Deployment Options

### 1. Render (Recommended - Free Tier Available)

**Steps:**
1. Go to [render.com](https://render.com) and sign up
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: `ai-founder-verification`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn --bind 0.0.0.0:$PORT app:app`

**Environment Variables to Set:**
```
FLASK_ENV=production
FLASK_SECRET_KEY=your-secret-key-here
LINKEDIN_EMAIL=your-email@example.com
LINKEDIN_PASSWORD=your-password
```

### 2. Railway

**Steps:**
1. Go to [railway.app](https://railway.app) and sign up
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Railway will auto-detect Python and deploy

**Environment Variables:**
Set the same variables as Render above.

### 3. PythonAnywhere

**Steps:**
1. Go to [pythonanywhere.com](https://pythonanywhere.com) and sign up
2. Go to "Web" tab → "Add a new web app"
3. Choose "Manual configuration" → "Python 3.12"
4. Upload your files via "Files" tab
5. Install dependencies in "Console" tab:
   ```bash
   pip3.12 install --user -r requirements.txt
   ```
6. Configure WSGI file in "Web" tab

### 4. Vercel (Alternative)

**Steps:**
1. Go to [vercel.com](https://vercel.com) and sign up
2. Import your GitHub repository
3. Vercel will auto-detect Python and deploy using `vercel.json`

## 🔧 Environment Variables

Set these in your hosting platform's environment variables section:

```bash
FLASK_ENV=production
FLASK_SECRET_KEY=your-secret-key-here
LINKEDIN_EMAIL=your-email@example.com
LINKEDIN_PASSWORD=your-password
PORT=5000
```

## 📁 Required Files

Make sure these files are in your repository root:

- `app.py` - Main Flask application
- `requirements.txt` - Python dependencies
- `Procfile` - Process file for deployment
- `runtime.txt` - Python version specification
- `vercel.json` - Vercel configuration
- `railway.json` - Railway configuration

## 🚀 Quick Deploy Commands

### For Render:
```bash
# Just push to GitHub and connect via Render dashboard
git push origin main
```

### For Railway:
```bash
railway login
railway init
railway up
```

### For Vercel:
```bash
vercel --prod
```

## 🔍 Troubleshooting

### Common Issues:

1. **Build Failures**: Check Python version compatibility
2. **Import Errors**: Ensure all dependencies are in requirements.txt
3. **Port Issues**: Use `$PORT` environment variable
4. **Memory Issues**: Some free tiers have memory limits

### Debug Commands:
```bash
# Check logs
railway logs

# Local testing
python app.py

# Check dependencies
pip install -r requirements.txt
```

## 📊 Free Tier Limitations

- **Render**: 750 hours/month, sleeps after inactivity
- **Railway**: $5 credit monthly, limited usage
- **PythonAnywhere**: 1 web app, 3 months free, then $5/month
- **Vercel**: 100GB bandwidth/month, serverless functions

## 🎯 Recommended Deployment Order

1. **Render** - Most reliable free tier
2. **Railway** - Good alternative with generous limits
3. **PythonAnywhere** - Best for learning and development
4. **Vercel** - Good for API-focused apps

## 📞 Support

If you encounter issues:
1. Check the hosting platform's documentation
2. Review build logs for specific errors
3. Ensure all environment variables are set
4. Test locally before deploying

---

**Happy Deploying! 🚀**
