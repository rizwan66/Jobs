# Usage Guide - German Job Portal Scanner

## Quick Start

### 1. Installation
```bash
cd job_scraper_app
pip install -r requirements.txt
```

### 2. Run the App
```bash
streamlit run app.py
```

The app will open in your browser at http://localhost:8501

### 3. Search for Jobs

**In the sidebar:**
1. Enter job keywords (e.g., "Software Engineer", "Marketing Manager")
2. Enter location (e.g., "Berlin", "Munich", "Hamburg")
3. Select job type (optional)
4. Choose which portals to search
5. Click "Search Jobs"

## Features Walkthrough

### Debug Mode
**When to use:** If you're getting no results or want to understand what's happening

**How to enable:**
1. Check "Show Debug Info" in the sidebar
2. Perform a search
3. View the debug panel showing:
   - URLs accessed
   - HTTP status codes
   - Number of jobs found per portal
   - Errors encountered
   - Selectors that were tried

**What to look for:**
- Status code 200 = Request succeeded
- Status code 403/429 = Portal blocking requests
- "Jobs Found: 0" with status 200 = Portal structure may have changed

### Test Mode
**When to use:** To verify the app interface is working correctly

**How to enable:**
1. Check "Test Mode (Use Sample Data)" in the sidebar
2. Enter any keywords and location
3. Click "Search Jobs"
4. You'll see sample data instead of real scraping results

**Purpose:**
- Tests the app UI without making actual web requests
- Useful for development and troubleshooting
- If test mode works but real mode doesn't, the issue is with scraping

### Filtering Results

After search results appear:
1. **Filter by Company**: Select specific companies from the dropdown
2. **Filter by Portal**: Choose which portals' results to view
3. **Pagination**: Navigate through multiple pages of results

### Exporting Data

1. After getting search results, click "Download Results as CSV"
2. Opens a download dialog with timestamped filename
3. CSV includes all filtered results with:
   - Job title
   - Company name
   - Location
   - Description
   - URL
   - Portal name

## Testing Individual Scrapers

If the app isn't finding jobs, test scrapers individually:

```bash
python test_scrapers.py
```

Or with custom parameters:
```bash
python test_scrapers.py "developer" "Munich"
```

**Output shows:**
- Which portals are working
- Detailed debug information for each
- First job found (if any)
- HTML samples for debugging

## Common Search Examples

### Tech Jobs
- **Keywords**: "Software Engineer", "Developer", "DevOps"
- **Locations**: "Berlin", "Munich", "Hamburg", "Frankfurt"
- **Portals**: All three work well for tech jobs

### Business Jobs
- **Keywords**: "Project Manager", "Business Analyst", "Marketing"
- **Locations**: Major German cities
- **Portals**: Indeed.de and StepStone.de typically have more results

### Entry-Level Jobs
- **Keywords**: "Junior", "Trainee", "Intern"
- **Locations**: Any German city
- **Note**: May get fewer results, try broader terms

### Remote Jobs
- **Keywords**: Your desired role + "remote"
- **Job Type**: Select "Remote"
- **Location**: Can use "Germany" or specific city

## Troubleshooting Workflow

### If you get no results:

1. **First: Enable Debug Mode**
   - Check "Show Debug Info"
   - Look at status codes and errors

2. **Second: Try Test Mode**
   - If test mode works, the app is fine
   - Issue is with web scraping

3. **Third: Run Test Script**
   ```bash
   python test_scrapers.py "developer" "Berlin"
   ```
   - See which portals are working
   - Get detailed error messages

4. **Fourth: Try Different Parameters**
   - Broader keywords
   - Different locations
   - Different portals
   - English vs German terms

5. **Fifth: Check Network**
   - Test your internet connection
   - Try accessing portals manually in browser
   - Check if you're behind a firewall/proxy

## Understanding Debug Output

### Successful Scraping
```
URL: https://de.indeed.com/jobs?q=engineer&l=Berlin
Status Code: 200
Jobs Found: 15
```
✅ Everything working correctly

### Portal Blocking
```
Status Code: 403
Error: Network error: 403 Client Error
Jobs Found: 0
```
❌ Portal is blocking automated requests

### Structure Changed
```
Status Code: 200
Jobs Found: 0
Selectors tried: div.job_seen_beacon, div.jobsearch-ResultsList, ...
```
⚠️ Portal HTML structure may have changed

### Network Error
```
Status Code: 0
Error: Network error: Connection timeout
```
❌ Connection issue - check internet

## Best Practices

1. **Be Patient**: Scraping takes 5-15 seconds per portal
2. **Be Respectful**: Don't spam searches - app has built-in delays
3. **Start Broad**: Use general terms first, then refine
4. **Use Filters**: Get all results first, then filter in the app
5. **Export Data**: Download results for later analysis
6. **Check Debug**: Always check debug mode if something seems wrong

## Advanced Tips

### Finding More Jobs
- Search for synonyms (e.g., "developer" and "engineer" separately)
- Try both English and German terms
- Use location variations (city names vs region names)
- Try different portals separately

### Dealing with Blocking
- Wait a few minutes between searches
- Try one portal at a time
- Use broader search terms (fewer requests needed)
- Consider time of day (less traffic = less likely to be blocked)

### Updating Selectors
If you're comfortable with Python and HTML:
1. Enable debug mode to see HTML samples
2. Visit the portal manually and inspect elements
3. Update selectors in [scrapers.py](scrapers.py)
4. Test with `python test_scrapers.py`

## Getting Help

If nothing works:
1. Check [README.md](README.md) troubleshooting section
2. Run test script and save output
3. Check console output for error messages
4. Verify you can access job portals manually in browser
