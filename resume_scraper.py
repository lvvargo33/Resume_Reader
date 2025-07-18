import requests
import time
import json
import random
import os
import logging
from datetime import datetime
import csv
import base64
import re
from typing import List, Dict, Optional

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# GitHub API Configuration
GITHUB_API_BASE = "https://api.github.com"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # Set your token as environment variable

if not GITHUB_TOKEN:
    logger.warning("GitHub token not found. Please set GITHUB_TOKEN environment variable.")
    logger.warning("You can set it with: export GITHUB_TOKEN=your_token_here")

class Job:
    def __init__(self, title, company, location, hire_date, description="", duration=""):
        self.title = title
        self.company = company
        self.location = location
        self.hire_date = hire_date
        self.description = description
        self.duration = duration

class School:
    def __init__(self, degree, school_name, grad_date, field_of_study=""):
        self.degree = degree
        self.school_name = school_name
        self.grad_date = grad_date
        self.field_of_study = field_of_study

class Resume:
    def __init__(self, resume_id):
        self.id = resume_id
        self.jobs = []
        self.schools = []
        self.skills = []
        self.summary = ""
        self.location = ""
        self.experience_level = ""

class GitHubResumeCollector:
    def __init__(self):
        self.session_start = datetime.now()
        self.request_count = 0
        self.daily_limit = 4500  # Conservative limit (5000 max)
        self.session_limit = 1000
        self.min_delay = 0.5  # Faster delays for API
        self.max_delay = 2.0
        self.consecutive_errors = 0
        self.max_consecutive_errors = 3
        
        # GitHub API headers
        self.headers = {
            'Authorization': f'token {GITHUB_TOKEN}',
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'Resume-Research-Bot/1.0'
        }
        
        # Resume indicators for repository search
        self.resume_keywords = [
            'resume', 'cv', 'curriculum-vitae', 'portfolio', 
            'profile', 'about-me', 'personal-website'
        ]
        
        # Programming languages to look for
        self.tech_languages = [
            'python', 'javascript', 'java', 'typescript', 'go', 
            'rust', 'cpp', 'csharp', 'ruby', 'php', 'swift', 'kotlin'
        ]
        
        # Enhanced skills detection patterns
        self.skill_patterns = {
            # Frontend Frameworks
            'frontend_frameworks': {
                'react': ['react', 'reactjs', 'react.js', 'react-native'],
                'vue': ['vue', 'vuejs', 'vue.js', 'nuxt'],
                'angular': ['angular', 'angularjs', 'angular.js'],
                'svelte': ['svelte', 'sveltekit'],
                'next': ['next.js', 'nextjs'],
                'gatsby': ['gatsby', 'gatsbyjs']
            },
            
            # Backend Frameworks
            'backend_frameworks': {
                'django': ['django', 'django-rest-framework'],
                'flask': ['flask', 'flask-restful'],
                'fastapi': ['fastapi', 'fast-api'],
                'express': ['express', 'expressjs', 'express.js'],
                'nestjs': ['nestjs', 'nest.js'],
                'spring': ['spring', 'spring-boot', 'springboot'],
                'rails': ['rails', 'ruby-on-rails', 'rubyonrails'],
                'laravel': ['laravel', 'lumen'],
                'asp.net': ['asp.net', 'aspnet', 'dotnet-core']
            },
            
            # Databases
            'databases': {
                'postgresql': ['postgresql', 'postgres', 'psql'],
                'mysql': ['mysql', 'mariadb'],
                'mongodb': ['mongodb', 'mongo', 'mongoose'],
                'redis': ['redis', 'redis-cache'],
                'elasticsearch': ['elasticsearch', 'elastic-search', 'elk'],
                'sqlite': ['sqlite', 'sqlite3'],
                'cassandra': ['cassandra', 'apache-cassandra'],
                'dynamodb': ['dynamodb', 'dynamo-db']
            },
            
            # Cloud & DevOps
            'cloud_devops': {
                'aws': ['aws', 'amazon-web-services', 'ec2', 's3', 'lambda', 'cloudformation'],
                'azure': ['azure', 'microsoft-azure'],
                'gcp': ['gcp', 'google-cloud', 'google-cloud-platform'],
                'docker': ['docker', 'dockerfile', 'docker-compose'],
                'kubernetes': ['kubernetes', 'k8s', 'kubectl'],
                'terraform': ['terraform', 'tf'],
                'jenkins': ['jenkins', 'ci-cd', 'continuous-integration'],
                'github-actions': ['github-actions', 'gh-actions'],
                'gitlab-ci': ['gitlab-ci', 'gitlab-cicd']
            },
            
            # Data Science & AI
            'data_ai': {
                'pandas': ['pandas', 'numpy', 'scipy'],
                'tensorflow': ['tensorflow', 'tf', 'keras'],
                'pytorch': ['pytorch', 'torch'],
                'scikit-learn': ['scikit-learn', 'sklearn', 'ml'],
                'jupyter': ['jupyter', 'notebook', 'ipynb'],
                'spark': ['spark', 'apache-spark', 'pyspark'],
                'tableau': ['tableau', 'data-visualization'],
                'power-bi': ['power-bi', 'powerbi']
            },
            
            # Mobile Development
            'mobile': {
                'react-native': ['react-native', 'rn'],
                'flutter': ['flutter', 'dart'],
                'ionic': ['ionic', 'cordova'],
                'xamarin': ['xamarin', 'xamarin-forms'],
                'android': ['android', 'kotlin-android'],
                'ios': ['ios', 'swift-ios', 'objective-c']
            },
            
            # Testing & Quality
            'testing': {
                'jest': ['jest', 'testing-library'],
                'cypress': ['cypress', 'e2e-testing'],
                'selenium': ['selenium', 'webdriver'],
                'pytest': ['pytest', 'python-testing'],
                'junit': ['junit', 'java-testing'],
                'mocha': ['mocha', 'chai']
            }
        }
        
        # Industry context keywords
        self.industry_keywords = {
            'fintech': ['fintech', 'blockchain', 'cryptocurrency', 'payment', 'banking', 'financial'],
            'healthcare': ['healthcare', 'medical', 'health', 'clinical', 'hospital', 'pharma'],
            'ecommerce': ['ecommerce', 'e-commerce', 'retail', 'shopping', 'marketplace'],
            'gaming': ['gaming', 'game', 'unity', 'unreal', 'gamedev'],
            'education': ['education', 'learning', 'student', 'course', 'academic'],
            'enterprise': ['enterprise', 'erp', 'crm', 'business', 'corporate'],
            'security': ['security', 'cybersecurity', 'infosec', 'encryption', 'auth'],
            'iot': ['iot', 'internet-of-things', 'embedded', 'sensors', 'hardware']
        }
        
        # Non-technical job titles and keywords
        self.non_technical_keywords = {
            'healthcare': ['nurse', 'doctor', 'therapist', 'medical', 'healthcare', 'physician', 'surgeon', 'pharmacist', 'dentist', 'veterinarian'],
            'education': ['teacher', 'professor', 'educator', 'instructor', 'principal', 'dean', 'tutor', 'academic', 'researcher', 'librarian'],
            'business': ['manager', 'consultant', 'analyst', 'coordinator', 'administrator', 'executive', 'director', 'supervisor', 'specialist'],
            'sales_marketing': ['sales', 'marketing', 'account manager', 'business development', 'customer success', 'brand manager', 'digital marketing'],
            'finance': ['accountant', 'financial', 'banker', 'auditor', 'bookkeeper', 'finance', 'investment', 'analyst', 'controller'],
            'creative': ['designer', 'writer', 'photographer', 'artist', 'journalist', 'editor', 'copywriter', 'creative director', 'illustrator'],
            'government': ['government', 'public sector', 'civil service', 'policy', 'public administration', 'municipal', 'federal', 'state'],
            'operations': ['operations', 'logistics', 'supply chain', 'project manager', 'program manager', 'quality assurance', 'compliance'],
            'hr_legal': ['human resources', 'hr', 'lawyer', 'attorney', 'legal', 'paralegal', 'recruiter', 'talent acquisition'],
            'customer_service': ['customer service', 'support', 'help desk', 'customer success', 'client relations', 'account coordinator']
        }
        
        # Non-technical organizations
        self.non_tech_organizations = {
            'education': ['university', 'college', 'school', 'institute', 'academy', 'education', '.edu'],
            'healthcare': ['hospital', 'clinic', 'medical center', 'health system', 'healthcare', 'medical', 'pharma'],
            'government': ['government', 'city of', 'state of', 'federal', 'department of', 'ministry', 'agency'],
            'nonprofit': ['foundation', 'charity', 'non-profit', 'ngo', 'organization', 'association', 'society'],
            'finance': ['bank', 'insurance', 'financial', 'credit union', 'investment', 'capital', 'fund'],
            'retail': ['retail', 'store', 'market', 'shop', 'mall', 'chain', 'brand'],
            'media': ['news', 'media', 'publishing', 'magazine', 'newspaper', 'broadcast', 'television'],
            'manufacturing': ['manufacturing', 'factory', 'industrial', 'production', 'automotive', 'aerospace']
        }
        
    def make_github_request(self, url: str) -> Optional[Dict]:
        """Make authenticated request to GitHub API"""
        try:
            response = requests.get(url, headers=self.headers)
            
            # Check rate limit
            remaining = int(response.headers.get('X-RateLimit-Remaining', 0))
            if remaining < 100:
                logger.warning(f"Rate limit getting low: {remaining} requests remaining")
            
            if response.status_code == 200:
                self.consecutive_errors = 0
                return response.json()
            elif response.status_code == 403:
                logger.error("Rate limit exceeded or token invalid")
                return None
            elif response.status_code == 404:
                logger.debug("Resource not found")
                return None
            else:
                logger.error(f"GitHub API error: {response.status_code}")
                self.consecutive_errors += 1
                return None
                
        except Exception as e:
            logger.error(f"Request failed: {e}")
            self.consecutive_errors += 1
            return None
    
    def respectful_delay(self):
        """Implement respectful delays between requests"""
        if self.consecutive_errors > 0:
            # Exponential backoff on errors
            delay = self.min_delay * (2 ** self.consecutive_errors)
            delay = min(delay, 10)  # Cap at 10 seconds for API
        else:
            delay = random.uniform(self.min_delay, self.max_delay)
        
        logger.debug(f"Waiting {delay:.2f} seconds...")
        time.sleep(delay)
    
    def check_limits(self):
        """Check if we've hit our rate limits"""
        if self.request_count >= self.daily_limit:
            logger.warning("Daily limit reached")
            return False
        
        if self.request_count >= self.session_limit:
            logger.warning("Session limit reached")
            return False
        
        if self.consecutive_errors >= self.max_consecutive_errors:
            logger.warning("Too many consecutive errors")
            return False
        
        return True
    
    def search_resume_repositories(self, query: str = "resume", per_page: int = 30) -> List[Dict]:
        """Search for repositories that might contain resumes"""
        repositories = []
        
        for keyword in self.resume_keywords:
            if not self.check_limits():
                break
                
            search_url = f"{GITHUB_API_BASE}/search/repositories?q={keyword}+in:name&per_page={per_page}&sort=updated"
            
            logger.info(f"Searching for repositories with keyword: {keyword}")
            self.respectful_delay()
            self.request_count += 1
            
            data = self.make_github_request(search_url)
            if data and 'items' in data:
                repositories.extend(data['items'])
                logger.info(f"Found {len(data['items'])} repositories for keyword: {keyword}")
            
            # Also search for profile README repositories (username/username)
            profile_search_url = f"{GITHUB_API_BASE}/search/repositories?q=filename:README.md+in:path&per_page={per_page}"
            
            self.respectful_delay()
            self.request_count += 1
            
            profile_data = self.make_github_request(profile_search_url)
            if profile_data and 'items' in profile_data:
                # Filter for profile READMEs (where repo name equals owner name)
                profile_repos = [repo for repo in profile_data['items'] 
                               if repo['name'] == repo['owner']['login']]
                repositories.extend(profile_repos)
                logger.info(f"Found {len(profile_repos)} profile README repositories")
        
        return repositories
    
    def get_user_profile(self, username: str) -> Optional[Dict]:
        """Get detailed user profile information"""
        if not self.check_limits():
            return None
            
        user_url = f"{GITHUB_API_BASE}/users/{username}"
        
        self.respectful_delay()
        self.request_count += 1
        
        return self.make_github_request(user_url)
    
    def get_repository_content(self, owner: str, repo: str, path: str = "README.md") -> Optional[str]:
        """Get content of a specific file in a repository"""
        if not self.check_limits():
            return None
            
        content_url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/contents/{path}"
        
        self.respectful_delay()
        self.request_count += 1
        
        data = self.make_github_request(content_url)
        if data and 'content' in data:
            try:
                # GitHub API returns base64 encoded content
                content = base64.b64decode(data['content']).decode('utf-8')
                return content
            except Exception as e:
                logger.error(f"Failed to decode content: {e}")
                return None
        
        return None
    
    def get_user_repositories(self, username: str) -> List[Dict]:
        """Get all public repositories for a user"""
        if not self.check_limits():
            return []
            
        repos_url = f"{GITHUB_API_BASE}/users/{username}/repos?per_page=100"
        
        self.respectful_delay()
        self.request_count += 1
        
        data = self.make_github_request(repos_url)
        return data if data else []
    
    def extract_github_resume_data(self, username: str, repository_data: Dict) -> Optional[Resume]:
        """Extract resume data from GitHub profile and repositories"""
        try:
            resume = Resume(username)
            
            # Get user profile
            user_profile = self.get_user_profile(username)
            if not user_profile:
                return None
            
            # Extract basic profile information
            resume.summary = user_profile.get('bio', '') or ''
            resume.location = user_profile.get('location', '') or ''
            
            # Get company information if available
            company = user_profile.get('company', '')
            if company:
                # Create a job entry for current company
                job = Job(
                    title="Developer",  # Default title
                    company=company,
                    location=resume.location,
                    hire_date="Present",
                    description="",
                    duration=""
                )
                resume.jobs.append(job)
            
            # Get user repositories to analyze skills
            repositories = self.get_user_repositories(username)
            if repositories:
                # Enhanced skills analysis
                enhanced_skills = self.analyze_enhanced_skills(repositories, username)
                resume.skills = enhanced_skills['skills_list']
                resume.skill_details = enhanced_skills['skill_details']
                resume.technology_stack = enhanced_skills['tech_stack']
                resume.industry_context = enhanced_skills['industry_context']
                resume.skill_proficiency = enhanced_skills['proficiency_level']
            
            # Try to get resume/CV content from repositories
            resume_content = None
            
            # First, try to get content from resume repository
            if repository_data:
                resume_content = self.get_repository_content(
                    repository_data['owner']['login'], 
                    repository_data['name']
                )
            
            # If no resume repo, try profile README
            if not resume_content:
                resume_content = self.get_repository_content(username, username)
            
            if resume_content:
                # Parse resume content for additional information
                parsed_data = self.parse_resume_content(resume_content)
                
                # Update resume with parsed data
                if parsed_data.get('summary'):
                    resume.summary = parsed_data['summary']
                
                if parsed_data.get('jobs'):
                    resume.jobs.extend(parsed_data['jobs'])
                
                if parsed_data.get('schools'):
                    resume.schools = parsed_data['schools']
                
                if parsed_data.get('skills'):
                    # Merge skills, keeping unique ones
                    all_skills = set(resume.skills + parsed_data['skills'])
                    resume.skills = list(all_skills)[:15]  # Limit to 15 skills
            
            # Determine experience level based on GitHub activity
            account_age_years = self.calculate_account_age(user_profile.get('created_at', ''))
            public_repos = user_profile.get('public_repos', 0)
            
            if account_age_years < 2 or public_repos < 5:
                resume.experience_level = "entry"
            elif account_age_years < 5 or public_repos < 20:
                resume.experience_level = "mid"
            elif account_age_years < 10 or public_repos < 50:
                resume.experience_level = "senior"
            else:
                resume.experience_level = "executive"
            
            self.consecutive_errors = 0
            return resume
            
        except Exception as e:
            logger.error(f"Error extracting GitHub resume for {username}: {e}")
            self.consecutive_errors += 1
            return None
    
    def parse_resume_content(self, content: str) -> Dict:
        """Parse resume content from README or other text files"""
        parsed_data = {
            'summary': '',
            'jobs': [],
            'schools': [],
            'skills': []
        }
        
        try:
            # Simple regex patterns for common resume sections
            content_lower = content.lower()
            
            # Extract summary/about section
            summary_patterns = [
                r'(?:about|summary|profile|bio)(?:\s*:?\s*\n)(.*?)(?:\n\s*\n|\n#+|$)',
                r'(?:## about|## summary|## profile)(.*?)(?:\n#+|$)'
            ]
            
            for pattern in summary_patterns:
                match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
                if match:
                    parsed_data['summary'] = match.group(1).strip()[:500]  # Limit length
                    break
            
            # Extract skills
            skills_patterns = [
                r'(?:skills?|technologies?|languages?)(?:\s*:?\s*\n)(.*?)(?:\n\s*\n|\n#+|$)',
                r'(?:## skills|## technologies|## languages)(.*?)(?:\n#+|$)'
            ]
            
            for pattern in skills_patterns:
                match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
                if match:
                    skills_text = match.group(1)
                    # Extract individual skills (simple approach)
                    skills = re.findall(r'\b[A-Za-z+#]{2,}\b', skills_text)
                    parsed_data['skills'] = skills[:10]  # Limit to 10 skills
                    break
            
            # Extract education (basic)
            education_patterns = [
                r'(?:education|university|college|degree)(?:\s*:?\s*\n)(.*?)(?:\n\s*\n|\n#+|$)',
                r'(?:## education|## university)(.*?)(?:\n#+|$)'
            ]
            
            for pattern in education_patterns:
                match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
                if match:
                    edu_text = match.group(1).strip()
                    # Create a basic education entry
                    school = School(
                        degree="",
                        school_name=edu_text[:100],  # Use first part as school name
                        grad_date="",
                        field_of_study=""
                    )
                    parsed_data['schools'] = [school]
                    break
            
        except Exception as e:
            logger.error(f"Error parsing resume content: {e}")
        
        return parsed_data
    
    def calculate_account_age(self, created_at: str) -> int:
        """Calculate GitHub account age in years"""
        try:
            if not created_at:
                return 0
            
            from datetime import datetime
            created_date = datetime.strptime(created_at, '%Y-%m-%dT%H:%M:%SZ')
            age_years = (datetime.now() - created_date).days / 365.25
            return int(age_years)
        except:
            return 0
    
    def search_popular_developers(self, per_page: int = 100) -> List[Dict]:
        """Search for popular developers with many repositories"""
        repositories = []
        
        # Search for users with many repositories in different programming languages
        for language in self.tech_languages:
            if not self.check_limits():
                break
                
            # Search for repositories in specific language with many stars
            search_url = f"{GITHUB_API_BASE}/search/repositories?q=language:{language}&sort=stars&order=desc&per_page={per_page}"
            
            logger.info(f"Searching for popular {language} developers...")
            self.respectful_delay()
            self.request_count += 1
            
            data = self.make_github_request(search_url)
            if data and 'items' in data:
                # Filter for repositories with active developers
                lang_repos = [repo for repo in data['items'] 
                            if repo.get('stargazers_count', 0) > 50 and 
                            repo.get('owner', {}).get('type') == 'User']
                repositories.extend(lang_repos)
                logger.info(f"Found {len(lang_repos)} popular {language} repositories")
        
        # Also search for users with many followers
        if not self.check_limits():
            search_url = f"{GITHUB_API_BASE}/search/users?q=followers:>100&sort=followers&order=desc&per_page={per_page}"
            
            logger.info("Searching for developers with many followers...")
            self.respectful_delay()
            self.request_count += 1
            
            data = self.make_github_request(search_url)
            if data and 'items' in data:
                # For each user, get their most popular repository
                for user in data['items'][:50]:  # Limit to top 50 users
                    if not self.check_limits():
                        break
                    
                    user_repos = self.get_user_repositories(user['login'])
                    if user_repos:
                        # Get the most starred repository
                        most_starred = max(user_repos, key=lambda x: x.get('stargazers_count', 0))
                        repositories.append(most_starred)
        
        return repositories
    
    def search_non_technical_profiles(self, per_page: int = 100) -> List[Dict]:
        """Search for non-technical professionals by bio keywords"""
        profiles = []
        
        for category, keywords in self.non_technical_keywords.items():
            if not self.check_limits():
                break
                
            for keyword in keywords[:3]:  # Limit to top 3 keywords per category
                if not self.check_limits():
                    break
                    
                # Search for users with specific job titles in their bio
                search_url = f"{GITHUB_API_BASE}/search/users?q={keyword}+in:bio&per_page={per_page}"
                
                logger.info(f"Searching for {category} professionals with keyword: {keyword}")
                self.respectful_delay()
                self.request_count += 1
                
                data = self.make_github_request(search_url)
                if data and 'items' in data:
                    # Filter for users with complete profiles
                    filtered_users = []
                    for user in data['items']:
                        # Get detailed profile to check for completeness
                        user_profile = self.get_user_profile(user['login'])
                        if user_profile and self.is_non_technical_profile(user_profile):
                            # Create a mock repository entry for compatibility
                            mock_repo = {
                                'owner': {'login': user['login']},
                                'name': user['login'],  # Profile README
                                'description': user_profile.get('bio', ''),
                                'category': category
                            }
                            filtered_users.append(mock_repo)
                    
                    profiles.extend(filtered_users)
                    logger.info(f"Found {len(filtered_users)} {category} professionals with keyword: {keyword}")
        
        return profiles
    
    def search_organization_based_profiles(self, per_page: int = 100) -> List[Dict]:
        """Search for professionals working at non-technical organizations"""
        profiles = []
        
        for category, org_keywords in self.non_tech_organizations.items():
            if not self.check_limits():
                break
                
            for org_keyword in org_keywords[:2]:  # Limit to top 2 keywords per category
                if not self.check_limits():
                    break
                    
                # Search for users with specific organizations in their company field
                search_url = f"{GITHUB_API_BASE}/search/users?q={org_keyword}+in:company&per_page={per_page}"
                
                logger.info(f"Searching for professionals at {category} organizations: {org_keyword}")
                self.respectful_delay()
                self.request_count += 1
                
                data = self.make_github_request(search_url)
                if data and 'items' in data:
                    # Filter for users with complete profiles
                    filtered_users = []
                    for user in data['items']:
                        # Get detailed profile to check for completeness
                        user_profile = self.get_user_profile(user['login'])
                        if user_profile and self.is_complete_profile(user_profile):
                            # Create a mock repository entry for compatibility
                            mock_repo = {
                                'owner': {'login': user['login']},
                                'name': user['login'],  # Profile README
                                'description': user_profile.get('company', ''),
                                'category': category
                            }
                            filtered_users.append(mock_repo)
                    
                    profiles.extend(filtered_users)
                    logger.info(f"Found {len(filtered_users)} professionals at {category} organizations")
        
        return profiles
    
    def search_non_technical_repositories(self, per_page: int = 100) -> List[Dict]:
        """Search for repositories with non-technical content"""
        repositories = []
        
        # Search for repositories with non-technical file types
        non_tech_searches = [
            "filename:resume.pdf",
            "filename:cv.pdf", 
            "filename:portfolio.pdf",
            "extension:docx resume",
            "extension:pptx presentation",
            "curriculum vitae filetype:pdf",
            "lesson plan filetype:pdf",
            "business plan filetype:pdf",
            "research paper filetype:pdf"
        ]
        
        for search_term in non_tech_searches:
            if not self.check_limits():
                break
                
            search_url = f"{GITHUB_API_BASE}/search/repositories?q={search_term}&per_page={per_page}"
            
            logger.info(f"Searching for repositories with: {search_term}")
            self.respectful_delay()
            self.request_count += 1
            
            data = self.make_github_request(search_url)
            if data and 'items' in data:
                # Filter for repositories from individual users (not organizations)
                user_repos = [repo for repo in data['items'] 
                            if repo.get('owner', {}).get('type') == 'User']
                repositories.extend(user_repos)
                logger.info(f"Found {len(user_repos)} repositories with {search_term}")
        
        return repositories
    
    def is_non_technical_profile(self, profile: Dict) -> bool:
        """Check if a profile appears to be non-technical"""
        bio = profile.get('bio', '').lower() if profile.get('bio') else ''
        company = profile.get('company', '').lower() if profile.get('company') else ''
        
        # Check for non-technical keywords in bio
        for category, keywords in self.non_technical_keywords.items():
            for keyword in keywords:
                if keyword.lower() in bio:
                    return True
        
        # Check for non-technical organizations
        for category, org_keywords in self.non_tech_organizations.items():
            for org_keyword in org_keywords:
                if org_keyword.lower() in company:
                    return True
        
        # Check repository count - non-technical users typically have fewer repos
        public_repos = profile.get('public_repos', 0)
        if public_repos <= 10:  # Likely non-technical if very few repos
            return True
        
        return False
    
    def is_complete_profile(self, profile: Dict) -> bool:
        """Check if a profile is complete enough for resume extraction"""
        required_fields = ['bio', 'location', 'company']
        filled_fields = sum(1 for field in required_fields if profile.get(field))
        
        # At least 2 out of 3 fields should be filled
        return filled_fields >= 2
    
    def analyze_enhanced_skills(self, repositories: List[Dict], username: str) -> Dict:
        """Enhanced skills analysis from repositories"""
        analysis = {
            'skills_list': [],
            'skill_details': {},
            'tech_stack': {},
            'industry_context': [],
            'proficiency_level': 'beginner'
        }
        
        try:
            # Basic language analysis
            languages = {}
            frameworks = {}
            tools = {}
            total_repos = len(repositories)
            total_stars = 0
            
            for repo in repositories:
                # Language analysis
                if repo.get('language'):
                    lang = repo['language'].lower()
                    languages[lang] = languages.get(lang, 0) + 1
                
                # Stars for proficiency calculation
                total_stars += repo.get('stargazers_count', 0)
                
                # Repository name and description analysis
                repo_text = f"{repo.get('name', '')} {repo.get('description', '')}".lower()
                
                # Framework detection
                for category, frameworks_dict in self.skill_patterns.items():
                    for framework, patterns in frameworks_dict.items():
                        for pattern in patterns:
                            if pattern in repo_text:
                                if category not in frameworks:
                                    frameworks[category] = {}
                                frameworks[category][framework] = frameworks[category].get(framework, 0) + 1
                
                # Industry context detection
                for industry, keywords in self.industry_keywords.items():
                    for keyword in keywords:
                        if keyword in repo_text:
                            if industry not in analysis['industry_context']:
                                analysis['industry_context'].append(industry)
            
            # Calculate proficiency level
            analysis['proficiency_level'] = self.calculate_proficiency_level(
                total_repos, total_stars, languages
            )
            
            # Build skills list (top languages + frameworks)
            top_languages = sorted(languages.items(), key=lambda x: x[1], reverse=True)[:8]
            analysis['skills_list'] = [lang.title() for lang, count in top_languages]
            
            # Add framework skills
            for category, framework_dict in frameworks.items():
                top_frameworks = sorted(framework_dict.items(), key=lambda x: x[1], reverse=True)[:3]
                for framework, count in top_frameworks:
                    if framework.title() not in analysis['skills_list']:
                        analysis['skills_list'].append(framework.title())
            
            # Limit skills list to top 15
            analysis['skills_list'] = analysis['skills_list'][:15]
            
            # Build detailed skill information
            for lang, count in languages.items():
                analysis['skill_details'][lang] = {
                    'repositories': count,
                    'percentage': round((count / total_repos) * 100, 1) if total_repos > 0 else 0,
                    'category': 'programming_language'
                }
            
            for category, framework_dict in frameworks.items():
                for framework, count in framework_dict.items():
                    analysis['skill_details'][framework] = {
                        'repositories': count,
                        'percentage': round((count / total_repos) * 100, 1) if total_repos > 0 else 0,
                        'category': category
                    }
            
            # Build technology stack combinations
            analysis['tech_stack'] = self.identify_tech_stacks(frameworks, languages)
            
            # Limit industry context to top 3
            analysis['industry_context'] = analysis['industry_context'][:3]
            
        except Exception as e:
            logger.error(f"Error in enhanced skills analysis for {username}: {e}")
            # Fallback to basic analysis
            if repositories:
                basic_languages = {}
                for repo in repositories:
                    if repo.get('language'):
                        lang = repo['language'].lower()
                        basic_languages[lang] = basic_languages.get(lang, 0) + 1
                
                analysis['skills_list'] = [lang.title() for lang, count in 
                                         sorted(basic_languages.items(), key=lambda x: x[1], reverse=True)[:10]]
        
        return analysis
    
    def calculate_proficiency_level(self, total_repos: int, total_stars: int, languages: Dict) -> str:
        """Calculate skill proficiency level based on repository metrics"""
        try:
            # Scoring factors
            repo_score = min(total_repos / 20, 1.0)  # 20+ repos = max score
            star_score = min(total_stars / 100, 1.0)  # 100+ stars = max score
            diversity_score = min(len(languages) / 5, 1.0)  # 5+ languages = max score
            
            # Weighted average
            overall_score = (repo_score * 0.4) + (star_score * 0.3) + (diversity_score * 0.3)
            
            if overall_score >= 0.8:
                return 'expert'
            elif overall_score >= 0.6:
                return 'advanced'
            elif overall_score >= 0.4:
                return 'intermediate'
            elif overall_score >= 0.2:
                return 'beginner'
            else:
                return 'novice'
                
        except Exception:
            return 'beginner'
    
    def identify_tech_stacks(self, frameworks: Dict, languages: Dict) -> Dict:
        """Identify common technology stack combinations"""
        stacks = {}
        
        try:
            # Common stack patterns
            stack_patterns = {
                'MEAN': ['mongodb', 'express', 'angular', 'nodejs'],
                'MERN': ['mongodb', 'express', 'react', 'nodejs'],
                'LAMP': ['linux', 'apache', 'mysql', 'php'],
                'Django_Stack': ['django', 'postgresql', 'redis'],
                'Rails_Stack': ['rails', 'postgresql', 'redis'],
                'Spring_Stack': ['spring', 'mysql', 'java'],
                'React_Stack': ['react', 'nodejs', 'express'],
                'Vue_Stack': ['vue', 'nodejs', 'express'],
                'Python_Data': ['pandas', 'jupyter', 'scikit-learn'],
                'AWS_Stack': ['aws', 'docker', 'kubernetes'],
                'Full_Stack_JS': ['react', 'nodejs', 'mongodb'],
                'Enterprise_Java': ['spring', 'mysql', 'jenkins']
            }
            
            # Check for stack matches
            all_skills = set()
            for category in frameworks.values():
                all_skills.update(category.keys())
            all_skills.update(languages.keys())
            
            for stack_name, required_skills in stack_patterns.items():
                matched_skills = [skill for skill in required_skills if skill in all_skills]
                if len(matched_skills) >= 2:  # At least 2 skills from the stack
                    stacks[stack_name] = {
                        'matched_skills': matched_skills,
                        'completeness': len(matched_skills) / len(required_skills)
                    }
            
            # Sort by completeness
            stacks = dict(sorted(stacks.items(), key=lambda x: x[1]['completeness'], reverse=True))
            
        except Exception as e:
            logger.error(f"Error identifying tech stacks: {e}")
        
        return stacks
    
    def search_users_by_bio(self, keyword: str, max_results: int = 50) -> List[Dict]:
        """Search for users by bio keyword"""
        if not self.check_limits():
            return []
            
        search_url = f"{GITHUB_API_BASE}/search/users?q={keyword}+in:bio&per_page={min(max_results, 100)}"
        
        self.respectful_delay()
        self.request_count += 1
        
        data = self.make_github_request(search_url)
        if data and 'items' in data:
            return data['items'][:max_results]
        return []
    
    def collect_user_resume(self, user: Dict) -> Optional[Dict]:
        """Collect resume data from a GitHub user"""
        try:
            username = user['login']
            
            # Get user profile
            user_profile = self.get_user_profile(username)
            if not user_profile:
                return None
            
            # Get user repositories
            repositories = self.get_user_repositories(username)
            
            # Enhanced skills analysis
            enhanced_skills = self.analyze_enhanced_skills(repositories, username)
            
            # Create resume data structure
            resume_data = {
                'id': username,
                'name': user_profile.get('name', username),
                'bio': user_profile.get('bio', ''),
                'location': user_profile.get('location', ''),
                'company': user_profile.get('company', ''),
                'email': user_profile.get('email', ''),
                'blog': user_profile.get('blog', ''),
                'twitter_username': user_profile.get('twitter_username', ''),
                'public_repos': user_profile.get('public_repos', 0),
                'followers': user_profile.get('followers', 0),
                'following': user_profile.get('following', 0),
                'created_at': user_profile.get('created_at', ''),
                'updated_at': user_profile.get('updated_at', ''),
                'skills': enhanced_skills['skills_list'],
                'skill_details': enhanced_skills['skill_details'],
                'technology_stack': enhanced_skills['tech_stack'],
                'industry_context': enhanced_skills['industry_context'],
                'skill_proficiency': enhanced_skills['proficiency_level'],
                'github_stats': {
                    'total_repos': len(repositories),
                    'total_stars': sum(repo.get('stargazers_count', 0) for repo in repositories),
                    'languages': {}
                }
            }
            
            # Add language statistics
            for repo in repositories:
                if repo.get('language'):
                    lang = repo['language']
                    resume_data['github_stats']['languages'][lang] = \
                        resume_data['github_stats']['languages'].get(lang, 0) + 1
            
            return resume_data
            
        except Exception as e:
            logger.error(f"Error collecting resume for {user.get('login', 'unknown')}: {e}")
            return None
    
    def collect_resumes(self, target_count=50):
        """Collect resumes using multi-stage strategy with optimized rate limiting"""
        all_resumes = []
        
        # Start with a smaller batch to test and show progress
        initial_batch = min(target_count, 50)
        
        # Stage 1: Non-technical professionals (40% of initial batch)
        non_tech_target = int(initial_batch * 0.4)
        logger.info("="*60)
        logger.info(f"STAGE 1: Searching for Non-Technical Professionals (Target: {non_tech_target})")
        logger.info("="*60)
        
        # Search by job titles in user bios - reduced keywords for faster execution
        logger.info("Searching by job titles in user bios...")
        non_tech_keywords = {
            'healthcare': ['nurse', 'doctor'],
            'business': ['manager', 'analyst']
        }
        
        for category, keywords in non_tech_keywords.items():
            if len(all_resumes) >= non_tech_target:
                break
            for keyword in keywords:
                if len(all_resumes) >= non_tech_target:
                    break
                logger.info(f"Searching for {category} professionals with keyword: {keyword}")
                users = self.search_users_by_bio(keyword, max_results=8)  # Reduced for faster execution
                for user in users:
                    if len(all_resumes) >= non_tech_target:
                        break
                    resume_data = self.collect_user_resume(user)
                    if resume_data:
                        all_resumes.append(resume_data)
                        logger.info(f"Collected resume {len(all_resumes)}/{initial_batch}: {resume_data['name']}")
        
        # Stage 2: Semi-technical professionals (30% of initial batch)
        semi_tech_target = int(initial_batch * 0.3)
        current_target = non_tech_target + semi_tech_target
        logger.info("="*60)
        logger.info(f"STAGE 2: Searching for Semi-Technical Professionals (Target: {current_target})")
        logger.info("="*60)
        
        semi_tech_keywords = ['data analyst', 'product manager']
        
        for keyword in semi_tech_keywords:
            if len(all_resumes) >= current_target:
                break
            logger.info(f"Searching for semi-technical professionals: {keyword}")
            users = self.search_users_by_bio(keyword, max_results=10)
            for user in users:
                if len(all_resumes) >= current_target:
                    break
                resume_data = self.collect_user_resume(user)
                if resume_data:
                    all_resumes.append(resume_data)
                    logger.info(f"Collected resume {len(all_resumes)}/{initial_batch}: {resume_data['name']}")
        
        # Stage 3: Technical professionals (fill remaining)
        logger.info("="*60)
        logger.info(f"STAGE 3: Searching for Technical Professionals (Target: {initial_batch})")
        logger.info("="*60)
        
        tech_keywords = ['software engineer', 'developer']
        
        for keyword in tech_keywords:
            if len(all_resumes) >= initial_batch:
                break
            logger.info(f"Searching for technical professionals: {keyword}")
            users = self.search_users_by_bio(keyword, max_results=15)
            for user in users:
                if len(all_resumes) >= initial_batch:
                    break
                resume_data = self.collect_user_resume(user)
                if resume_data:
                    all_resumes.append(resume_data)
                    logger.info(f"Collected resume {len(all_resumes)}/{initial_batch}: {resume_data['name']}")
        
        return all_resumes

