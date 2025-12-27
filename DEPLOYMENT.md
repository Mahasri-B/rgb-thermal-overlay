# Deployment Guide

This guide provides detailed instructions for deploying the RGB Thermal Overlay Algorithm application to Render and Vercel.

## Prerequisites

- A GitHub account
- A Render account (free tier available)
- A Vercel account (free tier available)
- Your code pushed to a GitHub repository

## Option 1: Deploy to Render (Recommended)

Render is the recommended platform for this application as it fully supports OpenCV and Python dependencies.

### Step 1: Prepare Your Repository

1. Make sure all files are committed to your Git repository:
```bash
git add .
git commit -m "Prepare for deployment"
git push origin main
```

### Step 2: Create Render Account

1. Go to [render.com](https://render.com)
2. Sign up for a free account (or log in if you already have one)
3. Connect your GitHub account when prompted

### Step 3: Create New Web Service

1. In the Render dashboard, click **"New +"** → **"Web Service"**
2. Select your GitHub repository
3. Render will auto-detect the configuration from `render.yaml`

### Step 4: Configure Service Settings

If auto-detection doesn't work, manually configure:

- **Name**: `thermal-overlay-app` (or your preferred name)
- **Environment**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app`
- **Plan**: Free (or paid for better performance)

### Step 5: Environment Variables (Optional)

Render will automatically set:
- `PORT`: Set by Render
- `PYTHON_VERSION`: 3.11.0

### Step 6: Deploy

1. Click **"Create Web Service"**
2. Render will start building and deploying your application
3. Wait for the deployment to complete (usually 5-10 minutes)
4. Your app will be available at: `https://your-app-name.onrender.com`

### Step 7: Verify Deployment

1. Visit your app URL
2. Test the upload functionality
3. Check the logs in Render dashboard if there are any issues

## Option 2: Deploy to Vercel

**⚠️ Important Note**: Vercel has limitations with OpenCV due to binary size constraints. The application may work, but Render is recommended for full functionality.

### Step 1: Install Vercel CLI

```bash
npm install -g vercel
```

### Step 2: Login to Vercel

```bash
vercel login
```

### Step 3: Deploy

From your project directory:

```bash
vercel
```

Follow the prompts:
- Set up and deploy? **Yes**
- Which scope? Select your account
- Link to existing project? **No**
- Project name? `thermal-overlay-app` (or your choice)
- Directory? **./** (current directory)
- Override settings? **No**

### Step 4: Production Deployment

For production:

```bash
vercel --prod
```

### Alternative: Deploy via Vercel Dashboard

1. Go to [vercel.com](https://vercel.com)
2. Sign up or log in
3. Click **"Add New"** → **"Project"**
4. Import your GitHub repository
5. Vercel will auto-detect the `vercel.json` configuration
6. Click **"Deploy"**

### Step 5: Verify Deployment

1. Visit your Vercel deployment URL
2. Test the application functionality
3. Check function logs in Vercel dashboard

## Troubleshooting

### Render Issues

**Issue**: Build fails with OpenCV errors
- **Solution**: Ensure you're using Python 3.11 and the correct OpenCV version in `requirements.txt`

**Issue**: Application times out
- **Solution**: Upgrade to a paid plan or optimize image processing

**Issue**: Static files not loading
- **Solution**: Ensure `static/` and `templates/` folders are in the repository

### Vercel Issues

**Issue**: OpenCV import fails
- **Solution**: OpenCV may not work on Vercel due to binary size. Consider using Render instead.

**Issue**: Function timeout
- **Solution**: Increase timeout in Vercel dashboard settings (max 60s on free tier)

**Issue**: 404 errors
- **Solution**: Check `vercel.json` routing configuration

## Environment Variables

Both platforms support environment variables. You can set them in:

- **Render**: Dashboard → Your Service → Environment
- **Vercel**: Dashboard → Your Project → Settings → Environment Variables

Common variables you might need:
- `FLASK_ENV`: `production`
- `PORT`: Automatically set by platform

## Custom Domain

### Render
1. Go to your service settings
2. Click **"Custom Domains"**
3. Add your domain and follow DNS configuration instructions

### Vercel
1. Go to your project settings
2. Click **"Domains"**
3. Add your domain and configure DNS

## Monitoring & Logs

### Render
- View logs: Dashboard → Your Service → Logs
- Monitor: Dashboard → Your Service → Metrics

### Vercel
- View logs: Dashboard → Your Project → Functions → Logs
- Analytics: Dashboard → Your Project → Analytics

## Updating Your Deployment

### Render
- Push to your main branch → Auto-deploys
- Or manually trigger: Dashboard → Manual Deploy

### Vercel
- Push to your main branch → Auto-deploys
- Or use CLI: `vercel --prod`

## Cost Considerations

### Render Free Tier
- 750 hours/month
- Sleeps after 15 minutes of inactivity
- Good for development/testing

### Vercel Free Tier
- Unlimited deployments
- 100GB bandwidth/month
- Function execution limits

For production use, consider paid plans for better performance and reliability.

## Support

- Render Support: [render.com/docs](https://render.com/docs)
- Vercel Support: [vercel.com/docs](https://vercel.com/docs)
- Project Issues: Open an issue in your repository

