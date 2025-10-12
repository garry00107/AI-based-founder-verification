#!/bin/bash

# Vercel Deployment Script for AI Founder Verification App

echo "🚀 Deploying AI Founder Verification App to Vercel..."

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI not found. Installing..."
    npm install -g vercel
fi

# Login to Vercel (if not already logged in)
echo "🔐 Checking Vercel authentication..."
vercel whoami &> /dev/null
if [ $? -ne 0 ]; then
    echo "Please login to Vercel..."
    vercel login
fi

# Deploy to Vercel
echo "📦 Deploying to Vercel..."
vercel --prod

echo "✅ Deployment complete!"
echo "🔗 Your app should be available at the provided URL"
echo ""
echo "📋 Next steps:"
echo "1. Set environment variables in Vercel dashboard:"
echo "   - FLASK_SECRET_KEY"
echo "   - LINKEDIN_EMAIL" 
echo "   - LINKEDIN_PASSWORD"
echo "2. Redeploy after setting environment variables"
echo "3. Test your application"