# Sampling Strategy Configuration
SAMPLING_STRATEGY = {
    "total_target": 1000,
    "pilot_size": 50,
    "regions": {
        "northeast": {
            "target": 170,
            "cities": ["New York", "Boston", "Philadelphia", "Pittsburgh", "Buffalo"]
        },
        "midwest": {
            "target": 210,
            "cities": ["Chicago", "Detroit", "Cleveland", "Indianapolis", "Milwaukee"]
        },
        "south": {
            "target": 380,
            "cities": ["Atlanta", "Houston", "Dallas", "Miami", "Charlotte", "Nashville", "Austin", "Tampa"]
        },
        "west": {
            "target": 240,
            "cities": ["Los Angeles", "San Francisco", "Seattle", "Denver", "Phoenix"]
        }
    },
    "job_categories": {
        "professional_technical": {"target": 300, "keywords": ["software engineer", "data analyst", "consultant", "designer"]},
        "management_business": {"target": 150, "keywords": ["manager", "director", "executive", "business analyst"]},
        "sales_customer_service": {"target": 120, "keywords": ["sales", "customer service", "account manager", "representative"]},
        "healthcare": {"target": 100, "keywords": ["nurse", "doctor", "therapist", "medical assistant"]},
        "education": {"target": 80, "keywords": ["teacher", "professor", "instructor", "principal"]},
        "engineering_it": {"target": 80, "keywords": ["engineer", "developer", "programmer", "systems administrator"]},
        "finance": {"target": 60, "keywords": ["accountant", "financial analyst", "banker", "auditor"]},
        "administrative": {"target": 50, "keywords": ["administrative assistant", "secretary", "coordinator", "clerk"]},
        "manufacturing_operations": {"target": 40, "keywords": ["operator", "technician", "supervisor", "manufacturing"]},
        "other": {"target": 20, "keywords": ["specialist", "coordinator", "associate", "assistant"]}
    }
}

