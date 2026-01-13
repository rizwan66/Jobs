"""
Job scraper module for German job portals
"""
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Tuple, Optional
import time
import random
import logging
from datetime import datetime, timedelta
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class JobScraper:
    """Base class for job scraping"""

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        self.debug_info = {
            'url': '',
            'status_code': 0,
            'error': '',
            'jobs_found': 0,
            'selectors_tried': []
        }

    def scrape(self, keywords: str, location: str, job_type: str = "") -> Tuple[List[Dict], Dict]:
        """Override this method in subclasses"""
        raise NotImplementedError

    def _extract_job_level(self, title: str, summary: str) -> str:
        """Extract job level from title or summary"""
        text = f"{title} {summary}".lower()

        if any(word in text for word in ['entry level', 'junior', 'graduate', 'trainee', 'intern', 'praktikum']):
            return 'Entry Level'
        elif any(word in text for word in ['senior', 'lead', 'principal', 'staff', 'expert']):
            return 'Senior Level'
        elif any(word in text for word in ['mid-level', 'intermediate', 'experienced']):
            return 'Mid Level'
        elif any(word in text for word in ['director', 'head of', 'chief', 'vp', 'vice president', 'manager', 'leiter']):
            return 'Management'
        else:
            return 'Not Specified'

    def _extract_skills(self, summary: str) -> list:
        """Extract common technical skills from job summary"""
        if not summary:
            return []

        text = summary.lower()
        skills_found = []

        # Common technical skills
        skill_keywords = {
            'Python', 'Java', 'JavaScript', 'TypeScript', 'C++', 'C#', 'PHP', 'Ruby', 'Go', 'Rust', 'Swift', 'Kotlin',
            'React', 'Angular', 'Vue', 'Node.js', 'Django', 'Flask', 'Spring', 'Express',
            'SQL', 'MySQL', 'PostgreSQL', 'MongoDB', 'Redis', 'Oracle', 'NoSQL',
            'AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes', 'Jenkins', 'Git', 'CI/CD',
            'Machine Learning', 'AI', 'Data Science', 'Deep Learning', 'TensorFlow', 'PyTorch',
            'Agile', 'Scrum', 'DevOps', 'REST API', 'GraphQL', 'Microservices',
            'HTML', 'CSS', 'SASS', 'Bootstrap', 'Tailwind',
            'Linux', 'Unix', 'Windows Server', 'Networking',
            'SAP', 'Salesforce', 'Excel', 'Power BI', 'Tableau'
        }

        for skill in skill_keywords:
            if skill.lower() in text:
                skills_found.append(skill)

        return skills_found[:10]  # Limit to top 10 skills

    def _extract_posted_date(self, date_text: str) -> Optional[str]:
        """Extract and normalize posting date from text"""
        if not date_text:
            return None

        date_text = date_text.lower().strip()
        today = datetime.now()

        # Common patterns
        if 'heute' in date_text or 'today' in date_text:
            return today.strftime('%Y-%m-%d')
        elif 'gestern' in date_text or 'yesterday' in date_text:
            return (today - timedelta(days=1)).strftime('%Y-%m-%d')

        # X days/hours/minutes ago patterns
        time_patterns = [
            (r'vor (\d+) tag', 'days'),
            (r'(\d+) tag', 'days'),
            (r'vor (\d+) stunde', 'hours'),
            (r'(\d+) stunde', 'hours'),
            (r'vor (\d+) minute', 'minutes'),
            (r'(\d+) minute', 'minutes'),
            (r'(\d+)\s*d', 'days'),  # "5d ago"
            (r'(\d+)\s*h', 'hours'),  # "2h ago"
        ]

        for pattern, unit in time_patterns:
            match = re.search(pattern, date_text)
            if match:
                value = int(match.group(1))
                if unit == 'days':
                    return (today - timedelta(days=value)).strftime('%Y-%m-%d')
                elif unit == 'hours':
                    return (today - timedelta(hours=value)).strftime('%Y-%m-%d')
                elif unit == 'minutes':
                    return today.strftime('%Y-%m-%d')

        # Specific date patterns (dd.mm.yyyy or dd.mm.yy)
        date_match = re.search(r'(\d{1,2})\.(\d{1,2})\.(\d{2,4})', date_text)
        if date_match:
            day, month, year = date_match.groups()
            if len(year) == 2:
                year = '20' + year
            try:
                return f"{year}-{month.zfill(2)}-{day.zfill(2)}"
            except:
                pass

        return date_text  # Return original if no pattern matched


