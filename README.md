# Global Job Portal Scanner

A Streamlit web application that scans and scrapes job portals across multiple countries to find available positions based on user-defined parameters.

## Features

### Core Features
- **Multiple Portal Support**: Scrapes Indeed, StepStone, XING Jobs, Monster, and LinkedIn
- **Multi-Country Search**: Search jobs in Germany, USA, Canada, UK, and Europe
- **Multi-Page Scraping**: Search through up to 100 pages per portal (configurable, default: 5)
- **Real-time Search**: Live scraping of job listings with progress tracking
- **Export Functionality**: Download results as CSV with all metadata

### Advanced Filtering
- **Company Filter**: Filter by specific companies
- **Location Filter**: Filter by job locations within Germany
- **Job Level Filter**: Filter by Entry Level, Mid Level, Senior Level, or Management
- **Skills Filter**: Filter jobs by required technical skills (Python, Java, React, AWS, etc.)
- **Salary Filter**: Show only jobs with salary information or without
- **Portal Filter**: Filter by specific job portal
- **Job Posting Age Filter**: Filter by how recently jobs were posted (Last 24 Hours, 3/7/14/30 Days)

### Additional Features
- **Smart Skill Detection**: Automatically extracts technical skills from job descriptions
- **Job Level Classification**: Identifies seniority level from title and description
- **Salary Information**: Displays salary when available
- **Job Posting Date**: Shows when each job was posted with relative time (e.g., "2 days ago", "Today")
- **Clean Interface**: User-friendly Streamlit interface with pagination
- **Statistics Dashboard**: View total jobs, unique companies, and portals scanned
- **Debug Mode**: Detailed debugging information to troubleshoot scraping issues
- **Test Mode**: Sample data for testing the app without making real requests

## Installation

1. Navigate to the project directory:
```bash
cd job_scraper_app
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the Streamlit app:
```bash
streamlit run app.py
```

2. The app will open in your default browser (usually at http://localhost:8501)

3. In the sidebar, enter:
   - **Country/Region**: Select Germany, USA, Canada, UK, or Europe
   - **Job Title/Keywords**: e.g., "Software Engineer", "Data Analyst"
   - **Location**: e.g., "Berlin", "New York", "Toronto", "London"
   - **Job Type**: Full-time, Part-time, Remote, etc.
   - **Maximum Pages**: 1-100 pages per portal (default: 5)
   - **Select Portals**: Choose which job portals to scan (varies by country)
   - **Debug Mode**: Enable to see detailed scraping information
   - **Test Mode**: Enable to use sample data instead of real scraping

4. Click "Search Jobs" and wait for results

5. Use filters to refine results and download as CSV if needed

## Supported Job Portals

### Germany (Fully Supported) 🇩🇪
1. **Indeed.de** - Germany's largest job search engine
2. **StepStone.de** - Leading German job board
3. **XING Jobs** - Professional network and job platform
4. **Monster.de** - Global job portal (Germany)
5. **Arbeitsagentur.de** - German Federal Employment Agency (official government portal)

### USA 🇺🇸
- Indeed.com, Monster.com, Glassdoor, CareerBuilder
- ⚠️ Limited scraping support - some portals may not work

### Canada 🇨🇦
- Indeed.ca, Monster.ca, Workopolis, Job Bank
- ⚠️ Limited scraping support - some portals may not work

### UK 🇬🇧
- Indeed.co.uk, Reed.co.uk, TotalJobs, CV-Library
- ⚠️ Limited scraping support - some portals may not work

### Europe 🇪🇺
- Indeed.de, StepStone.de, Monster.de, EuroJobs, Jobrapido
- ⚠️ Multi-country search - adjust location for specific cities

## Project Structure

```
job_scraper_app/
├── app.py                  # Main Streamlit application with UI
├── scrapers.py             # Job scraper modules for each portal
├── sample_data.py          # Sample data generator for testing
├── test_scrapers.py        # Testing utility for debugging scrapers
├── requirements.txt        # Python dependencies
├── packages.txt            # System packages for deployment
├── README.md              # This file
├── DEPLOYMENT.md          # Deployment guide for Streamlit Cloud
├── USAGE_GUIDE.md         # Detailed usage instructions
├── .gitignore             # Git ignore file
└── .streamlit/
    └── config.toml        # Streamlit configuration