def save_resume_data(resume, output_dir):
    """Save resume data to JSON file"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    filename = f"resume_{resume.id}.json"
    filepath = os.path.join(output_dir, filename)
    
    resume_data = {
        "id": resume.id,
        "summary": resume.summary,
        "location": resume.location,
        "experience_level": resume.experience_level,
        "jobs": [
            {
                "title": job.title,
                "company": job.company,
                "location": job.location,
                "hire_date": job.hire_date,
                "description": job.description,
                "duration": job.duration
            } for job in resume.jobs
        ],
        "schools": [
            {
                "degree": school.degree,
                "school_name": school.school_name,
                "grad_date": school.grad_date,
                "field_of_study": school.field_of_study
            } for school in resume.schools
        ],
        "skills": resume.skills
    }
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(resume_data, f, indent=2, ensure_ascii=False)
    
    logger.info(f"Saved resume data to {filepath}")

def test_indeed_response():
    """Test Indeed's response to respectful scraping approach"""
    scraper = RespectfulScraper()
    driver = scraper.setup_driver()
    
    test_results = {
        "timestamp": datetime.now().isoformat(),
        "tests": [],
        "summary": {}
    }
    
    try:
        # Test 1: Basic Indeed homepage access
        logger.info("Test 1: Accessing Indeed homepage")
        scraper.respectful_delay()
        scraper.request_count += 1
        
        start_time = time.time()
        driver.get("https://indeed.com")
        load_time = time.time() - start_time
        
        page_title = driver.title
        current_url = driver.current_url
        page_source_length = len(driver.page_source)
        
        # Check for common anti-bot indicators
        anti_bot_indicators = {
            "captcha": "captcha" in driver.page_source.lower(),
            "blocked": "blocked" in driver.page_source.lower() or "access denied" in driver.page_source.lower(),
            "security_check": "security check" in driver.page_source.lower(),
            "unusual_traffic": "unusual traffic" in driver.page_source.lower(),
            "robot_detected": "robot" in driver.page_source.lower()
        }
        
        test_results["tests"].append({
            "test": "homepage_access",
            "url": "https://indeed.com",
            "status": "success" if page_title else "failed",
            "load_time": load_time,
            "page_title": page_title,
            "current_url": current_url,
            "page_size": page_source_length,
            "anti_bot_indicators": anti_bot_indicators
        })
        
        logger.info(f"Homepage loaded: {page_title}")
        logger.info(f"Load time: {load_time:.2f}s")
        logger.info(f"Anti-bot indicators: {anti_bot_indicators}")
        
        # Test 2: Resume search page access
        if scraper.check_limits():
            logger.info("Test 2: Accessing resume search page")
            scraper.respectful_delay()
            scraper.request_count += 1
            
            start_time = time.time()
            search_url = "https://resumes.indeed.com/search?q=software+engineer&l=New+York"
            driver.get(search_url)
            load_time = time.time() - start_time
            
            page_title = driver.title
            current_url = driver.current_url
            page_source_length = len(driver.page_source)
            
            # Check for search results or blocking
            search_indicators = {
                "search_results": "resume" in driver.page_source.lower(),
                "no_results": "no results" in driver.page_source.lower() or "0 results" in driver.page_source.lower(),
                "login_required": "sign in" in driver.page_source.lower() or "login" in driver.page_source.lower(),
                "access_restricted": "restricted" in driver.page_source.lower() or "premium" in driver.page_source.lower()
            }
            
            anti_bot_indicators = {
                "captcha": "captcha" in driver.page_source.lower(),
                "blocked": "blocked" in driver.page_source.lower() or "access denied" in driver.page_source.lower(),
                "security_check": "security check" in driver.page_source.lower(),
                "unusual_traffic": "unusual traffic" in driver.page_source.lower(),
                "robot_detected": "robot" in driver.page_source.lower()
            }
            
            test_results["tests"].append({
                "test": "resume_search",
                "url": search_url,
                "status": "success" if page_title else "failed",
                "load_time": load_time,
                "page_title": page_title,
                "current_url": current_url,
                "page_size": page_source_length,
                "search_indicators": search_indicators,
                "anti_bot_indicators": anti_bot_indicators
            })
            
            logger.info(f"Search page loaded: {page_title}")
            logger.info(f"Load time: {load_time:.2f}s")
            logger.info(f"Search indicators: {search_indicators}")
            logger.info(f"Anti-bot indicators: {anti_bot_indicators}")
        
        # Test 3: Job search page (for comparison)
        if scraper.check_limits():
            logger.info("Test 3: Accessing job search page for comparison")
            scraper.respectful_delay()
            scraper.request_count += 1
            
            start_time = time.time()
            job_search_url = "https://indeed.com/jobs?q=software+engineer&l=New+York"
            driver.get(job_search_url)
            load_time = time.time() - start_time
            
            page_title = driver.title
            current_url = driver.current_url
            page_source_length = len(driver.page_source)
            
            # Check for job results
            job_indicators = {
                "job_results": "job" in driver.page_source.lower() and "title" in driver.page_source.lower(),
                "no_results": "no jobs" in driver.page_source.lower() or "0 jobs" in driver.page_source.lower(),
                "sponsored_jobs": "sponsored" in driver.page_source.lower()
            }
            
            test_results["tests"].append({
                "test": "job_search",
                "url": job_search_url,
                "status": "success" if page_title else "failed",
                "load_time": load_time,
                "page_title": page_title,
                "current_url": current_url,
                "page_size": page_source_length,
                "job_indicators": job_indicators
            })
            
            logger.info(f"Job search page loaded: {page_title}")
            logger.info(f"Load time: {load_time:.2f}s")
            logger.info(f"Job indicators: {job_indicators}")
        
        # Generate summary
        test_results["summary"] = {
            "total_tests": len(test_results["tests"]),
            "successful_tests": len([t for t in test_results["tests"] if t["status"] == "success"]),
            "total_requests": scraper.request_count,
            "any_anti_bot_detected": any(any(test.get("anti_bot_indicators", {}).values()) for test in test_results["tests"]),
            "resume_search_accessible": any(t["test"] == "resume_search" and t["status"] == "success" for t in test_results["tests"])
        }
        
        logger.info(f"Test Summary: {test_results['summary']}")
        
        # Save results
        with open(f"indeed_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", 'w') as f:
            json.dump(test_results, f, indent=2)
        
        return test_results
        
    except Exception as e:
        logger.error(f"Test failed: {e}")
        test_results["error"] = str(e)
        return test_results
    finally:
        driver.quit()