class IndeedDeScraper(JobScraper):
    """Scraper for Indeed.de"""

    def scrape(self, keywords: str, location: str, job_type: str = "", max_pages: int = 40) -> Tuple[List[Dict], Dict]:
        jobs = []
        self.debug_info = {
            'url': '',
            'status_code': 0,
            'error': '',
            'jobs_found': 0,
            'selectors_tried': [],
            'html_sample': '',
            'pages_scraped': 0
        }

        try:
            # Scrape multiple pages
            for page in range(min(max_pages, 100)):  # Limit to 40 pages max
                # Build URL
                base_url = "https://de.indeed.com/jobs"
                params = {
                    'q': keywords,
                    'l': location,
                    'start': page * 10  # Indeed uses start parameter for pagination
                }

                # Add job type filter if specified
                if job_type:
                    if job_type == "Full-time":
                        params['jt'] = 'fulltime'
                    elif job_type == "Part-time":
                        params['jt'] = 'parttime'
                    elif job_type == "Remote":
                        params['remotejob'] = '032b3046-06a3-4876-8dfd-474eb5e7ed11'

                response = requests.get(base_url, params=params, headers=self.headers, timeout=15)

                if page == 0:  # Store info from first page
                    self.debug_info['url'] = response.url
                    self.debug_info['status_code'] = response.status_code

                response.raise_for_status()

                soup = BeautifulSoup(response.content, 'html.parser')

                # Try multiple selectors for job cards (only log on first page)
                if page == 0:
                    selectors = [
                        ('div', 'job_seen_beacon'),
                        ('div', 'jobsearch-ResultsList'),
                        ('td', 'resultContent'),
                        ('div', 'cardOutline'),
                        ('a', 'jcs-JobTitle')
                    ]
                else:
                    selectors = [
                        ('div', 'job_seen_beacon'),
                        ('td', 'resultContent'),
                    ]

                job_cards = []
                for tag, class_name in selectors:
                    if page == 0:
                        self.debug_info['selectors_tried'].append(f"{tag}.{class_name}")

                    if tag == 'div' and class_name == 'jobsearch-ResultsList':
                        container = soup.find(tag, class_=class_name)
                        if container:
                            job_cards = container.find_all('div', class_='cardOutline')
                            if not job_cards:
                                job_cards = container.find_all('li')
                            if not job_cards:
                                job_cards = container.find_all('td', class_='resultContent')
                            if job_cards:
                                break
                    else:
                        job_cards = soup.find_all(tag, class_=class_name)
                        if job_cards:
                            break

                # Store HTML sample for debugging (first page only)
                if page == 0 and soup.body:
                    self.debug_info['html_sample'] = str(soup.body)[:500]

                logger.info(f"Indeed.de page {page + 1}: Found {len(job_cards)} job cards")

                # If no jobs found on this page, stop pagination
                if len(job_cards) == 0:
                    break

                page_jobs_added = 0
                for card in job_cards:
                    try:
                        # Try multiple selectors for title
                        title_elem = (card.find('h2', class_='jobTitle') or
                                     card.find('h2') or
                                     card.find('a', class_='jcs-JobTitle') or
                                     card.find('span', {'title': True}))

                        # Try multiple selectors for company
                        company_elem = (card.find('span', {'data-testid': 'company-name'}) or
                                       card.find('span', class_='companyName') or
                                       card.find('span', class_='company') or
                                       card.find('span', {'class': 'css-1h7lukg'}))

                        # Try multiple selectors for location
                        location_elem = (card.find('div', {'data-testid': 'text-location'}) or
                                        card.find('div', class_='companyLocation') or
                                        card.find('div', class_='location') or
                                        card.find('div', {'class': 'css-1p0sjhy'}))

                        # Try multiple selectors for summary
                        summary_elem = (card.find('div', class_='job-snippet') or
                                       card.find('div', class_='summary') or
                                       card.find('ul') or
                                       card.find('div', {'class': 'jobCardShelfContainer'}))

                        # Extract salary/pay information
                        salary_elem = (card.find('span', class_='salary-snippet') or
                                      card.find('div', class_='salary-snippet') or
                                      card.find('div', {'data-testid': 'attribute_snippet_testid'}))
                        salary = salary_elem.get_text(strip=True) if salary_elem else None

                        # Extract job URL - try multiple methods
                        job_link = ""
                        if title_elem:
                            link_elem = title_elem.find('a') if title_elem.name != 'a' else title_elem
                            if link_elem:
                                job_id = link_elem.get('data-jk', '') or link_elem.get('id', '').replace('job_', '')
                                if job_id:
                                    job_link = f"https://de.indeed.com/viewjob?jk={job_id}"
                                elif link_elem.get('href'):
                                    href = link_elem.get('href')
                                    if href.startswith('http'):
                                        job_link = href
                                    elif href.startswith('/'):
                                        job_link = f"https://de.indeed.com{href}"

                        title = title_elem.get_text(strip=True) if title_elem else None
                        company = company_elem.get_text(strip=True) if company_elem else 'Company not listed'
                        loc = location_elem.get_text(strip=True) if location_elem else location
                        summary = summary_elem.get_text(strip=True) if summary_elem else 'No description available'

                        # Extract job level from title or summary
                        job_level = self._extract_job_level(title, summary)

                        # Extract skills from summary
                        skills = self._extract_skills(summary)

                        # Extract posted date
                        date_elem = (card.find('span', {'data-testid': 'myJobsStateDate'}) or
                                   card.find('span', {'class': lambda x: x and 'date' in x.lower() if x else False}) or
                                   card.find('span', {'class': 'date'}))
                        date_text = date_elem.get_text(strip=True) if date_elem else None
                        posted_date = self._extract_posted_date(date_text) if date_text else None

                        # Only add job if we have at least a title and not duplicate
                        if title and not any(j['title'] == title and j['company'] == company for j in jobs):
                            job = {
                                'title': title,
                                'company': company,
                                'location': loc,
                                'summary': summary[:300],  # Limit summary length
                                'url': job_link,
                                'portal': 'Indeed.de',
                                'salary': salary,
                                'job_level': job_level,
                                'skills': skills,
                                'posted_date': posted_date
                            }
                            jobs.append(job)
                            page_jobs_added += 1
                    except Exception as e:
                        logger.debug(f"Error parsing job card: {str(e)}")
                        continue

                self.debug_info['pages_scraped'] = page + 1

                # Stop if we didn't add any new jobs from this page
                if page_jobs_added == 0:
                    break

                # Respectful delay between pages
                time.sleep(random.uniform(1.5, 2.5))

            self.debug_info['jobs_found'] = len(jobs)

        except requests.exceptions.RequestException as e:
            self.debug_info['error'] = f"Network error: {str(e)}"
            logger.error(f"Error scraping Indeed.de: {str(e)}")
        except Exception as e:
            self.debug_info['error'] = f"Parsing error: {str(e)}"
            logger.error(f"Error scraping Indeed.de: {str(e)}")

        return jobs, self.debug_info


