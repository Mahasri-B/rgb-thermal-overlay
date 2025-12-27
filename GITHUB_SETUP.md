# GitHub Repository Setup & Deployment Guide

## Step 1: Create GitHub Repository

1. Go to https://github.com/Mahasri-B
2. Click the **"+"** icon in the top right → **"New repository"**
3. Repository settings:
   - **Repository name**: `rgb-thermal-overlay` (or any name you prefer)
   - **Description**: "RGB Thermal Overlay Algorithm - Professional Image Alignment Tool"
   - **Visibility**: Public (or Private if you prefer)
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)
4. Click **"Create repository"**

## Step 2: Push Your Code

After creating the repository, run these commands in your terminal:

```bash
cd "C:\Users\marsh\Desktop\Task 1 - RGB Thermal Overlay Algorithm"
git remote set-url origin https://github.com/Mahasri-B/YOUR-REPO-NAME.git
git push -u origin main
```

Replace `YOUR-REPO-NAME` with the actual repository name you created.

**OR** if you used the name `rgb-thermal-overlay`, just run:
```bash
git push -u origin main
```

## Step 3: Deploy to Render (Recommended)

### Option A: Using Render Dashboard

1. Go to https://render.com and sign up/login
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub account if not already connected
4. Select your repository: `rgb-thermal-overlay`
5. Render will auto-detect settings from `render.yaml`
6. Configure if needed:
   - **Name**: `rgb-thermal-overlay` (or your choice)
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
7. Click **"Create Web Service"**
8. Wait 5-10 minutes for deployment
9. Your app will be live at: `https://your-app-name.onrender.com`

### Option B: Using Render CLI (Alternative)

```bash
# Install Render CLI (if you want)
npm install -g render-cli

# Or use the dashboard method above
```

## Step 4: Deploy to Vercel (Optional)

**Note**: Vercel may have limitations with OpenCV. Render is recommended.

1. Go to https://vercel.com and sign up/login
2. Click **"Add New"** → **"Project"**
3. Import your GitHub repository
4. Vercel will auto-detect `vercel.json`
5. Click **"Deploy"**
6. Your app will be live at: `https://your-app-name.vercel.app`

## Your Repository URL

Once pushed, your code will be available at:
**https://github.com/Mahasri-B/rgb-thermal-overlay**

## Quick Commands Reference

```bash
# Check status
git status

# Add changes
git add .

# Commit changes
git commit -m "Your commit message"

# Push to GitHub
git push origin main

# View your repository
# https://github.com/Mahasri-B/rgb-thermal-overlay
```

## What Changed

✅ **Output now returns only `aligned_AT.JPG`** (single image file, not ZIP)
✅ **Professional frontend** with modern UI
✅ **Ready for deployment** on Render and Vercel
✅ **All configuration files** included

## Next Steps After Deployment

1. Test your deployed app
2. Share the URL with others
3. Monitor usage in Render/Vercel dashboard
4. Update code and push - auto-deploys on Render/Vercel

