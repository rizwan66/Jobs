# Troubleshooting Guide

## Common Issues and Solutions

### Port 8501 Already in Use

**Error:**
```
Port 8501 is already in use
```

**Solutions:**

#### Option 1: Use the start script (Recommended)
```bash
./start_app.sh
```
The script will automatically detect and handle port conflicts.

#### Option 2: Kill the existing process
```bash
# Find the process using port 8501
lsof -ti:8501

# Kill the process (replace PID with the number from above)
kill -9 PID

# Or kill directly
kill -9 $(lsof -ti:8501)

# Then start the app
streamlit run app.py
```

#### Option 3: Use a different port
```bash
streamlit run app.py --server.port=8502
```

Then open: `http://localhost:8502`

#### Option 4: Stop all Streamlit processes
```bash
pkill -f streamlit
streamlit run app.py
```

---

### CORS/XSRF Configuration Warning

**Error:**
```
Warning: the config option 'server.enableCORS=false' is not compatible with
'server.enableXsrfProtection=true'.
```

**Solution:** ✅ Already Fixed!

The `.streamlit/config.toml` file has been updated to use compatible settings:
- `enableCORS = true`
- `enableXsrfProtection = true`

This warning should no longer appear.

---

### Module Not Found Errors

**Error:**
```
ModuleNotFoundError: No module named 'streamlit'
```

**Solution:**
```bash
# Install all dependencies
pip install -r requirements.txt

# Or install individually
pip install streamlit requests beautifulsoup4 pandas lxml
```

---

### Permission Denied

**Error:**
```
Permission denied: './start_app.sh'
```

**Solution:**
```bash
chmod +x start_app.sh
./start_app.sh
```

---

### No Jobs Found

**Issue:** Search returns 0 jobs from all portals

**Solutions:**

1. **Enable Test Mode First:**
   - Check "Test Mode (Use Sample Data)" in sidebar
   - This verifies the app itself works
   - If test mode works, the issue is with scraping

2. **Enable Debug Mode:**
   - Check "Show Debug Info" in sidebar
   - Look at status codes and errors
   - Check which selectors were tried

3. **Run Test Script:**
   ```bash
   python test_scrapers.py "developer" "Berlin"
   ```
   This shows detailed information about each portal.

4. **Check Common Issues:**
   - **Status 200, 0 jobs**: Portal structure changed or search too specific
   - **Status 403/429**: Portal blocking requests (try different keywords)
   - **Network error**: Check internet connection
   - **Timeout**: Portal too slow (increase timeout in scrapers.py)

5. **Try Different Parameters:**
   - Use broader keywords: "engineer" instead of "senior software engineer"
   - Try different locations: "Germany" instead of specific cities
   - Use English terms: "software engineer" often works better
   - Reduce max pages to 1-3 for testing

---

### App Runs But Shows Blank Page

**Solutions:**

1. **Clear browser cache:**
   - Press Cmd+Shift+R (Mac) or Ctrl+Shift+R (Windows)
   - Or clear browser cache manually

2. **Try different browser:**
   - Chrome usually works best
   - Firefox and Safari also supported

3. **Check console for errors:**
   - Open browser developer tools (F12)
   - Check console tab for JavaScript errors

4. **Restart the app:**
   ```bash
   # Stop with Ctrl+C
   # Then restart
   ./start_app.sh
   ```

---

### Slow Performance

**Issue:** App takes too long to load or search

**Solutions:**

1. **Reduce max pages:**
   - Set slider to 3-5 pages (default: 5)
   - Don't use 40 pages unless necessary

2. **Search fewer portals:**
   - Uncheck 1-2 portals in sidebar
   - Indeed.de is usually fastest

3. **Use specific keywords:**
   - More specific = fewer pages needed
   - "Python Developer Berlin" better than "developer"

4. **Clear session state:**
   - Refresh browser (Cmd/Ctrl + R)
   - Click "Clear cache" in Streamlit menu (top right)

---

### CSV Export Not Working

**Issue:** Download button doesn't work

**Solutions:**

1. **Check browser settings:**
   - Allow downloads from localhost
   - Check download location

2. **Check if jobs were found:**
   - Export only works if jobs > 0
   - Try test mode to verify export works

3. **Try different browser:**
   - Some browsers block localhost downloads

---

### Filters Not Working

**Issue:** Filters don't reduce results

**Solutions:**

1. **Check filter values:**
   - Filters must exactly match job data
   - Case-sensitive in some cases

2. **Clear and reapply filters:**
   - Deselect all filters
   - Apply one at a time

3. **Check if data exists:**
   - "Skills" filter only works if skills detected
   - "Salary" filter only works if salary info present