def run_github_collection(target_count=5000):
    """Run multi-stage GitHub resume collection prioritizing non-technical professionals"""
    collector = GitHubResumeCollector()
    
    output_dir = f"github_collection_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    collected_resumes = []
    
    # Multi-stage collection targets
    stage_targets = {
        'non_technical': 2000,    # Stage 1: Non-technical professionals
        'semi_technical': 1000,   # Stage 2: Semi-technical roles
        'technical': 2000         # Stage 3: Technical professionals
    }
    
    try:
        all_repositories = []
        
        # STAGE 1: Non-Technical Professionals (Target: 2000)
        logger.info("="*60)
        logger.info("STAGE 1: Searching for Non-Technical Professionals")
        logger.info("="*60)
        
        # Strategy 1A: Bio-based search
        logger.info("Searching by job titles in user bios...")
        bio_profiles = collector.search_non_technical_profiles()
        all_repositories.extend(bio_profiles)
        logger.info(f"Found {len(bio_profiles)} non-technical profiles from bio search")
        
        # Strategy 1B: Organization-based search
        logger.info("Searching by non-technical organizations...")
        org_profiles = collector.search_organization_based_profiles()
        all_repositories.extend(org_profiles)
        logger.info(f"Found {len(org_profiles)} professionals from non-tech organizations")
        
        # Strategy 1C: Repository content search
        logger.info("Searching for non-technical repository content...")
        non_tech_repos = collector.search_non_technical_repositories()
        all_repositories.extend(non_tech_repos)
        logger.info(f"Found {len(non_tech_repos)} repositories with non-technical content")
        
        stage1_total = len(bio_profiles) + len(org_profiles) + len(non_tech_repos)
        logger.info(f"Stage 1 Total: {stage1_total} non-technical candidates found")
        
        # STAGE 2: Semi-Technical Professionals (Target: 1000)
        if len(all_repositories) < stage_targets['non_technical'] + stage_targets['semi_technical']:
            logger.info("="*60)
            logger.info("STAGE 2: Searching for Semi-Technical Professionals")
            logger.info("="*60)
            
            # Search for technical adjacent roles
            semi_tech_keywords = [
                "product manager", "ux designer", "data analyst", "business analyst",
                "technical writer", "sales engineer", "project manager", "scrum master"
            ]
            
            for keyword in semi_tech_keywords:
                if not collector.check_limits():
                    break
                    
                search_url = f"{GITHUB_API_BASE}/search/users?q={keyword}+in:bio&per_page=100"
                logger.info(f"Searching for semi-technical professionals: {keyword}")
                
                collector.respectful_delay()
                collector.request_count += 1
                
                data = collector.make_github_request(search_url)
                if data and 'items' in data:
                    for user in data['items']:
                        user_profile = collector.get_user_profile(user['login'])
                        if user_profile and collector.is_complete_profile(user_profile):
                            mock_repo = {
                                'owner': {'login': user['login']},
                                'name': user['login'],
                                'description': user_profile.get('bio', ''),
                                'category': 'semi_technical'
                            }
                            all_repositories.append(mock_repo)
            
            logger.info(f"Stage 2 added semi-technical professionals")
        
        # STAGE 3: Technical Professionals (Target: 2000)
        if len(all_repositories) < target_count:
            logger.info("="*60)
            logger.info("STAGE 3: Searching for Technical Professionals")
            logger.info("="*60)
            
            # Strategy 3A: Resume repositories
            logger.info("Searching for technical resume repositories...")
            resume_repos = collector.search_resume_repositories()
            all_repositories.extend(resume_repos)
            logger.info(f"Found {len(resume_repos)} technical resume repositories")
            
            # Strategy 3B: Popular developers
            if len(all_repositories) < target_count:
                logger.info("Searching for popular technical developers...")
                popular_devs = collector.search_popular_developers()
                all_repositories.extend(popular_devs)
                logger.info(f"Found {len(popular_devs)} popular developer repositories")
        
        # Remove duplicates
        seen_users = set()
        unique_repositories = []
        for repo in all_repositories:
            username = repo['owner']['login']
            if username not in seen_users:
                seen_users.add(username)
                unique_repositories.append(repo)
        
        logger.info(f"="*60)
        logger.info(f"COLLECTION PHASE: Processing {len(unique_repositories)} unique candidates")
        logger.info(f"="*60)
        
        # Process repositories and extract resume data
        processed_users = set()
        stage_counts = {'non_technical': 0, 'semi_technical': 0, 'technical': 0}
        
        for i, repo in enumerate(unique_repositories):
            if not collector.check_limits():
                logger.warning("Rate limit reached, stopping collection")
                break
            
            username = repo['owner']['login']
            
            # Skip if we've already processed this user
            if username in processed_users:
                continue
            
            processed_users.add(username)
            
            logger.info(f"Processing resume {len(collected_resumes)+1}/{target_count} for user: {username}")
            
            # Extract resume data
            resume = collector.extract_github_resume_data(username, repo)
            
            if resume:
                # Add category information to resume
                category = repo.get('category', 'technical')
                resume.category = category
                stage_counts[category] = stage_counts.get(category, 0) + 1
                
                collected_resumes.append(resume)
                
                # Save individual resume
                save_resume_data(resume, output_dir)
                
                logger.info(f"Successfully collected {category} resume for {username}")
                
                # Check if we've reached our target
                if len(collected_resumes) >= target_count:
                    logger.info(f"Reached collection target of {target_count} resumes")
                    break
                    
                # Progress updates
                if len(collected_resumes) % 100 == 0:
                    logger.info(f"Progress: {len(collected_resumes)}/{target_count} resumes collected")
                    logger.info(f"  Non-technical: {stage_counts.get('non_technical', 0)}")
                    logger.info(f"  Semi-technical: {stage_counts.get('semi_technical', 0)}")
                    logger.info(f"  Technical: {stage_counts.get('technical', 0)}")
            else:
                logger.debug(f"Failed to extract resume data for {username}")
        
        logger.info(f"Collection completed. Collected {len(collected_resumes)} resumes.")
        logger.info(f"Final breakdown:")
        logger.info(f"  Non-technical: {stage_counts.get('non_technical', 0)}")
        logger.info(f"  Semi-technical: {stage_counts.get('semi_technical', 0)}")
        logger.info(f"  Technical: {stage_counts.get('technical', 0)}")
        
        # Generate summary statistics with category breakdown
        generate_collection_summary(collected_resumes, output_dir)
        
        return collected_resumes
        
    except Exception as e:
        logger.error(f"GitHub collection failed: {e}")
        return []

