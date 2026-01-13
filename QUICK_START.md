# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Option 1: Run Locally

```bash
# Navigate to the app directory
cd job_scraper_app

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

The app will open at `http://localhost:8501`

### Option 2: Deploy to Streamlit Cloud

```bash
# Run the deployment script
./deploy_to_github.sh

# Then follow the prompts to deploy to Streamlit Cloud
```

## 📋 Basic Usage

### 1. Search for Jobs

**Sidebar Controls:**
- **Keywords**: Enter job title (e.g., "Software Engineer")
- **Location**: Enter city (e.g., "Berlin")
- **Job Type**: Select employment type
- **Max Pages**: Choose 1-40 (default: 5)
- **Portals**: Select which portals to search

### 2. Apply Filters

**Advanced Filters (after search):**
- **Company**: Select specific companies
- **Location**: Filter by cities
- **Job Level**: Entry, Mid, Senior, Management
- **Skills**: Filter by required skills
- **Salary**: Show jobs with/without salary info

### 3. View & Export Results

- Click job titles to expand descriptions
- View detected skills and job levels
- Click "View Job" to visit original posting
- Download results as CSV

## 🔧 Key Features at a Glance

| Feature | How to Use |
|---------|-----------|
| Multi-Page Search | Adjust "Maximum Pages" slider (1-40) |
| Debug Mode | Enable "Show Debug Info" checkbox |
| Test Mode | Enable "Test Mode" checkbox |
| Filter by Level | Use "Job Level" multi-select |
| Filter by Skills | Use "Required Skills" multi-select |
| Export Data | Click "Download Results as CSV" |

## 💡 Pro Tips

### Get More Results
- Increase "Maximum Pages" to 20-40
- Use broader keywords ("engineer" vs "senior software engineer")
- Select all three portals

### Find Entry-Level Jobs
1. Search with keywords
2. Apply "Job Level" filter: Select "Entry Level"
3. Results show only junior/entry positions

### Filter by Tech Stack
1. Complete a search
2. Use "Required Skills" filter
3. Select technologies you know (e.g., Python, React)
4. See jobs matching your skills

### Find High-Paying Jobs
1. Run search
2. Set "Salary Info" to "With Salary Info Only"
3. Sort through results

### Troubleshooting
- **No results?** Enable "Test Mode" to verify app works
- **Slow search?** Reduce max pages to 3-5
- **Portal errors?** Check "Debug Info" for details

## 📱 Mobile Usage

The app works on mobile devices:
- Responsive design
- Touch-friendly filters
- Swipe through results

## 🔄 Update Frequency

- **Job data**: Real-time (each search)
- **Portal structures**: May change anytime
- **App updates**: Push to GitHub to deploy

## ⚡ Performance Tips

### Fast Searches (< 30 seconds)
- Max pages: 1-5
- Single portal
- Specific keywords

### Comprehensive Searches (1-3 minutes)
- Max pages: 20-40
- All portals
- Broader keywords

### Balanced Searches (30-60 seconds)
- Max pages: 5-10 (default: 5)
- 2-3 portals
- Specific keywords

## 📊 Understanding Results

### Job Card Information

```
🔍 Software Engineer (Title)
├── Company: TechCorp GmbH
├── Location: Berlin
├── Portal: Indeed.de
├── Level: Mid Level
├── 💰 Salary: €60,000 - €80,000
└── 🔧 Skills: Python, React, AWS, Docker
```

### Statistics Dashboard

- **Total Jobs**: All jobs found across portals
- **Unique Companies**: Number of different employers
- **Portals Scanned**: Active portals searched

### Filter Counter

"Showing 25 of 150 jobs" means:
- 25 jobs match your filters
- 150 total jobs were found

## 🎯 Common Use Cases

### Job Seeker
1. Search with your target role
2. Filter by entry/mid level
3. Filter by your skills
4. Export to track applications

### Recruiter
1. Search with required skills
2. Filter by company (competitors)
3. Analyze salary ranges
4. Export for reporting

### Researcher
1. Broad keyword search
2. High max pages (30-40)
3. All portals enabled
4. Export for data analysis

### Career Switcher
1. Search target role
2. Filter "Entry Level"
3. Check required skills
4. Identify skill gaps

## 🆘 Need Help?

- **Usage Guide**: See [USAGE_GUIDE.md](USAGE_GUIDE.md)
- **Deployment**: See [DEPLOYMENT.md](DEPLOYMENT.md)
- **Features**: See [FEATURES.md](FEATURES.md)
- **Troubleshooting**: See [README.md](README.md)

## ✅ Checklist for First Use

- [ ] Install dependencies
- [ ] Run `streamlit run app.py`
- [ ] Enable "Test Mode" to verify app works
- [ ] Disable "Test Mode" for real search
- [ ] Try a simple search (e.g., "developer" in "Berlin")
- [ ] Experiment with filters
- [ ] Export results to CSV
- [ ] Enable "Debug Mode" to see what's happening

## 🌟 Best Practices

1. **Start Simple**: Begin with test mode
2. **Use Filters**: Don't overwhelm yourself with 1000+ results
3. **Export Data**: Save results for comparison
4. **Check Debug**: When something seems wrong
5. **Be Patient**: Scraping takes time
6. **Respect Limits**: Don't spam searches

## 🔐 Privacy & Security

- ✅ No data stored on servers
- ✅ No tracking or analytics
- ✅ No personal information collected
- ✅ All scraping is client-side
- ✅ Results only visible to you

## 📈 Next Steps

After mastering the basics:
1. Deploy to Streamlit Cloud
2. Share with friends/colleagues
3. Customize filters for your needs
4. Contribute improvements on GitHub
5. Provide feedback for enhancements

Happy job hunting! 🎉
