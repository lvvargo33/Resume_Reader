#!/usr/bin/env python3
"""
Quick demonstration of the enhanced GitHub resume collection with skills analysis
"""

import requests
import json
import time
import os
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# GitHub API Configuration
GITHUB_API_BASE = "https://api.github.com"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

class QuickGitHubCollector:
    def __init__(self):
        self.headers = {
            'Authorization': f'token {GITHUB_TOKEN}',
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'Resume-Research-Bot/1.0'
        }
        self.request_count = 0
        
        # Enhanced skills detection patterns
        self.skill_patterns = {
            'frontend_frameworks': {
                'react': ['react', 'reactjs', 'react.js'],
                'vue': ['vue', 'vuejs', 'vue.js'],
                'angular': ['angular', 'angularjs']
            },
            'backend_frameworks': {
                'django': ['django', 'django-rest-framework'],
                'flask': ['flask', 'flask-restful'],
                'express': ['express', 'expressjs']
            },
            'databases': {
                'postgresql': ['postgresql', 'postgres'],
                'mysql': ['mysql', 'mariadb'],
                'mongodb': ['mongodb', 'mongo']
            },
            'cloud_devops': {
                'aws': ['aws', 'amazon-web-services'],
                'docker': ['docker', 'dockerfile'],
                'kubernetes': ['kubernetes', 'k8s']
            }
        }
    
    def make_request(self, url):
        """Make GitHub API request with error handling"""
        try:
            response = requests.get(url, headers=self.headers)
            self.request_count += 1
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.warning(f"API request failed: {response.status_code}")
                return None
        except Exception as e:
            logger.error(f"Request error: {e}")
            return None
    
    def analyze_skills(self, repositories):
        """Analyze skills from repositories"""
        languages = {}
        frameworks = {}
        total_repos = len(repositories)
        total_stars = 0
        
        for repo in repositories:
            # Language analysis
            if repo.get('language'):
                lang = repo['language'].lower()
                languages[lang] = languages.get(lang, 0) + 1
            
            # Stars for proficiency
            total_stars += repo.get('stargazers_count', 0)
            
            # Framework detection
            repo_text = f"{repo.get('name', '')} {repo.get('description', '')}".lower()
            for category, framework_dict in self.skill_patterns.items():
                for framework, patterns in framework_dict.items():
                    for pattern in patterns:
                        if pattern in repo_text:
                            if category not in frameworks:
                                frameworks[category] = {}
                            frameworks[category][framework] = frameworks[category].get(framework, 0) + 1
        
        # Calculate proficiency
        repo_score = min(total_repos / 20, 1.0)
        star_score = min(total_stars / 100, 1.0)
        overall_score = (repo_score * 0.6) + (star_score * 0.4)
        
        if overall_score >= 0.7:
            proficiency = 'expert'
        elif overall_score >= 0.5:
            proficiency = 'advanced'
        elif overall_score >= 0.3:
            proficiency = 'intermediate'
        else:
            proficiency = 'beginner'
        
        # Build skills list
        top_languages = sorted(languages.items(), key=lambda x: x[1], reverse=True)[:5]
        skills_list = [lang.title() for lang, count in top_languages]
        
        return {
            'skills_list': skills_list,
            'languages': languages,
            'frameworks': frameworks,
            'proficiency': proficiency,
            'total_repos': total_repos,
            'total_stars': total_stars
        }
    
    def collect_sample_resumes(self, target=10):
        """Collect a small sample of resumes for demonstration"""
        resumes = []
        
        # Search for users with specific keywords
        keywords = ['software engineer', 'data analyst', 'product manager', 'developer']
        
        for keyword in keywords:
            if len(resumes) >= target:
                break
                
            logger.info(f"Searching for: {keyword}")
            search_url = f"{GITHUB_API_BASE}/search/users?q={keyword}+in:bio&per_page=10"
            
            users_data = self.make_request(search_url)
            if not users_data or 'items' not in users_data:
                continue
            
            time.sleep(1)  # Rate limiting
            
            for user in users_data['items'][:3]:  # Limit to 3 per keyword
                if len(resumes) >= target:
                    break
                
                username = user['login']
                logger.info(f"Processing user: {username}")
                
                # Get user profile
                profile_url = f"{GITHUB_API_BASE}/users/{username}"
                profile = self.make_request(profile_url)
                
                if not profile:
                    continue
                
                time.sleep(0.5)
                
                # Get repositories
                repos_url = f"{GITHUB_API_BASE}/users/{username}/repos?per_page=50"
                repos = self.make_request(repos_url)
                
                if not repos:
                    repos = []
                
                time.sleep(0.5)
                
                # Analyze skills
                skills_analysis = self.analyze_skills(repos)
                
                # Create resume data
                resume_data = {
                    'id': username,
                    'name': profile.get('name', username),
                    'bio': profile.get('bio', ''),
                    'location': profile.get('location', ''),
                    'company': profile.get('company', ''),
                    'public_repos': profile.get('public_repos', 0),
                    'followers': profile.get('followers', 0),
                    'created_at': profile.get('created_at', ''),
                    'skills': skills_analysis['skills_list'],
                    'skill_proficiency': skills_analysis['proficiency'],
                    'github_stats': {
                        'total_repos': skills_analysis['total_repos'],
                        'total_stars': skills_analysis['total_stars'],
                        'languages': skills_analysis['languages']
                    },
                    'technology_stack': skills_analysis['frameworks'],
                    'search_keyword': keyword
                }
                
                resumes.append(resume_data)
                logger.info(f"Collected resume {len(resumes)}/{target}: {resume_data['name']}")
        
        return resumes

def main():
    """Main execution function"""
    print("GitHub Resume Collection - Quick Demo")
    print("="*50)
    print("Target: 10 resumes for demonstration")
    print("Enhanced skills analysis with technology stacks")
    print("="*50)
    
    # Check if GitHub token is available
    if not GITHUB_TOKEN:
        print("❌ GitHub token is required. Please set the GITHUB_TOKEN environment variable.")
        print("   Example: export GITHUB_TOKEN=your_token_here")
        return []
    
    collector = QuickGitHubCollector()
    
    # Collect sample resumes
    logger.info("Starting collection...")
    resumes = collector.collect_sample_resumes(target=10)
    
    if resumes:
        # Save to file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"sample_resumes_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(resumes, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Successfully collected {len(resumes)} resumes!")
        print(f"📄 Saved to: {filename}")
        print(f"🔄 API requests used: {collector.request_count}")
        
        # Show sample data
        print(f"\n📊 SAMPLE RESULTS:")
        for i, resume in enumerate(resumes[:3], 1):
            print(f"\n{i}. {resume['name']} (@{resume['id']})")
            print(f"   Bio: {resume['bio'][:100]}...")
            print(f"   Location: {resume['location']}")
            print(f"   Company: {resume['company']}")
            print(f"   Skills: {', '.join(resume['skills'])}")
            print(f"   Proficiency: {resume['skill_proficiency']}")
            print(f"   Repos: {resume['github_stats']['total_repos']}")
        
        # Skills summary
        all_skills = {}
        for resume in resumes:
            for skill in resume['skills']:
                all_skills[skill] = all_skills.get(skill, 0) + 1
        
        top_skills = sorted(all_skills.items(), key=lambda x: x[1], reverse=True)[:10]
        print(f"\n🎯 Top Skills Across All Resumes:")
        for skill, count in top_skills:
            print(f"   {skill}: {count} people")
        
        return resumes
    else:
        print("❌ No resumes collected")
        return []

if __name__ == "__main__":
    main()