```

## How It Works

1. **User Input**: Users specify search parameters through the Streamlit interface
2. **Multi-Page Scraping**: The app iterates through multiple result pages on each portal
3. **Intelligent Parsing**: Multiple fallback selectors ensure compatibility with site changes
4. **Deduplication**: Automatically removes duplicate job listings across pages
5. **Display**: Results are formatted and displayed with filtering options
6. **Export**: Users can download results as CSV for further analysis

The app scrapes up to 40 pages per portal (configurable), with automatic pagination detection and respectful delays between requests.

## Important Notes

- **Rate Limiting**: The app includes respectful delays between requests to avoid overloading servers
- **Structure Changes**: Job portal HTML structures may change, which could affect scraping
- **Legal Compliance**: Ensure you comply with each portal's Terms of Service
- **Robots.txt**: Respect robots.txt rules of each website

## Limitations

- Some job portals may block automated scraping
- Results are limited to prevent excessive requests
- Some portals require JavaScript rendering (consider Selenium for advanced scraping)
- Job descriptions may be truncated; full details available on source portals

## Deployment

The app is ready for deployment to Streamlit Cloud. See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

### Quick Deploy to Streamlit Cloud

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Set main file to `app.py`
5. Click Deploy!

Your app will be live at `https://your-app-name.streamlit.app`

## Future Enhancements

- Add more German job portals (Monster.de, LinkedIn Jobs, etc.)
- Implement Selenium for JavaScript-heavy sites
- Add job alerts and email notifications
- Store job history in a database
- Advanced salary range filtering and comparison
- Save favorite jobs and search queries
- Job application tracking

## Troubleshooting

### No Jobs Found

If you're getting "No jobs found matching your criteria", try these steps:

1. **Enable Debug Mode**:
   - Check the "Show Debug Info" checkbox in the sidebar
   - This will show you exactly what happened with each portal
   - Look at HTTP status codes, errors, and which selectors were tried

2. **Use Test Mode**:
   - Enable "Test Mode (Use Sample Data)" in the sidebar
   - This tests the app interface with sample data to ensure the app itself is working
   - If test mode works but real scraping doesn't, the issue is with scraping

3. **Run the Test Script**:
   ```bash
   python test_scrapers.py
   ```
   - This tests each scraper individually and shows detailed output
   - Helps identify which portals are working and which aren't
   - You can specify search terms: `python test_scrapers.py "developer" "Munich"`

4. **Try Different Search Terms**:
   - Use English terms: "software engineer", "developer", "manager"
   - Try broader terms: "engineer" instead of "senior software engineer"
   - Try broader locations: "Germany" instead of specific cities

5. **Check Common Issues**:
   - **HTTP 403/429**: Portal is blocking automated requests
   - **HTTP 200 but 0 jobs**: Portal structure may have changed, or search is too specific
   - **Network errors**: Check your internet connection
   - **Timeout errors**: Portal is too slow to respond

### Portal-Specific Issues

**Indeed.de**:
- Most reliable portal, uses multiple fallback selectors
- If failing, may be due to geographic restrictions or rate limiting

**StepStone.de**:
- May require specific URL format
- Structure changes frequently

**XING Jobs**:
- May require login for some features
- Limited access without authentication

### Scraping Errors

**Portal HTML structure changed:**
- Open an issue on GitHub with the portal name
- Enable debug mode to see which selectors were tried
- The HTML sample in debug output can help identify new selectors

**Rate limiting:**
- App already includes delays between requests
- Try scraping one portal at a time
- Wait a few minutes between searches

**Geo-blocking:**
- Some portals may restrict access from certain regions
- Try using a VPN connected to Germany

### Performance Issues

**Slow scraping:**
- Normal - scraping takes 5-15 seconds per portal
- Each portal has a 1-2 second delay to be respectful
- Reduce number of selected portals for faster results

**App freezing:**
- This shouldn't happen - the app uses progress indicators
- Try refreshing the browser
- Check browser console for JavaScript errors

## License

This project is for educational purposes. Ensure you comply with all applicable laws and website Terms of Service when scraping.
