# Deployment Guide - German Job Portal Scanner

This guide explains how to deploy the job scraper app to Streamlit Cloud.

## Prerequisites

1. GitHub account
2. Streamlit Cloud account (free at [share.streamlit.io](https://share.streamlit.io))
3. Git installed on your local machine

## Step 1: Prepare Your Repository

### 1.1 Initialize Git Repository (if not already done)

```bash
cd job_scraper_app
git init
```

### 1.2 Create GitHub Repository

1. Go to [github.com](https://github.com) and create a new repository
2. Name it: `german-job-portal-scanner` (or any name you prefer)
3. Keep it public or private (your choice)
4. Don't initialize with README (we already have one)

### 1.3 Add Files and Push to GitHub

```bash
# Add all files
git add .

# Commit
git commit -m "Initial commit: German Job Portal Scanner with advanced filters"

# Add remote repository (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/german-job-portal-scanner.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 2: Deploy to Streamlit Cloud

### 2.1 Sign Up / Log In to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Authorize Streamlit to access your repositories

### 2.2 Create New App

1. Click "New app" button
2. Fill in the deployment settings:
   - **Repository**: Select your `german-job-portal-scanner` repository
   - **Branch**: `main`
   - **Main file path**: `app.py`
   - **App URL** (optional): Choose a custom subdomain

3. Click "Deploy!"

### 2.3 Wait for Deployment

- First deployment takes 2-5 minutes
- Streamlit Cloud will install dependencies from `requirements.txt`
- You'll see build logs in real-time

## Step 3: Access Your Deployed App

Once deployment is complete:

- Your app will be live at: `https://your-app-name.streamlit.app`
- Share this URL with anyone!
- App will auto-update when you push changes to GitHub

## Configuration

### App Settings

The app configuration is in `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"
```

You can customize colors and theme as needed.

### Environment Variables (Optional)

If you need to add secrets or environment variables:

1. Go to your app settings on Streamlit Cloud
2. Click "Secrets" in the left sidebar
3. Add secrets in TOML format:

```toml
# Example secrets (if needed in future)
[api_keys]
some_api_key = "your-key-here"
```

## Updating Your Deployed App

To update the app after making changes:

```bash
# Make your changes
# Then commit and push

git add .
git commit -m "Description of changes"
git push origin main
```

Streamlit Cloud will automatically detect changes and redeploy!

## Resource Limits (Free Tier)

Streamlit Cloud free tier includes:

- **CPU**: 1 CPU core
- **Memory**: 1 GB RAM
- **Bandwidth**: Unlimited
- **Apps**: Unlimited public apps
- **Sleep**: Apps sleep after 7 days of inactivity

**Important Notes:**
- App may be slow with many concurrent users
- Consider upgrading to paid tier for better performance
- App will wake up when accessed (takes ~30 seconds)

## Troubleshooting

### App Won't Start

1. Check build logs in Streamlit Cloud dashboard
2. Verify `requirements.txt` has all dependencies
3. Check for Python version compatibility

### Memory Issues

If app crashes due to memory:
- Reduce `max_pages` default value in sidebar
- Implement caching for results
- Consider pagination for large result sets

### Scraping Issues

Some job portals may block requests from cloud IPs:
- This is expected behavior
- Enable "Test Mode" to verify app functionality
- Use debug mode to see which portals are working

### Performance Optimization

To improve performance:

```python
# Add caching to app.py
@st.cache_data(ttl=3600)  # Cache for 1 hour
def cached_scrape(keywords, location, ...):
    return scrape_all_portals(keywords, location, ...)
```

## Custom Domain (Optional)

To use a custom domain:

1. Upgrade to Streamlit Cloud paid plan
2. Go to app settings
3. Add your custom domain
4. Update DNS records as instructed

## Monitoring

Monitor your app:

1. **Usage Stats**: Check Streamlit Cloud dashboard
2. **Logs**: View real-time logs in browser
3. **Errors**: Streamlit shows errors in app UI

## Security Best Practices

1. **Never commit secrets**: Use Streamlit secrets management
2. **Respect robots.txt**: App already includes delays
3. **Rate limiting**: Built into scrapers
4. **User data**: App doesn't store user data

## Alternative Deployment Options

### Heroku

If you prefer Heroku:

1. Create `Procfile`:
```
web: streamlit run app.py --server.port=$PORT
```

2. Create `setup.sh`:
```bash
mkdir -p ~/.streamlit/
echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
" > ~/.streamlit/config.toml
```

3. Deploy to Heroku:
```bash
heroku create your-app-name
git push heroku main
```

### Docker

Create `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]
```

Build and run:
```bash
docker build -t job-scraper .
docker run -p 8501:8501 job-scraper
```

## Support

For issues with:
- **Streamlit Cloud**: [docs.streamlit.io](https://docs.streamlit.io)
- **This App**: Check [README.md](README.md) troubleshooting section

## Cost Optimization

To minimize costs on paid tiers:

1. **Cache results**: Reduce API calls
2. **Limit pages**: Default to 5 pages max
3. **Auto-sleep**: Let app sleep when not in use
4. **Compress data**: Minimize memory usage

## Maintenance

Regular maintenance tasks:

1. **Update dependencies**: Monthly updates recommended
2. **Check scrapers**: Portal structures change
3. **Monitor errors**: Review logs weekly
4. **User feedback**: Track issues and requests

## Backup Strategy

Recommended backups:

1. **Code**: Always in GitHub
2. **Config**: Store `.streamlit/config.toml` separately
3. **Docs**: Keep documentation updated

Your app is now live and accessible worldwide! 🚀