---

### Deployment Issues

**Issue:** App won't deploy to Streamlit Cloud

**Solutions:**

1. **Check requirements.txt:**
   ```bash
   cat requirements.txt
   ```
   Ensure all dependencies are listed with versions.

2. **Check for syntax errors:**
   ```bash
   python -m py_compile app.py
   python -m py_compile scrapers.py
   ```

3. **Verify Git setup:**
   ```bash
   git status
   git log -1
   ```

4. **Check build logs:**
   - View logs in Streamlit Cloud dashboard
   - Look for specific error messages

5. **Common deployment errors:**
   - **Missing dependencies**: Add to requirements.txt
   - **Python version**: Streamlit Cloud uses Python 3.9-3.11
   - **Large files**: Remove or gitignore files > 100MB
   - **Invalid config**: Check .streamlit/config.toml syntax

---

### Memory Errors

**Issue:** App crashes with memory error

**Solutions:**

1. **Reduce max pages to 5 or less**

2. **Search one portal at a time**

3. **Add caching (for advanced users):**
   ```python
   @st.cache_data(ttl=3600)
   def cached_scrape(...):
       return scrape_all_portals(...)
   ```

4. **Limit result display:**
   - Use pagination (already implemented)
   - Reduce jobs_per_page in app.py

---

## Quick Fixes Cheat Sheet

| Problem | Quick Fix |
|---------|-----------|
| Port in use | `./start_app.sh` or `kill -9 $(lsof -ti:8501)` |
| No jobs found | Enable Test Mode first |
| Slow search | Reduce max pages to 3-5 |
| Module not found | `pip install -r requirements.txt` |
| Can't start script | `chmod +x start_app.sh` |
| Blank page | Clear cache (Cmd+Shift+R) |
| CSV won't download | Try different browser |

---

## Getting Help

### Before Asking for Help

1. **Check this guide** for your specific error
2. **Enable debug mode** and note the errors
3. **Try test mode** to isolate the issue
4. **Run test script** to test scrapers individually
5. **Check browser console** for JavaScript errors

### Information to Provide

When reporting an issue, include:

1. **Error message** (exact text)
2. **Steps to reproduce**
3. **Debug mode output** (if relevant)
4. **Test script output** (if scraping issue)
5. **Browser and OS** version
6. **Python version**: `python --version`
7. **Streamlit version**: `streamlit version`

### Where to Get Help

- **Documentation**: Check all .md files in project
- **Streamlit Docs**: [docs.streamlit.io](https://docs.streamlit.io)
- **Python Help**: [python.org](https://www.python.org)
- **BeautifulSoup**: [crummy.com/software/BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)

---

## Preventive Maintenance

### Regular Checks

**Weekly:**
- Test all three portals
- Verify filters work
- Check export functionality

**Monthly:**
- Update dependencies: `pip install --upgrade -r requirements.txt`
- Test on different browsers
- Review scraper selectors

**When Issues Arise:**
- Check portal HTML structure
- Update selectors in scrapers.py
- Test with test_scrapers.py

---

## Advanced Troubleshooting

### Debug Scrapers

```bash
# Test with verbose output
python test_scrapers.py "engineer" "Berlin"

# Test single portal
python -c "from scrapers import IndeedDeScraper; s = IndeedDeScraper(); jobs, info = s.scrape('developer', 'Berlin', max_pages=1); print(f'Found: {len(jobs)} jobs')"
```

### Check Streamlit Cache

```bash
# Clear Streamlit cache
streamlit cache clear
```

### Verify Installation

```bash
# Check Python version (should be 3.7+)
python --version

# Check Streamlit version
streamlit version

# List installed packages
pip list | grep -E "streamlit|requests|beautifulsoup4|pandas"
```

### Network Debugging

```bash
# Test if portals are accessible
curl -I https://de.indeed.com
curl -I https://www.stepstone.de
curl -I https://www.xing.com

# Check DNS
nslookup de.indeed.com
```

---

## Still Having Issues?

If problems persist after trying these solutions:

1. **Restart everything:**
   ```bash
   pkill -f streamlit
   ./start_app.sh
   ```

2. **Fresh install:**
   ```bash
   pip uninstall -r requirements.txt -y
   pip install -r requirements.txt
   ```

3. **Check system resources:**
   - Close other applications
   - Free up RAM
   - Check disk space

4. **Last resort - Reset:**
   ```bash
   rm -rf __pycache__
   rm -rf .streamlit/cache
   pip install --force-reinstall streamlit
   ```

---

**Most issues can be resolved with `./start_app.sh` and proper dependency installation!**
