#!/bin/bash

# Quick deployment script for German Job Portal Scanner
# This script helps you deploy the app to GitHub and Streamlit Cloud

echo "================================================"
echo "German Job Portal Scanner - Deployment Script"
echo "================================================"
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Error: Git is not installed. Please install Git first."
    exit 1
fi

echo "✅ Git is installed"
echo ""

# Ask for GitHub username
read -p "Enter your GitHub username: " GITHUB_USERNAME

if [ -z "$GITHUB_USERNAME" ]; then
    echo "❌ Error: GitHub username is required"
    exit 1
fi

# Ask for repository name
read -p "Enter repository name (default: german-job-portal-scanner): " REPO_NAME
REPO_NAME=${REPO_NAME:-german-job-portal-scanner}

echo ""
echo "Repository will be created at: https://github.com/$GITHUB_USERNAME/$REPO_NAME"
echo ""

# Check if .git directory exists
if [ -d ".git" ]; then
    echo "⚠️  Git repository already initialized"
    read -p "Do you want to continue? This will add a new remote. (y/n): " continue
    if [ "$continue" != "y" ]; then
        echo "Deployment cancelled"
        exit 0
    fi
else
    echo "📦 Initializing Git repository..."
    git init
fi

echo ""
echo "📝 Adding files to Git..."
git add .

echo ""
echo "💾 Creating commit..."
git commit -m "Deploy: German Job Portal Scanner with advanced filters" || echo "No changes to commit"

echo ""
echo "🔗 Adding GitHub remote..."
git remote add origin "https://github.com/$GITHUB_USERNAME/$REPO_NAME.git" 2>/dev/null || git remote set-url origin "https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"

echo ""
echo "☁️  Setting main branch..."
git branch -M main

echo ""
echo "🚀 Pushing to GitHub..."
echo ""
echo "⚠️  IMPORTANT: You need to create the repository on GitHub first!"
echo "   Go to: https://github.com/new"
echo "   Repository name: $REPO_NAME"
echo "   Keep it public or private (your choice)"
echo "   Don't initialize with README"
echo ""
read -p "Press Enter when you've created the repository on GitHub..."

git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "================================================"
    echo "✅ Successfully deployed to GitHub!"
    echo "================================================"
    echo ""
    echo "📍 Your repository: https://github.com/$GITHUB_USERNAME/$REPO_NAME"
    echo ""
    echo "Next steps:"
    echo "1. Go to https://share.streamlit.io"
    echo "2. Sign in with GitHub"
    echo "3. Click 'New app'"
    echo "4. Select your repository: $REPO_NAME"
    echo "5. Set main file path: app.py"
    echo "6. Click 'Deploy!'"
    echo ""
    echo "Your app will be live at: https://$REPO_NAME.streamlit.app"
    echo ""
    echo "📖 For detailed instructions, see DEPLOYMENT.md"
    echo "================================================"
else
    echo ""
    echo "❌ Error: Failed to push to GitHub"
    echo "   Make sure you've created the repository on GitHub"
    echo "   Repository URL: https://github.com/$GITHUB_USERNAME/$REPO_NAME"
fi