class StepStoneScraper(JobScraper):
    """Scraper for StepStone.de"""

    def scrape(self, keywords: str, location: str, job_type: str = "", max_pages: int = 40) -> Tuple[List[Dict], Dict]:
        jobs = []
        self.debug_info = {
            'url': '',
            'status_code': 0,
            'error': '',
            'jobs_found': 0,
            'selectors_tried': [],
            'html_sample': '',
            'pages_scraped': 0
        }

        try:
            # Scrape multiple pages
            for page in range(1, min(max_pages + 1, 41)):  # StepStone pages start at 1
                # Try different URL patterns
                base_url = "https://www.stepstone.de/work"

                # Build search query - StepStone uses a different URL structure
                search_terms = keywords.replace(' ', '-').lower()
                location_term = location.replace(' ', '-').lower()

                url = f"{base_url}/{search_terms}-jobs-in-{location_term}"

                params = {'page': page} if page > 1 else {}

                response = requests.get(url, params=params, headers=self.headers, timeout=15)

                if page == 1:  # Store info from first page
                    self.debug_info['url'] = response.url
                    self.debug_info['status_code'] = response.status_code

                response.raise_for_status()

                soup = BeautifulSoup(response.content, 'html.parser')

                # Try multiple selectors for job listings
                if page == 1:
                    selectors = [
                        ('article', {'data-at': 'job-item'}),
                        ('article', {'class': 'res-'}),
                        ('li', {'data-at': 'job-item'}),
                        ('div', {'class': 'job-element'}),
                        ('article', None),  # Try all article tags
                    ]
                else:
                    selectors = [
                        ('article', {'data-at': 'job-item'}),
                        ('article', None),
                    ]

                job_cards = []
                for tag, attrs in selectors:
                    if page == 1:
                        self.debug_info['selectors_tried'].append(f"{tag} with {attrs}")

                    if attrs:
                        job_cards = soup.find_all(tag, attrs)
                    else:
                        # Find all articles, then filter those that look like job cards
                        all_tags = soup.find_all(tag)
                        job_cards = [t for t in all_tags if t.find('a') and (t.find('h2') or t.find('h3'))]

                    if job_cards:
                        break

                # Store HTML sample for debugging (first page only)
                if page == 1 and soup.body:
                    self.debug_info['html_sample'] = str(soup.body)[:500]

                logger.info(f"StepStone.de page {page}: Found {len(job_cards)} job cards")

                # If no jobs found on this page, stop pagination
                if len(job_cards) == 0:
                    break

                page_jobs_added = 0
                for card in job_cards:
                    try:
                        # Try multiple selectors for title
                        title_elem = (card.find('h2') or
                                     card.find('h3') or
                                     card.find('a', {'data-at': 'job-item-title'}) or
                                     card.find('a', class_=lambda x: x and 'title' in x.lower() if x else False))

                        # Try multiple selectors for company
                        company_elem = (card.find('span', {'data-at': 'job-item-company-name'}) or
                                       card.find('a', {'data-at': 'job-item-company-name'}) or
                                       card.find('div', class_=lambda x: x and 'company' in x.lower() if x else False) or
                                       card.find('span', class_=lambda x: x and 'company' in x.lower() if x else False))

                        # Try multiple selectors for location
                        location_elem = (card.find('span', {'data-at': 'job-item-location'}) or
                                        card.find('div', class_=lambda x: x and 'location' in x.lower() if x else False) or
                                        card.find('span', class_=lambda x: x and 'location' in x.lower() if x else False))

                        # Extract title
                        if title_elem and title_elem.find('a'):
                            title_link = title_elem.find('a')
                            title = title_link.get_text(strip=True)
                        elif title_elem:
                            title = title_elem.get_text(strip=True)
                        else:
                            title = None

                        company = company_elem.get_text(strip=True) if company_elem else 'Company not listed'
                        loc = location_elem.get_text(strip=True) if location_elem else location

                        # Try to extract salary
                        salary_elem = card.find('span', {'data-at': 'job-item-salary'}) or card.find('span', class_=lambda x: x and 'salary' in x.lower() if x else False)
                        salary = salary_elem.get_text(strip=True) if salary_elem else None

                        # Extract URL - try to find any link in the card
                        job_url = ""
                        link_elem = card.find('a', href=True)
                        if link_elem:
                            job_url = link_elem.get('href')
                            if job_url and not job_url.startswith('http'):
                                job_url = f"https://www.stepstone.de{job_url}"

                        # Extract job level and skills
                        summary = f"{title} {company} {loc}"
                        job_level = self._extract_job_level(title, summary)
                        skills = self._extract_skills(summary)

                        # Extract posted date
                        date_elem = (card.find('span', {'class': lambda x: x and 'date' in x.lower() or x and 'time' in x.lower() if x else False}) or
                                   card.find('time'))
                        date_text = date_elem.get_text(strip=True) if date_elem else None
                        posted_date = self._extract_posted_date(date_text) if date_text else None

                        # Only add job if we have at least a title and not duplicate
                        if title and not any(j['title'] == title and j['company'] == company for j in jobs):
                            job = {
                                'title': title,
                                'company': company,
                                'location': loc,
                                'summary': 'See full details on StepStone',
                                'url': job_url,
                                'portal': 'StepStone.de',
                                'salary': salary,
                                'job_level': job_level,
                                'skills': skills,
                                'posted_date': posted_date
                            }
                            jobs.append(job)
                            page_jobs_added += 1
                    except Exception as e:
                        logger.debug(f"Error parsing job card: {str(e)}")
                        continue

                self.debug_info['pages_scraped'] = page

                # Stop if we didn't add any new jobs from this page
                if page_jobs_added == 0:
                    break

                # Respectful delay between pages
                time.sleep(random.uniform(1.5, 2.5))

            self.debug_info['jobs_found'] = len(jobs)

        except requests.exceptions.RequestException as e:
            self.debug_info['error'] = f"Network error: {str(e)}"
            logger.error(f"Error scraping StepStone.de: {str(e)}")
        except Exception as e:
            self.debug_info['error'] = f"Parsing error: {str(e)}"
            logger.error(f"Error scraping StepStone.de: {str(e)}")

        return jobs, self.debug_info


