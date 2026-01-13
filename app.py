"""
Streamlit Job Scraper App for German Job Portals
"""
import streamlit as st
import pandas as pd
from scrapers import scrape_all_portals
from sample_data import get_sample_jobs
from datetime import datetime, timedelta
import time


# Page configuration
st.set_page_config(
    page_title="Global Job Portal Scanner",
    page_icon="🔍",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .job-card {
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #ddd;
        margin-bottom: 1rem;
        background-color: #f9f9f9;
    }
    .job-title {
        font-size: 1.2rem;
        font-weight: bold;
        color: #1f77b4;
    }
    .company-name {
        font-size: 1rem;
        color: #555;
    }
    .location {
        font-size: 0.9rem;
        color: #777;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'jobs' not in st.session_state:
    st.session_state.jobs = []
if 'search_performed' not in st.session_state:
    st.session_state.search_performed = False
if 'debug_info' not in st.session_state:
    st.session_state.debug_info = {}
if 'show_debug' not in st.session_state:
    st.session_state.show_debug = False
if 'selected_quick_search' not in st.session_state:
    st.session_state.selected_quick_search = ""


def main():
    # Header
    st.markdown('<h1 class="main-header">🇩🇪 German Job Portal Scanner</h1>', unsafe_allow_html=True)
    st.markdown("**Search StepStone.de and XING Jobs**")
    st.markdown("---")

    # Configure portals - ONLY GERMANY with StepStone and XING
    country_portals = {
        "Germany": ["StepStone.de", "XING Jobs"],
    }

    default_locations = {
        "Germany": "Berlin",
    }

    # Store selected country in session state - LOCKED TO GERMANY
    if 'selected_country' not in st.session_state:
        st.session_state.selected_country = "Germany"

    # Force Germany selection
    selected_country = "Germany"

    # Sidebar for search parameters
    with st.sidebar:
        st.header("Search Parameters (Germany Only)")

        # Quick search buttons for common roles
        st.subheader("🎯 Quick Search")
        quick_searches = {
            "Electrical Engineer": "Electrical Engineer",
            "Software Engineer": "Software Engineer",
            "Software Test Eng.": "Software Test Engineer",
            "SW Automation": "Software Automation",
            "Automation Eng.": "Automation Engineer",
            "Data Analyst": "Data Analyst",
            "Data Science": "Data Science",
            "AI": "AI",
            "ML": "Machine Learning"
        }

        # Create a 3-column layout for buttons
        cols = st.columns(3)
        for idx, (display_name, search_term) in enumerate(quick_searches.items()):
            col_idx = idx % 3
            with cols[col_idx]:
                if st.button(display_name, key=f"quick_{idx}", use_container_width=True):
                    st.session_state.selected_quick_search = search_term

        st.markdown("---")

        # Use selected role or manual input
        default_keywords = st.session_state.selected_quick_search if st.session_state.selected_quick_search else ""
        keywords = st.text_input(
            "Job Title / Keywords",
            value=default_keywords,
            placeholder="e.g., Software Engineer, Data Analyst",
            help="Enter job title or keywords to search for (or use Quick Search buttons above)"
        )

        location = st.text_input(
            "Location",
            value="Berlin",
            placeholder="e.g., Berlin, Munich, Hamburg",
            help="Enter city or region in Germany"
        )

        job_type = st.selectbox(
            "Job Type",
            options=["Any", "Full-time", "Part-time", "Remote", "Contract", "Internship"],
            help="Filter by employment type"
        )

        max_pages = st.slider(
            "Maximum Pages per Portal",
            min_value=1,
            max_value=100,
            value=5,
            help="Number of pages to scrape from each portal. More pages = more jobs but slower search. Max: 100 pages"
        )

        st.markdown("---")
        st.subheader("Job Portals")

        # Only StepStone and XING - both checked by default
        available_portals = ["StepStone.de", "XING Jobs"]
        portals = {}
        for portal in available_portals:
            portals[portal] = st.checkbox(portal, value=True)

        selected_portals = [portal for portal, selected in portals.items() if selected]

        st.markdown("---")

        # Debug mode toggle
        st.session_state.show_debug = st.checkbox("Show Debug Info", value=st.session_state.show_debug)

        # Test mode toggle
        test_mode = st.checkbox("Test Mode (Use Sample Data)", value=False,
                               help="Use this to test the app without scraping real portals")

        st.markdown("---")

        search_button = st.button("🔍 Search Jobs", type="primary", use_container_width=True)

        if search_button:
            if not keywords or not location:
                st.error("Please enter both keywords and location!")
            elif not selected_portals:
                st.error("Please select at least one job portal!")
            else:
                with st.spinner("Scanning job portals... This may take a moment."):
                    try:
                        if test_mode:
                            # Use sample data
                            jobs = get_sample_jobs(keywords, location)
                            debug_info = {
                                'Sample Data': {
                                    'url': 'N/A (Test Mode)',
                                    'status_code': 200,
                                    'error': '',
                                    'jobs_found': len(jobs),
                                    'selectors_tried': ['Sample data generator']
                                }
                            }
                            st.info("Test mode: Using sample data instead of scraping real portals")
                        else:
                            # Real scraping
                            job_type_param = "" if job_type == "Any" else job_type
                            jobs, debug_info = scrape_all_portals(
                                keywords=keywords,
                                location=location,
                                job_type=job_type_param,
                                selected_portals=selected_portals,
                                max_pages=max_pages
                            )

                        st.session_state.jobs = jobs
                        st.session_state.debug_info = debug_info
                        st.session_state.search_performed = True

                        if len(jobs) > 0:
                            st.success(f"Found {len(jobs)} jobs!")
                        else:
                            st.warning("No jobs found. Enable 'Show Debug Info' to see details about what happened.")
                    except Exception as e:
                        st.error(f"Error during search: {str(e)}")
                        import traceback
                        if st.session_state.show_debug:
                            st.code(traceback.format_exc())

    # Main content area
    if st.session_state.search_performed:
        jobs = st.session_state.jobs
        debug_info = st.session_state.debug_info

        # Show debug information if enabled
        if st.session_state.show_debug and debug_info:
            st.subheader("Debug Information")
            with st.expander("View Scraping Details", expanded=False):
                for portal, info in debug_info.items():
                    st.markdown(f"**{portal}**")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"URL: {info.get('url', 'N/A')}")
                        st.write(f"Status Code: {info.get('status_code', 'N/A')}")
                        st.write(f"Jobs Found: {info.get('jobs_found', 0)}")
                        st.write(f"Pages Scraped: {info.get('pages_scraped', 0)}")
                    with col2:
                        if info.get('error'):
                            st.error(f"Error: {info.get('error')}")
                        if info.get('selectors_tried'):
                            st.write(f"Selectors tried: {', '.join(info.get('selectors_tried', []))}")
                    st.markdown("---")
            st.markdown("---")

        if len(jobs) > 0:
            # Statistics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Jobs Found", len(jobs))
            with col2:
                unique_companies = len(set([job['company'] for job in jobs if job['company'] != 'N/A']))
                st.metric("Unique Companies", unique_companies)
            with col3:
                portals_used = len(set([job['portal'] for job in jobs]))
                st.metric("Portals Scanned", portals_used)

            st.markdown("---")

            # Advanced Filters
            st.subheader("🔍 Advanced Filters")

            filter_col1, filter_col2, filter_col3 = st.columns(3)

            with filter_col1:
                company_filter = st.multiselect(
                    "Company",
                    options=sorted(list(set([job['company'] for job in jobs if job.get('company') and job['company'] != 'N/A'])))
                )

                location_filter = st.multiselect(
                    "Location",
                    options=sorted(list(set([job['location'] for job in jobs if job.get('location')])))
                )

            with filter_col2:
                portal_filter = st.multiselect(
                    "Portal",
                    options=sorted(list(set([job['portal'] for job in jobs])))
                )

                level_filter = st.multiselect(
                    "Job Level",
                    options=sorted(list(set([job.get('job_level', 'Not Specified') for job in jobs])))
                )

            with filter_col3:
                # Collect all unique skills
                all_skills = set()
                for job in jobs:
                    if job.get('skills'):
                        all_skills.update(job['skills'])

                skill_filter = st.multiselect(
                    "Required Skills",
                    options=sorted(list(all_skills))
                )

                salary_filter = st.selectbox(
                    "Salary Info",
                    options=["All Jobs", "With Salary Info Only", "Without Salary Info"]
                )

            # Job posting age filter (full width below)
            st.markdown("---")
            posting_age_filter = st.selectbox(
                "📅 Job Posting Age",
                options=["All Jobs", "Last 24 Hours", "Last 3 Days", "Last 7 Days", "Last 14 Days", "Last 30 Days"],
                help="Filter jobs by how recently they were posted"
            )

            # Apply filters
            filtered_jobs = jobs

            if company_filter:
                filtered_jobs = [job for job in filtered_jobs if job.get('company') in company_filter]

            if location_filter:
                filtered_jobs = [job for job in filtered_jobs if job.get('location') in location_filter]

            if portal_filter:
                filtered_jobs = [job for job in filtered_jobs if job.get('portal') in portal_filter]

            if level_filter:
                filtered_jobs = [job for job in filtered_jobs if job.get('job_level', 'Not Specified') in level_filter]

            if skill_filter:
                filtered_jobs = [job for job in filtered_jobs if any(skill in job.get('skills', []) for skill in skill_filter)]

            if salary_filter == "With Salary Info Only":
                filtered_jobs = [job for job in filtered_jobs if job.get('salary')]
            elif salary_filter == "Without Salary Info":
                filtered_jobs = [job for job in filtered_jobs if not job.get('salary')]

            # Apply posting age filter
            if posting_age_filter != "All Jobs":
                today = datetime.now().date()

                days_mapping = {
                    "Last 24 Hours": 1,
                    "Last 3 Days": 3,
                    "Last 7 Days": 7,
                    "Last 14 Days": 14,
                    "Last 30 Days": 30
                }

                days_ago = days_mapping.get(posting_age_filter, 30)
                cutoff_date = (today - timedelta(days=days_ago)).strftime('%Y-%m-%d')

                # Filter jobs posted after cutoff date
                filtered_jobs = [
                    job for job in filtered_jobs
                    if job.get('posted_date') and job['posted_date'] >= cutoff_date
                ]

            st.markdown(f"**Showing {len(filtered_jobs)} of {len(jobs)} jobs**")
            st.markdown("---")

            # Export button
            if filtered_jobs:
                df = pd.DataFrame(filtered_jobs)
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download Results as CSV",
                    data=csv,
                    file_name=f"job_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                )

            # Display jobs
            st.subheader("Job Listings")

            # Pagination
            jobs_per_page = 10
            total_pages = (len(filtered_jobs) - 1) // jobs_per_page + 1 if filtered_jobs else 0

            if 'current_page' not in st.session_state:
                st.session_state.current_page = 1

            if total_pages > 1:
                page_col1, page_col2, page_col3 = st.columns([1, 2, 1])
                with page_col2:
                    st.session_state.current_page = st.selectbox(
                        "Page",
                        options=list(range(1, total_pages + 1)),
                        index=st.session_state.current_page - 1
                    )

            # Calculate start and end indices
            start_idx = (st.session_state.current_page - 1) * jobs_per_page
            end_idx = min(start_idx + jobs_per_page, len(filtered_jobs))

            # Display jobs for current page
            for idx, job in enumerate(filtered_jobs[start_idx:end_idx], start=start_idx + 1):
                with st.container():
                    col1, col2 = st.columns([3, 1])

                    with col1:
                        st.markdown(f"### {idx}. {job['title']}")

                        # Display basic info
                        info_col1, info_col2 = st.columns(2)
                        with info_col1:
                            st.markdown(f"**Company:** {job['company']}")
                            st.markdown(f"**Location:** {job['location']}")
                        with info_col2:
                            st.markdown(f"**Portal:** {job['portal']}")
                            if job.get('job_level'):
                                st.markdown(f"**Level:** {job['job_level']}")

                        # Display salary if available
                        if job.get('salary'):
                            st.markdown(f"💰 **Salary:** {job['salary']}")

                        # Display posted date if available
                        if job.get('posted_date'):
                            try:
                                posted = datetime.strptime(job['posted_date'], '%Y-%m-%d').date()
                                today = datetime.now().date()
                                days_ago = (today - posted).days
                                if days_ago == 0:
                                    date_display = "📅 **Posted:** Today"
                                elif days_ago == 1:
                                    date_display = "📅 **Posted:** Yesterday"
                                elif days_ago < 7:
                                    date_display = f"📅 **Posted:** {days_ago} days ago"
                                elif days_ago < 30:
                                    weeks_ago = days_ago // 7
                                    date_display = f"📅 **Posted:** {weeks_ago} week{'s' if weeks_ago > 1 else ''} ago"
                                else:
                                    date_display = f"📅 **Posted:** {job['posted_date']}"
                                st.markdown(date_display)
                            except:
                                st.markdown(f"📅 **Posted:** {job['posted_date']}")

                        # Display skills if available
                        if job.get('skills'):
                            skills_str = ", ".join(job['skills'][:5])  # Show first 5 skills
                            st.markdown(f"🔧 **Skills:** {skills_str}")

                        with st.expander("View Description"):
                            st.write(job['summary'])
                            if job.get('skills') and len(job['skills']) > 5:
                                st.write(f"**All Skills:** {', '.join(job['skills'])}")

                    with col2:
                        if job['url']:
                            st.link_button("View Job", job['url'], use_container_width=True)

                    st.markdown("---")
        else:
            st.warning("No jobs found matching your criteria.")
            st.info("""
            **Troubleshooting Tips:**
            - Enable 'Show Debug Info' in the sidebar to see what happened during scraping
            - Try different keywords (e.g., 'software engineer', 'developer', 'analyst')
            - Try broader locations (e.g., 'Germany' instead of specific cities)
            - Some portals may be blocking automated requests - try selecting different portals
            - Check if your internet connection is working properly
            """)

            if st.session_state.show_debug and debug_info:
                st.subheader("What you can check:")
                for portal, info in debug_info.items():
                    status = info.get('status_code', 0)
                    jobs_found = info.get('jobs_found', 0)
                    error = info.get('error', '')

                    if status == 200 and jobs_found == 0:
                        st.warning(f"**{portal}**: Request succeeded but found no jobs. The search may be too specific or portal structure may have changed.")
                    elif error:
                        st.error(f"**{portal}**: {error}")
                    elif status != 200:
                        st.error(f"**{portal}**: HTTP error {status}")

    else:
        # Welcome screen
        st.info("👈 Enter your search parameters in the sidebar and click 'Search Jobs' to get started!")

        st.markdown("### About This App")
        st.markdown("""
        This app scans popular German job portals to help you find relevant job opportunities:

        **Supported Job Portals:**
        - **Indeed.de** - One of Germany's largest job search engines
        - **StepStone.de** - Leading German job board
        - **XING Jobs** - Professional network and job platform

        **Features:**
        - Real-time job scraping from multiple portals
        - Filter by job type, company, and portal
        - Export results to CSV
        - Clean and organized job listings

        **How to Use:**
        1. Enter job keywords (e.g., "Software Engineer", "Marketing Manager")
        2. Specify location in Germany (e.g., "Berlin", "Munich")
        3. Select job type and portals to search
        4. Click "Search Jobs" and wait for results
        5. Filter and export results as needed

        **Note:** Web scraping may occasionally fail if portal structures change. The app implements respectful delays between requests.
        """)


if __name__ == "__main__":
    main()
