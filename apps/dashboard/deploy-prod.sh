#!/bin/bash

echo "🚀 Deploying Perswade to Production"

# Build and deploy frontend to Vercel
echo "📦 Deploying frontend to Vercel..."
cd frontend
vercel --prod
cd ..

# Deploy backend to Railway/Render
echo "🔧 Deploying backend..."
echo "Manual step: Push to your Git repository and connect to Railway/Render"
echo "Backend deployment URL will be: https://your-app.railway.app"

# Update frontend environment
echo "🔗 Update NEXT_PUBLIC_BACKEND_URL in Vercel environment variables"
echo "Set to your backend deployment URL"

echo "✅ Deployment complete!"