class XingJobsScraper(JobScraper):
    """Scraper for XING Jobs"""

    def scrape(self, keywords: str, location: str, job_type: str = "", max_pages: int = 40) -> Tuple[List[Dict], Dict]:
        jobs = []
        self.debug_info = {
            'url': '',
            'status_code': 0,
            'error': '',
            'jobs_found': 0,
            'selectors_tried': [],
            'html_sample': '',
            'pages_scraped': 0
        }

        try:
            # Scrape multiple pages
            for page in range(1, min(max_pages + 1, 41)):  # XING pages start at 1
                base_url = "https://www.xing.com/jobs/search"
                params = {
                    'keywords': keywords,
                    'location': location,
                    'page': page
                }

                response = requests.get(base_url, params=params, headers=self.headers, timeout=15)

                if page == 1:  # Store info from first page
                    self.debug_info['url'] = response.url
                    self.debug_info['status_code'] = response.status_code

                response.raise_for_status()

                soup = BeautifulSoup(response.content, 'html.parser')

                # Try multiple selectors for XING jobs
                if page == 1:
                    selectors = [
                        ('div', {'data-xds': 'JobTeaser'}),
                        ('article', {'class': 'job'}),
                        ('div', {'class': 'job-card'}),
                        ('li', {'class': 'job-posting'}),
                        ('a', {'class': lambda x: x and 'job' in x.lower() if x else False}),
                        ('div', None),  # Try generic divs with links
                    ]
                else:
                    selectors = [
                        ('div', {'data-xds': 'JobTeaser'}),
                        ('article', {'class': 'job'}),
                    ]

                job_cards = []
                for tag, attrs in selectors:
                    if page == 1:
                        self.debug_info['selectors_tried'].append(f"{tag} with {attrs}")

                    if attrs:
                        if isinstance(attrs, dict):
                            job_cards = soup.find_all(tag, attrs)
                        else:
                            job_cards = soup.find_all(tag, class_=attrs)
                    else:
                        # Find divs/articles that contain job-like content
                        all_tags = soup.find_all(tag)
                        job_cards = [t for t in all_tags if t.find('a', href=True) and (t.find('h2') or t.find('h3') or t.find('h4'))]

                    if job_cards:
                        break

                # Store HTML sample for debugging (first page only)
                if page == 1 and soup.body:
                    self.debug_info['html_sample'] = str(soup.body)[:500]

                logger.info(f"XING Jobs page {page}: Found {len(job_cards)} job cards")

                # If no jobs found on this page, stop pagination
                if len(job_cards) == 0:
                    break

                page_jobs_added = 0
                for card in job_cards:
                    try:
                        # Extract title and link
                        title = None
                        url = ""
                        company = 'See on XING'

                        # Try to find title in various places
                        title_elem = (card.find('h2') or
                                     card.find('h3') or
                                     card.find('h4') or
                                     card.find('a', {'class': lambda x: x and 'title' in x.lower() if x else False}) or
                                     card.find('a', href=True))

                        if title_elem:
                            if title_elem.name == 'a':
                                title = title_elem.get_text(strip=True)
                                url = title_elem.get('href', '')
                            else:
                                link_in_title = title_elem.find('a')
                                if link_in_title:
                                    title = link_in_title.get_text(strip=True)
                                    url = link_in_title.get('href', '')
                                else:
                                    title = title_elem.get_text(strip=True)
                                    # Try to find a link elsewhere in card
                                    link_elem = card.find('a', href=True)
                                    url = link_elem.get('href', '') if link_elem else ''

                        # Try to extract company if available
                        company_elem = (card.find('span', {'class': lambda x: x and 'company' in x.lower() if x else False}) or
                                       card.find('div', {'class': lambda x: x and 'company' in x.lower() if x else False}) or
                                       card.find('a', {'class': lambda x: x and 'company' in x.lower() if x else False}))

                        if company_elem:
                            company = company_elem.get_text(strip=True)

                        # Try to extract salary
                        salary_elem = card.find('span', class_=lambda x: x and 'salary' in x.lower() if x else False)
                        salary = salary_elem.get_text(strip=True) if salary_elem else None

                        # Make URL absolute
                        if url and not url.startswith('http'):
                            url = f"https://www.xing.com{url}"

                        # Extract job level and skills
                        summary = f"{title} {company}"
                        job_level = self._extract_job_level(title, summary)
                        skills = self._extract_skills(summary)

                        # Extract posted date
                        date_elem = (card.find('span', {'class': lambda x: x and 'date' in x.lower() or x and 'time' in x.lower() if x else False}) or
                                   card.find('time'))
                        date_text = date_elem.get_text(strip=True) if date_elem else None
                        posted_date = self._extract_posted_date(date_text) if date_text else None

                        # Only add job if we have at least a title and not duplicate
                        if title and not any(j['title'] == title and j['company'] == company for j in jobs):
                            job = {
                                'title': title,
                                'company': company,
                                'location': location,
                                'summary': 'Full details available on XING',
                                'url': url,
                                'portal': 'XING Jobs',
                                'salary': salary,
                                'job_level': job_level,
                                'skills': skills,
                                'posted_date': posted_date
                            }
                            jobs.append(job)
                            page_jobs_added += 1
                    except Exception as e:
                        logger.debug(f"Error parsing job card: {str(e)}")
                        continue

                self.debug_info['pages_scraped'] = page

                # Stop if we didn't add any new jobs from this page
                if page_jobs_added == 0:
                    break

                # Respectful delay between pages
                time.sleep(random.uniform(1.5, 2.5))

            self.debug_info['jobs_found'] = len(jobs)

        except requests.exceptions.RequestException as e:
            self.debug_info['error'] = f"Network error: {str(e)}"
            logger.error(f"Error scraping XING Jobs: {str(e)}")
        except Exception as e:
            self.debug_info['error'] = f"Parsing error: {str(e)}"
            logger.error(f"Error scraping XING Jobs: {str(e)}")

        return jobs, self.debug_info


