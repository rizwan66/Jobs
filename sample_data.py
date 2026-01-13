"""
Sample job data for testing when scrapers fail
"""

def get_sample_jobs(keywords: str, location: str):
    """
    Generate sample job data for testing purposes
    """
    return [
        {
            'title': f'Senior {keywords} (m/w/d)',
            'company': 'TechCorp GmbH',
            'location': location,
            'summary': f'We are looking for an experienced {keywords} to join our team in {location}. You will work on exciting projects with modern technologies including Python, React, and AWS.',
            'url': 'https://de.indeed.com',
            'portal': 'Sample Data',
            'salary': '€70,000 - €90,000 per year',
            'job_level': 'Senior Level',
            'skills': ['Python', 'React', 'AWS', 'Docker', 'Git']
        },
        {
            'title': f'{keywords} - Full Stack',
            'company': 'Digital Solutions AG',
            'location': location,
            'summary': f'Join our dynamic team as a {keywords}. We offer flexible working hours, remote work options, and competitive salary. Experience with JavaScript, Node.js, and MongoDB required.',
            'url': 'https://www.stepstone.de',
            'portal': 'Sample Data',
            'salary': '€55,000 - €75,000 per year',
            'job_level': 'Mid Level',
            'skills': ['JavaScript', 'Node.js', 'MongoDB', 'React', 'TypeScript']
        },
        {
            'title': f'Junior {keywords}',
            'company': 'StartUp Innovation',
            'location': location,
            'summary': f'Great opportunity for junior {keywords} to grow their career. Training and mentorship provided. Work with Java, Spring, and PostgreSQL.',
            'url': 'https://www.xing.com',
            'portal': 'Sample Data',
            'salary': '€40,000 - €50,000 per year',
            'job_level': 'Entry Level',
            'skills': ['Java', 'Spring', 'PostgreSQL', 'Git', 'Agile']
        },
        {
            'title': f'Lead {keywords} - Remote',
            'company': 'CloudTech Solutions',
            'location': 'Remote, ' + location,
            'summary': f'Remote position for experienced {keywords}. Lead a team of talented developers and shape our technical direction. Kubernetes and DevOps experience essential.',
            'url': 'https://de.indeed.com',
            'portal': 'Sample Data',
            'salary': '€90,000 - €120,000 per year',
            'job_level': 'Management',
            'skills': ['Kubernetes', 'DevOps', 'Python', 'AWS', 'CI/CD']
        },
        {
            'title': f'{keywords} with React/Node.js',
            'company': 'WebDev GmbH',
            'location': location,
            'summary': f'We are seeking a skilled {keywords} with experience in modern web technologies. Join our growing team working with React, Node.js, and GraphQL.',
            'url': 'https://www.stepstone.de',
            'portal': 'Sample Data',
            'salary': None,
            'job_level': 'Mid Level',
            'skills': ['React', 'Node.js', 'GraphQL', 'TypeScript', 'Docker']
        }
    ]