def generate_collection_summary(resumes: List[Resume], output_dir: str):
    """Generate summary statistics for collected resumes"""
    try:
        summary = {
            "total_resumes": len(resumes),
            "collection_date": datetime.now().isoformat(),
            "statistics": {
                "experience_levels": {},
                "top_skills": {},
                "locations": {},
                "companies": {}
            }
        }
        
        # Analyze collected data
        for resume in resumes:
            # Experience levels
            level = resume.experience_level
            summary["statistics"]["experience_levels"][level] = \
                summary["statistics"]["experience_levels"].get(level, 0) + 1
            
            # Skills
            for skill in resume.skills:
                summary["statistics"]["top_skills"][skill] = \
                    summary["statistics"]["top_skills"].get(skill, 0) + 1
            
            # Locations
            if resume.location:
                summary["statistics"]["locations"][resume.location] = \
                    summary["statistics"]["locations"].get(resume.location, 0) + 1
            
            # Companies
            for job in resume.jobs:
                if job.company:
                    summary["statistics"]["companies"][job.company] = \
                        summary["statistics"]["companies"].get(job.company, 0) + 1
            
            # Categories (if available)
            if hasattr(resume, 'category'):
                if "categories" not in summary["statistics"]:
                    summary["statistics"]["categories"] = {}
                summary["statistics"]["categories"][resume.category] = \
                    summary["statistics"]["categories"].get(resume.category, 0) + 1
        
        # Save summary
        summary_file = os.path.join(output_dir, "collection_summary.json")
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        logger.info(f"Collection summary saved to {summary_file}")
        
        # Print key statistics
        print("\n" + "="*50)
        print("COLLECTION SUMMARY")
        print("="*50)
        print(f"Total Resumes Collected: {summary['total_resumes']}")
        
        # Categories breakdown
        if "categories" in summary["statistics"]:
            print(f"\nJob Categories:")
            for category, count in summary["statistics"]["categories"].items():
                print(f"  {category.replace('_', ' ').title()}: {count}")
        
        print(f"\nExperience Levels:")
        for level, count in summary["statistics"]["experience_levels"].items():
            print(f"  {level.title()}: {count}")
        
        print(f"\nTop 10 Skills:")
        top_skills = sorted(summary["statistics"]["top_skills"].items(), 
                          key=lambda x: x[1], reverse=True)[:10]
        for skill, count in top_skills:
            print(f"  {skill}: {count}")
        
        print(f"\nTop 10 Locations:")
        top_locations = sorted(summary["statistics"]["locations"].items(), 
                             key=lambda x: x[1], reverse=True)[:10]
        for location, count in top_locations:
            print(f"  {location}: {count}")
        
    except Exception as e:
        logger.error(f"Failed to generate summary: {e}")