class MonsterDeScraper(JobScraper):
    """Scraper for Monster.de"""

    def scrape(self, keywords: str, location: str, job_type: str = "", max_pages: int = 100) -> Tuple[List[Dict], Dict]:
        jobs = []
        self.debug_info = {
            'url': '',
            'status_code': 0,
            'error': '',
            'jobs_found': 0,
            'selectors_tried': [],
            'html_sample': '',
            'pages_scraped': 0
        }

        try:
            seen_urls = set()

            # Scrape multiple pages
            for page in range(min(max_pages, 100)):
                # Monster.de uses page parameter
                params = {
                    'q': keywords,
                    'where': location,
                    'page': page + 1
                }

                base_url = "https://www.monster.de/jobs/suche"

                # First page has different URL structure
                if page == 0:
                    url = f"{base_url}?q={keywords.replace(' ', '+')}&where={location.replace(' ', '+')}"
                else:
                    url = f"{base_url}?q={keywords.replace(' ', '+')}&where={location.replace(' ', '+')}&page={page + 1}"

                self.debug_info['url'] = url

                response = requests.get(url, headers=self.headers, timeout=15)
                self.debug_info['status_code'] = response.status_code
                response.raise_for_status()

                soup = BeautifulSoup(response.content, 'lxml')

                # Multiple selector strategies for Monster.de
                job_cards_selectors = [
                    ('div', {'class': lambda x: x and 'job-card' in x.lower() if x else False}),
                    ('div', {'data-test-id': 'svx-job-card'}),
                    ('article', {'class': lambda x: x and 'job' in x.lower() if x else False}),
                    ('div', {'class': 'card'}),
                    ('section', {'class': lambda x: x and 'card' in x.lower() if x else False}),
                ]

                job_cards = []
                for tag, attrs in job_cards_selectors:
                    self.debug_info['selectors_tried'].append(f"{tag} with {attrs}")
                    job_cards = soup.find_all(tag, attrs, limit=50)
                    if job_cards:
                        break

                if not job_cards:
                    if page == 0:
                        self.debug_info['html_sample'] = str(soup)[:1000]
                    break

                self.debug_info['pages_scraped'] = page + 1
                page_jobs_count = 0

                for card in job_cards:
                    try:
                        # Extract title with multiple fallbacks
                        title_elem = (card.find('h2') or
                                    card.find('h3') or
                                    card.find('a', {'data-test-id': 'svx-job-title'}) or
                                    card.find('a', {'class': lambda x: x and 'title' in x.lower() if x else False}))

                        if not title_elem:
                            continue

                        title = title_elem.get_text(strip=True)

                        # Extract company
                        company_elem = (card.find('div', {'data-test-id': 'svx-job-company'}) or
                                      card.find('span', {'class': lambda x: x and 'company' in x.lower() if x else False}) or
                                      card.find('div', {'class': lambda x: x and 'company' in x.lower() if x else False}))
                        company = company_elem.get_text(strip=True) if company_elem else "Company not specified"

                        # Extract location
                        location_elem = (card.find('div', {'data-test-id': 'svx-job-location'}) or
                                       card.find('span', {'class': lambda x: x and 'location' in x.lower() if x else False}) or
                                       card.find('div', {'class': lambda x: x and 'location' in x.lower() if x else False}))
                        loc = location_elem.get_text(strip=True) if location_elem else location

                        # Extract summary
                        summary_elem = (card.find('div', {'class': lambda x: x and 'description' in x.lower() if x else False}) or
                                      card.find('p') or
                                      card.find('div', {'class': lambda x: x and 'summary' in x.lower() if x else False}))
                        summary = summary_elem.get_text(strip=True)[:300] if summary_elem else ""

                        # Extract URL
                        link_elem = title_elem if title_elem.name == 'a' else card.find('a')
                        job_link = link_elem.get('href', '') if link_elem else ''
                        if job_link and not job_link.startswith('http'):
                            job_link = f"https://www.monster.de{job_link}"

                        # Skip duplicates
                        if job_link in seen_urls:
                            continue
                        seen_urls.add(job_link)

                        # Extract salary
                        salary_elem = (card.find('span', {'class': lambda x: x and 'salary' in x.lower() if x else False}) or
                                     card.find('div', {'class': lambda x: x and 'salary' in x.lower() if x else False}))
                        salary = salary_elem.get_text(strip=True) if salary_elem else None

                        # Extract job level and skills
                        job_level = self._extract_job_level(title, summary)
                        skills = self._extract_skills(summary)

                        # Extract posted date
                        date_elem = (card.find('span', {'class': lambda x: x and 'date' in x.lower() or x and 'time' in x.lower() if x else False}) or
                                   card.find('div', {'class': lambda x: x and 'date' in x.lower() or x and 'time' in x.lower() if x else False}) or
                                   card.find('time'))
                        date_text = date_elem.get_text(strip=True) if date_elem else None
                        posted_date = self._extract_posted_date(date_text) if date_text else None

                        job = {
                            'title': title,
                            'company': company,
                            'location': loc,
                            'summary': summary,
                            'url': job_link,
                            'portal': 'Monster.de',
                            'salary': salary,
                            'job_level': job_level,
                            'skills': skills,
                            'posted_date': posted_date
                        }

                        jobs.append(job)
                        page_jobs_count += 1

                    except Exception as e:
                        logger.debug(f"Error parsing Monster.de job card: {str(e)}")
                        continue

                if page_jobs_count == 0:
                    break

                # Respectful delay between pages
                time.sleep(random.uniform(1.5, 2.5))

            self.debug_info['jobs_found'] = len(jobs)

        except requests.exceptions.RequestException as e:
            self.debug_info['error'] = f"Network error: {str(e)}"
            logger.error(f"Error scraping Monster.de: {str(e)}")
        except Exception as e:
            self.debug_info['error'] = f"Parsing error: {str(e)}"
            logger.error(f"Error scraping Monster.de: {str(e)}")

        return jobs, self.debug_info


