# Changelog

All notable changes to the Global Job Portal Scanner project will be documented in this file.

## [2.0.0] - 2026-01-12

### 🌟 Major Features Added

#### Multi-Country Support
- **Added**: Support for 5 countries/regions (Germany, USA, Canada, UK, Europe)
- **Added**: Country selection dropdown in sidebar
- **Added**: Information tabs for each country
- **Added**: Dynamic portal selection based on country
- **Added**: Country-specific default locations

#### New Job Portals
- **Added**: Monster.de scraper with full functionality
- **Added**: LinkedIn scraper with anti-scraping measure handling
- **Total Portals**: Increased from 3 to 5 for Germany

#### Increased Capacity
- **Changed**: Maximum pages per portal increased from 40 to 100
- **Impact**: Can now scrape up to 5,000 jobs per search (vs 2,000 previously)
- **Performance**: ~2.5x increase in search capacity

#### UI Enhancements
- **Added**: Country selection tabs with flags (🇩🇪 🇺🇸 🇨🇦 🇬🇧 🇪🇺)
- **Added**: Country-specific information and warnings
- **Added**: Dynamic portal checkboxes based on selected country
- **Changed**: App title from "German Job Portal Scanner" to "Global Job Portal Scanner"
- **Changed**: Background color to black (#000000) with dark theme
- **Changed**: Sidebar now shows country selector at the top

### 📝 Technical Changes

#### scrapers.py
- **Added**: `MonsterDeScraper` class (~160 lines)
- **Added**: `LinkedInScraper` class (~160 lines)
- **Changed**: All scrapers now support `max_pages=100` (previously 40)
- **Changed**: Updated `scrape_all_portals()` to include new scrapers
- **Total Lines**: ~1,200 (up from ~650)

#### app.py
- **Added**: Country selection tabs
- **Added**: `country_portals` dictionary for portal configuration
- **Added**: `default_locations` dictionary for country defaults
- **Added**: Dynamic portal selection logic
- **Added**: Warnings for unsupported portals
- **Changed**: Max pages slider now goes up to 100 (from 40)
- **Changed**: Title and branding to "Global"

#### .streamlit/config.toml
- **Changed**: `backgroundColor` from #ffffff (white) to #000000 (black)
- **Changed**: `secondaryBackgroundColor` to #1a1a1a (dark gray)
- **Changed**: `textColor` to #ffffff (white) for readability

#### Documentation
- **Added**: ENHANCEMENTS_2026.md - Detailed enhancement documentation
- **Added**: CHANGELOG.md - This file
- **Updated**: README.md - Multi-country support, new portals, increased limits
- **Updated**: STATUS.md - Current project status with enhancements

### 🐛 Bug Fixes
- None (this is a feature enhancement release)

### ⚠️ Known Limitations
- Non-Germany portals (USA, Canada, UK) are listed but not fully implemented
- LinkedIn has strict anti-scraping measures and may return limited results
- Monster.de scraper is new and may need adjustments based on real-world usage

### 🔄 Migration Guide
No breaking changes. Existing users can continue using the app exactly as before. All new features are additive.

### 📊 Statistics
- **New Scrapers**: 2 (Monster.de, LinkedIn)
- **Total Portals**: 5 for Germany (was 3)
- **Countries Supported**: 5 (was 1)
- **Max Pages**: 100 (was 40)
- **Max Jobs per Search**: ~5,000 (was ~2,000)
- **Code Growth**: ~550 lines added

---

## [1.0.0] - 2026-01-12 (Earlier Session)

### Initial Release Features

#### Core Functionality
- **Added**: Multi-portal scraping (Indeed.de, StepStone.de, XING Jobs)
- **Added**: Multi-page scraping (up to 40 pages per portal)
- **Added**: Real-time job search and display
- **Added**: CSV export functionality

#### Advanced Filtering
- **Added**: 6 filter types:
  - Company filter (multi-select)
  - Location filter (multi-select)
  - Job Level filter (Entry/Mid/Senior/Management)
  - Skills filter (50+ technologies)
  - Salary filter (With/Without)
  - Portal filter (multi-select)

#### Intelligent Data Extraction
- **Added**: Automatic skill detection (50+ technical skills)
- **Added**: Job level classification (4 categories)
- **Added**: Salary information extraction
- **Added**: Duplicate detection across pages

#### User Interface
- **Added**: Streamlit-based web interface
- **Added**: Sidebar for search parameters
- **Added**: Statistics dashboard
- **Added**: Debug mode with detailed information
- **Added**: Test mode with sample data
- **Added**: Pagination for large result sets

#### Documentation
- **Added**: README.md - Main documentation
- **Added**: DEPLOYMENT.md - Deployment guide
- **Added**: USAGE_GUIDE.md - User instructions
- **Added**: FEATURES.md - Feature documentation
- **Added**: QUICK_START.md - Quick start guide
- **Added**: PROJECT_SUMMARY.md - Project overview
- **Added**: DEPLOYMENT_CHECKLIST.md - Deployment checklist
- **Added**: TROUBLESHOOTING.md - Troubleshooting guide

#### Configuration
- **Added**: .streamlit/config.toml - Theme and server settings
- **Added**: requirements.txt - Python dependencies
- **Added**: packages.txt - System dependencies
- **Added**: .gitignore - Git exclusions
- **Added**: deploy_to_github.sh - Deployment automation
- **Added**: start_app.sh - Startup script with port conflict handling

#### Bug Fixes (During Development)
- **Fixed**: CORS/XSRF configuration conflict
- **Fixed**: Port 8501 already in use error
- **Fixed**: StepStone.de scraper returning no results
- **Fixed**: XING Jobs scraper returning no results
- **Fixed**: Indeed.de scraper with multiple fallback selectors

---

## Versioning

This project uses [Semantic Versioning](https://semver.org/):
- **Major version** (X.0.0): Breaking changes or major feature additions
- **Minor version** (0.X.0): New features, backwards compatible
- **Patch version** (0.0.X): Bug fixes, backwards compatible

## Links

- **Documentation**: See README.md
- **Enhancements**: See ENHANCEMENTS_2026.md
- **Status**: See STATUS.md
- **Troubleshooting**: See TROUBLESHOOTING.md
