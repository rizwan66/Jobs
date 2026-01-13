# Feature Documentation

## Advanced Filtering System

The German Job Portal Scanner now includes a comprehensive filtering system to help you find the perfect job.

### Filter Categories

#### 1. Company Filter
- **Type**: Multi-select dropdown
- **Purpose**: Filter jobs by specific companies
- **Usage**: Select one or more companies from the list
- **Example**: Filter for "Google", "Microsoft", "SAP"

#### 2. Location Filter
- **Type**: Multi-select dropdown
- **Purpose**: Filter jobs by specific cities/regions
- **Usage**: Select one or more locations
- **Example**: Filter for "Berlin", "Munich", "Hamburg"
- **Note**: Shows all unique locations from search results

#### 3. Job Level Filter
- **Type**: Multi-select dropdown
- **Purpose**: Filter by career level/seniority
- **Options**:
  - Entry Level (Junior, Trainee, Intern, Graduate)
  - Mid Level (Experienced, Intermediate)
  - Senior Level (Senior, Lead, Principal, Expert)
  - Management (Director, Manager, VP, Head of)
  - Not Specified (when level cannot be determined)
- **Example**: Filter for only "Entry Level" jobs

#### 4. Skills Filter
- **Type**: Multi-select dropdown
- **Purpose**: Filter jobs requiring specific technical skills
- **Detected Skills**: 50+ common technical skills including:
  - **Languages**: Python, Java, JavaScript, TypeScript, C++, C#, PHP, Ruby, Go, Rust
  - **Frameworks**: React, Angular, Vue, Node.js, Django, Flask, Spring
  - **Databases**: SQL, MySQL, PostgreSQL, MongoDB, Redis, Oracle
  - **Cloud/DevOps**: AWS, Azure, GCP, Docker, Kubernetes, Jenkins, CI/CD
  - **Other**: Machine Learning, AI, Agile, Scrum, REST API, GraphQL
- **Example**: Filter for jobs requiring "Python" and "AWS"
- **Note**: Skills are auto-detected from job descriptions

#### 5. Salary Filter
- **Type**: Single-select dropdown
- **Options**:
  - All Jobs (default)
  - With Salary Info Only
  - Without Salary Info
- **Purpose**: Show only jobs that include salary information
- **Note**: Not all job postings include salary

#### 6. Portal Filter
- **Type**: Multi-select dropdown
- **Purpose**: Filter by specific job portal
- **Options**: Indeed.de, StepStone.de, XING Jobs
- **Example**: Show only jobs from "Indeed.de"

## Job Metadata Extraction

### Automatic Data Extraction

The scrapers automatically extract and classify the following information:

#### Job Level Classification

Jobs are classified based on keywords in the title and description:

| Level | Keywords |
|-------|----------|
| Entry Level | junior, entry level, graduate, trainee, intern, praktikum |
| Mid Level | mid-level, intermediate, experienced |
| Senior Level | senior, lead, principal, staff, expert |
| Management | director, head of, chief, vp, vice president, manager, leiter |

#### Skill Detection

Skills are detected by scanning job descriptions for common technical terms:

**Programming Languages** (12):
- Python, Java, JavaScript, TypeScript, C++, C#, PHP, Ruby, Go, Rust, Swift, Kotlin

**Web Frameworks** (8):
- React, Angular, Vue, Node.js, Django, Flask, Spring, Express

**Databases** (7):
- SQL, MySQL, PostgreSQL, MongoDB, Redis, Oracle, NoSQL

**Cloud & DevOps** (8):
- AWS, Azure, GCP, Docker, Kubernetes, Jenkins, Git, CI/CD

**Data Science** (5):
- Machine Learning, AI, Data Science, Deep Learning, TensorFlow, PyTorch

**Methodologies** (6):
- Agile, Scrum, DevOps, REST API, GraphQL, Microservices

**Frontend** (5):
- HTML, CSS, SASS, Bootstrap, Tailwind

**Other** (7):
- Linux, Unix, Windows Server, Networking, SAP, Salesforce, Excel, Power BI, Tableau

#### Salary Information

- Extracted when available from job postings
- Displayed in various formats (annual, monthly, hourly)
- Used for filtering jobs with/without salary info

## UI Enhancements

### Job Display

Each job listing now shows:

1. **Job Title** (large header)
2. **Basic Information** (two columns):
   - Company name
   - Location
   - Portal source
   - Job level badge
3. **Salary** (if available): Displayed with 💰 icon
4. **Skills** (if detected): First 5 skills with 🔧 icon
5. **Description**: Expandable section with full description and all detected skills
6. **Apply Button**: Direct link to original job posting

### Statistics Dashboard

The dashboard shows:
- Total Jobs Found
- Unique Companies
- Portals Scanned
- Pages Scraped (in debug mode)

### Filter Results Counter

Shows: "Showing X of Y jobs" where:
- X = Number of jobs after applying filters
- Y = Total number of jobs found

## Performance Considerations

### Skill Detection

- Runs on every job during scraping
- Minimal performance impact
- Caches results in job object
- Limits to top 10 skills per job

### Filtering

- Client-side filtering (instant results)
- No additional API calls needed
- Filters are applied sequentially
- Maintains original result set

## Export Functionality

CSV export now includes all metadata:

| Column | Description |
|--------|-------------|
| title | Job title |
| company | Company name |
| location | Job location |
| summary | Job description |
| url | Link to original posting |
| portal | Source portal |
| salary | Salary information (if available) |
| job_level | Classified job level |
| skills | Comma-separated list of detected skills |

## Test Mode

Sample data now includes:
- All metadata fields
- Example salaries
- Various job levels
- Multiple skills per job
- Mix of jobs with/without salary

This allows full testing of filtering features without scraping.

## Future Enhancements

Potential additions to the filtering system:

1. **Salary Range Filter**: Minimum and maximum salary sliders
2. **Date Posted Filter**: Jobs from last 24h, 7 days, 30 days
3. **Contract Type**: Permanent, Contract, Freelance
4. **Work Arrangement**: Office, Remote, Hybrid
5. **Company Size**: Startup, SME, Enterprise
6. **Benefits**: Healthcare, pension, equity, etc.
7. **Save Filters**: Save favorite filter combinations
8. **Advanced Search**: Boolean operators for skills (AND, OR, NOT)

## API for Custom Filters

Developers can add custom filters by modifying the filtering logic in `app.py`:

```python
# Example: Add custom filter
if custom_filter_value:
    filtered_jobs = [
        job for job in filtered_jobs
        if your_custom_condition(job)
    ]
```

## Troubleshooting Filters

### No Results After Filtering

If filters show 0 results:
1. Remove filters one by one to identify the issue
2. Check if filter values match job data exactly
3. Use "All Jobs" for salary filter
4. Try broader skill selections

### Missing Skills

If expected skills aren't detected:
- Skills must appear in job description
- Skill names must match exactly (case-insensitive)
- Consider adding custom skills to `scrapers.py`

### Incorrect Job Levels

If job levels seem incorrect:
- Classification is based on keywords
- Can be improved by updating keywords in `_extract_job_level()`
- "Not Specified" is shown when no keywords match

## Accessibility

All filters are:
- Keyboard navigable
- Screen reader compatible
- Clear labeled
- Provide immediate visual feedback