class ArbeitsagenturScraper(JobScraper):
    """Scraper for Arbeitsagentur.de (German Federal Employment Agency)"""

    def scrape(self, keywords: str, location: str, job_type: str = "", max_pages: int = 100) -> Tuple[List[Dict], Dict]:
        jobs = []
        self.debug_info = {
            'url': '',
            'status_code': 0,
            'error': '',
            'jobs_found': 0,
            'selectors_tried': [],
            'html_sample': '',
            'pages_scraped': 0
        }

        try:
            seen_urls = set()

            # Scrape multiple pages
            for page in range(min(max_pages, 100)):
                # Arbeitsagentur uses page parameter
                params = {
                    'was': keywords,
                    'wo': location,
                    'page': page
                }

                base_url = "https://www.arbeitsagentur.de/jobsuche"

                if page == 0:
                    url = f"{base_url}?was={keywords.replace(' ', '+')}&wo={location.replace(' ', '+')}"
                else:
                    url = f"{base_url}?was={keywords.replace(' ', '+')}&wo={location.replace(' ', '+')}&page={page}"

                self.debug_info['url'] = url

                response = requests.get(url, headers=self.headers, timeout=15)
                self.debug_info['status_code'] = response.status_code
                response.raise_for_status()

                soup = BeautifulSoup(response.content, 'lxml')

                # Multiple selector strategies for Arbeitsagentur
                job_cards_selectors = [
                    ('div', {'class': lambda x: x and 'job' in x.lower() and 'card' in x.lower() if x else False}),
                    ('article', {'class': lambda x: x and 'job' in x.lower() if x else False}),
                    ('div', {'data-test': lambda x: x and 'job' in x.lower() if x else False}),
                    ('li', {'class': lambda x: x and 'result' in x.lower() if x else False}),
                    ('div', {'class': 'result-item'}),
                ]

                job_cards = []
                for tag, attrs in job_cards_selectors:
                    self.debug_info['selectors_tried'].append(f"{tag} with {attrs}")
                    job_cards = soup.find_all(tag, attrs, limit=50)
                    if job_cards:
                        break

                if not job_cards:
                    if page == 0:
                        self.debug_info['html_sample'] = str(soup)[:1000]
                    break

                self.debug_info['pages_scraped'] = page + 1
                page_jobs_count = 0

                for card in job_cards:
                    try:
                        # Extract title with multiple fallbacks
                        title_elem = (card.find('h3') or
                                    card.find('h2') or
                                    card.find('a', {'class': lambda x: x and 'title' in x.lower() if x else False}) or
                                    card.find('span', {'class': lambda x: x and 'title' in x.lower() if x else False}))

                        if not title_elem:
                            continue

                        title = title_elem.get_text(strip=True)

                        # Extract company
                        company_elem = (card.find('span', {'class': lambda x: x and 'company' in x.lower() if x else False}) or
                                      card.find('div', {'class': lambda x: x and 'company' in x.lower() if x else False}) or
                                      card.find('p', {'class': lambda x: x and 'company' in x.lower() if x else False}))
                        company = company_elem.get_text(strip=True) if company_elem else "Company not specified"

                        # Extract location
                        location_elem = (card.find('span', {'class': lambda x: x and 'location' in x.lower() or x and 'ort' in x.lower() if x else False}) or
                                       card.find('div', {'class': lambda x: x and 'location' in x.lower() or x and 'ort' in x.lower() if x else False}))
                        loc = location_elem.get_text(strip=True) if location_elem else location

                        # Extract summary
                        summary_elem = (card.find('div', {'class': lambda x: x and 'description' in x.lower() if x else False}) or
                                      card.find('p', {'class': lambda x: x and 'text' in x.lower() or x and 'beschreibung' in x.lower() if x else False}) or
                                      card.find('p'))
                        summary = summary_elem.get_text(strip=True)[:300] if summary_elem else ""

                        # Extract URL
                        link_elem = title_elem if title_elem.name == 'a' else card.find('a')
                        job_link = link_elem.get('href', '') if link_elem else ''
                        if job_link and not job_link.startswith('http'):
                            job_link = f"https://www.arbeitsagentur.de{job_link}"

                        # Skip duplicates
                        if job_link in seen_urls:
                            continue
                        seen_urls.add(job_link)

                        # Extract salary
                        salary_elem = (card.find('span', {'class': lambda x: x and 'salary' in x.lower() or x and 'gehalt' in x.lower() if x else False}) or
                                     card.find('div', {'class': lambda x: x and 'salary' in x.lower() or x and 'gehalt' in x.lower() if x else False}))
                        salary = salary_elem.get_text(strip=True) if salary_elem else None

                        # Extract posted date
                        date_elem = (card.find('span', {'class': lambda x: x and 'date' in x.lower() or x and 'time' in x.lower() if x else False}) or
                                   card.find('div', {'class': lambda x: x and 'date' in x.lower() or x and 'time' in x.lower() if x else False}) or
                                   card.find('time'))
                        date_text = date_elem.get_text(strip=True) if date_elem else None
                        posted_date = self._extract_posted_date(date_text) if date_text else None

                        # Extract job level and skills
                        job_level = self._extract_job_level(title, summary)
                        skills = self._extract_skills(summary)

                        job = {
                            'title': title,
                            'company': company,
                            'location': loc,
                            'summary': summary,
                            'url': job_link,
                            'portal': 'Arbeitsagentur.de',
                            'salary': salary,
                            'job_level': job_level,
                            'skills': skills,
                            'posted_date': posted_date
                        }

                        jobs.append(job)
                        page_jobs_count += 1

                    except Exception as e:
                        logger.debug(f"Error parsing Arbeitsagentur job card: {str(e)}")
                        continue

                if page_jobs_count == 0:
                    break

                # Respectful delay between pages
                time.sleep(random.uniform(1.5, 2.5))

            self.debug_info['jobs_found'] = len(jobs)

        except requests.exceptions.RequestException as e:
            self.debug_info['error'] = f"Network error: {str(e)}"
            logger.error(f"Error scraping Arbeitsagentur.de: {str(e)}")
        except Exception as e:
            self.debug_info['error'] = f"Parsing error: {str(e)}"
            logger.error(f"Error scraping Arbeitsagentur.de: {str(e)}")

        return jobs, self.debug_info


