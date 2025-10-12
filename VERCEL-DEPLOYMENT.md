# 🚀 Vercel Deployment Guide for AI Founder Verification App

This guide provides step-by-step instructions for deploying your AI Founder Verification Flask application to Vercel.

## 📋 Prerequisites

- GitHub repository with your code
- Node.js installed (for Vercel CLI)
- Vercel account

## 🔧 Step 1: Install Vercel CLI

```bash
npm install -g vercel
```

## 🔐 Step 2: Login to Vercel

```bash
vercel login
```

## 📦 Step 3: Deploy Your Application

### Option A: Using the Deployment Script
```bash
./deploy-vercel.sh
```

### Option B: Manual Deployment
```bash
# Navigate to your project directory
cd /path/to/AI-based-founder-verification

# Deploy to Vercel
vercel --prod
```

## 🌐 Step 4: Set Environment Variables

After deployment, you need to set environment variables in the Vercel dashboard:

1. Go to [vercel.com/dashboard](https://vercel.com/dashboard)
2. Select your project
3. Go to "Settings" → "Environment Variables"
4. Add the following variables:

| Variable | Value | Description |
|----------|-------|-------------|
| `FLASK_ENV` | `production` | Flask environment |
| `FLASK_SECRET_KEY` | `your-secret-key-here` | Secret key for Flask sessions |
| `LINKEDIN_EMAIL` | `your-email@example.com` | LinkedIn email for scraping |
| `LINKEDIN_PASSWORD` | `your-password` | LinkedIn password for scraping |

### Using Vercel CLI to set environment variables:

```bash
# Set environment variables
vercel env add FLASK_SECRET_KEY
vercel env add LINKEDIN_EMAIL
vercel env add LINKEDIN_PASSWORD

# Redeploy with new environment variables
vercel --prod
```

## 📁 Vercel-Specific Files

Your project now includes these Vercel-specific files:

- `vercel.json` - Vercel configuration
- `.vercelignore` - Files to ignore during deployment
- `vercel-env-example.json` - Environment variables template
- `deploy-vercel.sh` - Automated deployment script

## 🔍 Configuration Details

### vercel.json Configuration:
- **Python Build**: Uses `@vercel/python` for Flask app
- **Static Files**: Serves CSS, JS, and templates as static files
- **Routes**: All requests routed to Flask app except static files
- **Function Timeout**: 30 seconds maximum execution time
- **Environment**: Production mode enabled

### Key Features:
- ✅ Automatic Python dependency installation
- ✅ Static file serving for CSS/JS/templates
- ✅ Environment variable support
- ✅ Custom domain support
- ✅ Automatic HTTPS
- ✅ Global CDN

## 🚀 Deployment Process

1. **Build Phase**: Vercel installs Python dependencies from `requirements.txt`
2. **Static Files**: CSS, JS, and templates are served as static assets
3. **Function**: Flask app runs as a serverless function
4. **Routing**: All requests are handled by your Flask application

## 🔧 Troubleshooting

### Common Issues:

1. **Import Errors**: Ensure all dependencies are in `requirements.txt`
2. **Environment Variables**: Check they're set in Vercel dashboard
3. **Function Timeout**: Increase `maxDuration` in `vercel.json` if needed
4. **Static Files**: Verify paths in `vercel.json` routes

### Debug Commands:
```bash
# Check deployment status
vercel ls

# View logs
vercel logs

# Check environment variables
vercel env ls

# Remove deployment
vercel remove
```

## 📊 Vercel Free Tier Limits

- **Bandwidth**: 100GB/month
- **Function Execution**: 100GB-hours/month
- **Function Duration**: 10 seconds (can extend to 30s)
- **Builds**: Unlimited
- **Custom Domains**: Unlimited

## 🎯 After Deployment

1. **Test Your App**: Visit the provided Vercel URL
2. **Set Custom Domain**: Add your domain in Vercel dashboard
3. **Monitor Usage**: Check bandwidth and function usage
4. **Set up Analytics**: Enable Vercel Analytics for insights

## 🔄 Redeployment

To redeploy after making changes:

```bash
git add .
git commit -m "Update application"
git push origin main
vercel --prod
```

## 📞 Support

- **Vercel Documentation**: [vercel.com/docs](https://vercel.com/docs)
- **Vercel Community**: [github.com/vercel/vercel/discussions](https://github.com/vercel/vercel/discussions)
- **Flask on Vercel**: [vercel.com/docs/frameworks/flask](https://vercel.com/docs/frameworks/flask)

---

**Happy Deploying! 🚀**