if __name__ == "__main__":
    logger.info("Starting GitHub Developer Resume Collection...")
    
    # Use environment variable for GitHub token
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    
    # Check if GitHub token is available
    if not GITHUB_TOKEN:
        logger.error("GitHub token is required. Please set the GITHUB_TOKEN environment variable.")
        logger.info("You can set it with: export GITHUB_TOKEN=your_token_here")
        exit(1)
    
    print("GitHub Multi-Stage Resume Collection")
    print("="*60)
    print("Target: 50 professional resumes (initial batch)")
    print("Source: GitHub repositories and profiles")
    print("Data: Profile info, repositories, enhanced skills analysis")
    print()
    print("MULTI-STAGE STRATEGY:")
    print("  Stage 1: Non-Technical (20 target)")
    print("    - Healthcare, Business")
    print("  Stage 2: Semi-Technical (15 target)")
    print("    - Product Managers, Data Analysts")
    print("  Stage 3: Technical (15 target)")
    print("    - Software Engineers, Developers")
    print()
    print("Rate Limit: 5,000 requests/hour (respectful delays)")
    print("="*60)
    
    # Initialize collector and run collection
    collector = GitHubResumeCollector()
    
    # Run collection
    logger.info("Starting GitHub collection for 50 resumes...")
    collected_resumes = collector.collect_resumes(target_count=50)
    
    if collected_resumes:
        print(f"\n✅ Successfully collected {len(collected_resumes)} developer resumes!")
        
        # Save all resumes to a single JSON file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f"github_resumes_{timestamp}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(collected_resumes, f, indent=2, ensure_ascii=False)
        
        print(f"📄 Resumes saved to: {output_file}")
        
        # Show summary statistics
        print(f"\n📊 COLLECTION SUMMARY:")
        print(f"  Total resumes: {len(collected_resumes)}")
        
        # Count by category if available
        categories = {}
        skills_count = {}
        locations = {}
        
        for resume in collected_resumes:
            # Skills analysis
            for skill in resume.get('skills', []):
                skills_count[skill] = skills_count.get(skill, 0) + 1
            
            # Location analysis
            location = resume.get('location', 'Unknown')
            if location and location.strip():
                locations[location] = locations.get(location, 0) + 1
        
        # Top skills
        top_skills = sorted(skills_count.items(), key=lambda x: x[1], reverse=True)[:10]
        print(f"  Top skills: {', '.join([f'{skill}({count})' for skill, count in top_skills])}")
        
        # Top locations
        top_locations = sorted(locations.items(), key=lambda x: x[1], reverse=True)[:5]
        print(f"  Top locations: {', '.join([f'{loc}({count})' for loc, count in top_locations])}")
        
        print(f"  API requests used: {collector.request_count}")
        
    else:
        print("\n❌ No resumes were collected. Check the logs for details.")
        logger.warning("Collection failed - check GitHub token and rate limits")