class LinkedInScraper(JobScraper):
    """Scraper for LinkedIn (Note: LinkedIn has strict anti-scraping measures)"""

    def scrape(self, keywords: str, location: str, job_type: str = "", max_pages: int = 100) -> Tuple[List[Dict], Dict]:
        jobs = []
        self.debug_info = {
            'url': '',
            'status_code': 0,
            'error': '',
            'jobs_found': 0,
            'selectors_tried': [],
            'html_sample': '',
            'pages_scraped': 0
        }

        try:
            seen_urls = set()

            # Scrape multiple pages
            for page in range(min(max_pages, 100)):
                # LinkedIn uses start parameter (25 jobs per page)
                start = page * 25

                # LinkedIn public jobs search URL
                params = {
                    'keywords': keywords,
                    'location': location,
                    'start': start
                }

                url = f"https://www.linkedin.com/jobs/search?keywords={keywords.replace(' ', '%20')}&location={location.replace(' ', '%20')}&start={start}"
                self.debug_info['url'] = url

                response = requests.get(url, headers=self.headers, timeout=15)
                self.debug_info['status_code'] = response.status_code
                response.raise_for_status()

                soup = BeautifulSoup(response.content, 'lxml')

                # Multiple selector strategies for LinkedIn
                job_cards_selectors = [
                    ('li', {'class': lambda x: x and 'job' in x.lower() if x else False}),
                    ('div', {'class': lambda x: x and 'job-search-card' in x.lower() if x else False}),
                    ('div', {'data-entity-urn': lambda x: x and 'job' in x.lower() if x else False}),
                    ('article', {'class': lambda x: x and 'job' in x.lower() if x else False}),
                ]

                job_cards = []
                for tag, attrs in job_cards_selectors:
                    self.debug_info['selectors_tried'].append(f"{tag} with {attrs}")
                    job_cards = soup.find_all(tag, attrs, limit=50)
                    if job_cards:
                        break

                if not job_cards:
                    if page == 0:
                        self.debug_info['html_sample'] = str(soup)[:1000]
                        self.debug_info['error'] = "LinkedIn may be blocking automated access. Consider using LinkedIn API or reducing request frequency."
                    break

                self.debug_info['pages_scraped'] = page + 1
                page_jobs_count = 0

                for card in job_cards:
                    try:
                        # Extract title
                        title_elem = (card.find('h3', {'class': lambda x: x and 'job' in x.lower() if x else False}) or
                                    card.find('h3') or
                                    card.find('a', {'class': lambda x: x and 'job-title' in x.lower() if x else False}))

                        if not title_elem:
                            continue

                        title = title_elem.get_text(strip=True)

                        # Extract company
                        company_elem = (card.find('h4', {'class': lambda x: x and 'company' in x.lower() if x else False}) or
                                      card.find('a', {'class': lambda x: x and 'company' in x.lower() if x else False}) or
                                      card.find('span', {'class': lambda x: x and 'company' in x.lower() if x else False}))
                        company = company_elem.get_text(strip=True) if company_elem else "Company not specified"

                        # Extract location
                        location_elem = (card.find('span', {'class': lambda x: x and 'location' in x.lower() if x else False}) or
                                       card.find('div', {'class': lambda x: x and 'location' in x.lower() if x else False}))
                        loc = location_elem.get_text(strip=True) if location_elem else location

                        # Extract summary
                        summary_elem = card.find('p') or card.find('div', {'class': lambda x: x and 'description' in x.lower() if x else False})
                        summary = summary_elem.get_text(strip=True)[:300] if summary_elem else ""

                        # Extract URL
                        link_elem = card.find('a', {'class': lambda x: x and 'job' in x.lower() if x else False}) or card.find('a')
                        job_link = link_elem.get('href', '') if link_elem else ''
                        if job_link and not job_link.startswith('http'):
                            job_link = f"https://www.linkedin.com{job_link}"

                        # Skip duplicates
                        if job_link in seen_urls:
                            continue
                        seen_urls.add(job_link)

                        # Extract salary
                        salary_elem = card.find('span', {'class': lambda x: x and 'salary' in x.lower() if x else False})
                        salary = salary_elem.get_text(strip=True) if salary_elem else None

                        # Extract job level and skills
                        job_level = self._extract_job_level(title, summary)
                        skills = self._extract_skills(summary)

                        job = {
                            'title': title,
                            'company': company,
                            'location': loc,
                            'summary': summary,
                            'url': job_link,
                            'portal': 'LinkedIn',
                            'salary': salary,
                            'job_level': job_level,
                            'skills': skills
                        }

                        jobs.append(job)
                        page_jobs_count += 1

                    except Exception as e:
                        logger.debug(f"Error parsing LinkedIn job card: {str(e)}")
                        continue

                if page_jobs_count == 0:
                    break

                # Longer delay for LinkedIn due to anti-scraping measures
                time.sleep(random.uniform(2.5, 4.0))

            self.debug_info['jobs_found'] = len(jobs)

        except requests.exceptions.RequestException as e:
            self.debug_info['error'] = f"Network error: {str(e)}"
            logger.error(f"Error scraping LinkedIn: {str(e)}")
        except Exception as e:
            self.debug_info['error'] = f"Parsing error: {str(e)}"
            logger.error(f"Error scraping LinkedIn: {str(e)}")

        return jobs, self.debug_info


def scrape_all_portals(keywords: str, location: str, job_type: str = "", selected_portals: List[str] = None, max_pages: int = 100) -> Tuple[List[Dict], Dict]:
    """
    Scrape all selected job portals

    Args:
        keywords: Job search keywords
        location: Location to search
        job_type: Type of job (Full-time, Part-time, Remote, etc.)
        selected_portals: List of portal names to scrape
        max_pages: Maximum number of pages to scrape per portal (default: 40)

    Returns:
        Tuple of (List of job dictionaries, Debug information dictionary)
    """
    all_jobs = []
    debug_summary = {}

    scrapers = {
        'Indeed.de': IndeedDeScraper(),
        'StepStone.de': StepStoneScraper(),
        'XING Jobs': XingJobsScraper(),
        'Monster.de': MonsterDeScraper(),
        'Arbeitsagentur.de': ArbeitsagenturScraper(),
    }

    if selected_portals is None:
        selected_portals = list(scrapers.keys())

    for portal_name in selected_portals:
        if portal_name in scrapers:
            try:
                scraper = scrapers[portal_name]
                jobs, debug_info = scraper.scrape(keywords, location, job_type, max_pages)
                all_jobs.extend(jobs)
                debug_summary[portal_name] = debug_info
                logger.info(f"{portal_name}: Retrieved {len(jobs)} jobs from {debug_info.get('pages_scraped', 0)} pages")
            except Exception as e:
                debug_summary[portal_name] = {
                    'error': f"Unexpected error: {str(e)}",
                    'jobs_found': 0,
                    'pages_scraped': 0
                }
                logger.error(f"Error with {portal_name}: {str(e)}")

    return all_jobs, debug_summary
