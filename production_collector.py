#!/usr/bin/env python3
"""
Production GitHub Resume Collector
Optimized for large-scale collection with rate limiting and progress tracking
"""

import json
import time
import os
import sys
from datetime import datetime
from typing import Dict, List, Optional, Set
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('collection.log')
    ]
)
logger = logging.getLogger(__name__)


class GitHubResumeCollector:
    def __init__(self, token: str, checkpoint_file: str = "collection_checkpoint.json"):
        self.token = token
        self.checkpoint_file = checkpoint_file
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        # Optimized settings
        self.min_delay = 0.3  # Reduced from 0.5
        self.max_results_per_page = 100  # Maximum allowed by GitHub
        self.batch_save_interval = 100  # Save progress every 100 resumes
        
        # Session with retry strategy
        self.session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        # Progress tracking
        self.collected_users: Set[str] = set()
        self.resumes_collected = 0
        self.errors_encountered = 0
        self.start_time = None
        
        # Load checkpoint if exists
        self.load_checkpoint()
    
    def load_checkpoint(self) -> None:
        """Load progress from checkpoint file"""
        if os.path.exists(self.checkpoint_file):
            try:
                with open(self.checkpoint_file, 'r') as f:
                    checkpoint = json.load(f)
                    self.collected_users = set(checkpoint.get('collected_users', []))
                    self.resumes_collected = checkpoint.get('resumes_collected', 0)
                    logger.info(f"Resumed from checkpoint: {self.resumes_collected} resumes collected")
            except Exception as e:
                logger.warning(f"Could not load checkpoint: {e}")
    
    def save_checkpoint(self) -> None:
        """Save current progress to checkpoint file"""
        checkpoint = {
            'collected_users': list(self.collected_users),
            'resumes_collected': self.resumes_collected,
            'last_updated': datetime.now().isoformat()
        }
        with open(self.checkpoint_file, 'w') as f:
            json.dump(checkpoint, f)
        logger.info(f"Checkpoint saved: {self.resumes_collected} resumes")
    
    def check_rate_limit(self) -> Dict:
        """Check GitHub API rate limit"""
        response = self.session.get(f"{self.base_url}/rate_limit", headers=self.headers)
        if response.status_code == 200:
            return response.json()
        return {}
    
    def wait_for_rate_limit(self, response_headers: Dict) -> None:
        """Wait if rate limit is approaching"""
        remaining = int(response_headers.get('X-RateLimit-Remaining', 1))
        reset_time = int(response_headers.get('X-RateLimit-Reset', 0))
        
        if remaining < 10:
            wait_time = max(reset_time - time.time(), 0) + 1
            logger.warning(f"Rate limit approaching. Waiting {wait_time:.0f} seconds...")
            time.sleep(wait_time)
    
    def search_users(self, query: str, page: int = 1) -> List[Dict]:
        """Search for GitHub users"""
        params = {
            'q': query,
            'per_page': self.max_results_per_page,
            'page': page,
            'sort': 'repositories',
            'order': 'desc'
        }
        
        try:
            response = self.session.get(
                f"{self.base_url}/search/users",
                headers=self.headers,
                params=params,
                timeout=30
            )
            
            self.wait_for_rate_limit(response.headers)
            
            if response.status_code == 200:
                return response.json().get('items', [])
            else:
                logger.error(f"Search failed: {response.status_code} - {response.text}")
                return []
                
        except Exception as e:
            logger.error(f"Search error: {e}")
            self.errors_encountered += 1
            return []
    
    def get_user_details(self, username: str) -> Optional[Dict]:
        """Get detailed user profile"""
        if username in self.collected_users:
            return None
            
        try:
            response = self.session.get(
                f"{self.base_url}/users/{username}",
                headers=self.headers,
                timeout=30
            )
            
            self.wait_for_rate_limit(response.headers)
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.warning(f"Failed to get user {username}: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error fetching user {username}: {e}")
            self.errors_encountered += 1
            return None
    
    def get_user_repos(self, username: str, max_repos: int = 10) -> List[Dict]:
        """Get user's repositories"""
        try:
            response = self.session.get(
                f"{self.base_url}/users/{username}/repos",
                headers=self.headers,
                params={'per_page': max_repos, 'sort': 'updated'},
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            return []
            
        except Exception as e:
            logger.error(f"Error fetching repos for {username}: {e}")
            return []
    
    def extract_skills_from_repos(self, repos: List[Dict]) -> List[str]:
        """Extract programming languages from repositories"""
        skills = set()
        
        for repo in repos:
            if repo.get('language'):
                skills.add(repo['language'])
            
            # Get languages breakdown for more detail
            if repo.get('languages_url'):
                try:
                    response = self.session.get(
                        repo['languages_url'],
                        headers=self.headers,
                        timeout=10
                    )
                    if response.status_code == 200:
                        languages = response.json()
                        skills.update(languages.keys())
                except:
                    pass
        
        return list(skills)
    
    def should_skip_user(self, user_profile: Dict) -> bool:
        """Determine if user should be skipped based on profile completeness"""
        # Skip users with incomplete profiles
        if not user_profile.get('bio') and user_profile.get('public_repos', 0) < 5:
            return True
        
        # Skip if no email and no company/location info
        if not any([user_profile.get('email'), user_profile.get('company'), 
                   user_profile.get('location'), user_profile.get('blog')]):
            if user_profile.get('public_repos', 0) < 10:
                return True
        
        return False
    
    def create_resume_entry(self, user_data: Dict, repos: List[Dict]) -> Dict:
        """Create a resume entry from user data"""
        skills = self.extract_skills_from_repos(repos)
        
        return {
            'github_username': user_data['login'],
            'name': user_data.get('name', ''),
            'email': user_data.get('email', ''),
            'location': user_data.get('location', ''),
            'bio': user_data.get('bio', ''),
            'company': user_data.get('company', ''),
            'blog': user_data.get('blog', ''),
            'github_url': user_data['html_url'],
            'avatar_url': user_data['avatar_url'],
            'public_repos': user_data.get('public_repos', 0),
            'followers': user_data.get('followers', 0),
            'following': user_data.get('following', 0),
            'created_at': user_data.get('created_at', ''),
            'updated_at': user_data.get('updated_at', ''),
            'skills': skills,
            'top_repos': [
                {
                    'name': repo['name'],
                    'description': repo.get('description', ''),
                    'language': repo.get('language', ''),
                    'stars': repo.get('stargazers_count', 0),
                    'forks': repo.get('forks_count', 0),
                    'url': repo['html_url']
                }
                for repo in repos[:5]  # Top 5 repos
            ],
            'collected_at': datetime.now().isoformat()
        }
    
    def collect_resumes(self, search_queries: List[str], target_count: int = 1000) -> List[Dict]:
        """Main collection method"""
        self.start_time = time.time()
        resumes = []
        query_index = 0
        page = 1
        
        logger.info(f"Starting collection. Target: {target_count} resumes")
        
        while self.resumes_collected < target_count and query_index < len(search_queries):
            current_query = search_queries[query_index]
            logger.info(f"Searching with query: '{current_query}' (page {page})")
            
            users = self.search_users(current_query, page)
            
            if not users:
                # Move to next query
                query_index += 1
                page = 1
                continue
            
            for user in users:
                if self.resumes_collected >= target_count:
                    break
                
                username = user['login']
                
                # Get detailed user data
                user_profile = self.get_user_details(username)
                if not user_profile:
                    continue
                
                # Skip incomplete profiles
                if self.should_skip_user(user_profile):
                    logger.debug(f"Skipping user {username} - incomplete profile")
                    continue
                
                # Get user repositories
                repos = self.get_user_repos(username)
                
                # Create resume entry
                resume = self.create_resume_entry(user_profile, repos)
                resumes.append(resume)
                
                self.collected_users.add(username)
                self.resumes_collected += 1
                
                # Progress update
                if self.resumes_collected % 10 == 0:
                    elapsed = time.time() - self.start_time
                    rate = self.resumes_collected / elapsed * 3600
                    logger.info(f"Progress: {self.resumes_collected}/{target_count} resumes "
                              f"({rate:.0f}/hour) - Errors: {self.errors_encountered}")
                
                # Save checkpoint
                if self.resumes_collected % self.batch_save_interval == 0:
                    self.save_checkpoint()
                    # Also save partial results
                    self.save_batch_results(resumes)
                
                # Rate limiting delay
                time.sleep(self.min_delay)
            
            page += 1
            
            # GitHub limits search results to 1000 per query
            if page > 10:  # 100 results per page * 10 pages = 1000 max
                query_index += 1
                page = 1
        
        # Final save
        self.save_checkpoint()
        logger.info(f"Collection completed: {self.resumes_collected} resumes in "
                   f"{time.time() - self.start_time:.1f} seconds")
        
        return resumes
    
    def save_batch_results(self, resumes: List[Dict]) -> None:
        """Save current batch of results"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"resume_collections/batch_partial_{timestamp}.json"
        
        os.makedirs("resume_collections", exist_ok=True)
        
        with open(filename, 'w') as f:
            json.dump({
                'metadata': {
                    'count': len(resumes),
                    'collected_at': datetime.now().isoformat(),
                    'errors': self.errors_encountered
                },
                'resumes': resumes
            }, f, indent=2)
        
        logger.info(f"Saved partial results to {filename}")


def main():
    # Check for GitHub token
    token = os.environ.get('GITHUB_TOKEN')
    if not token:
        logger.error("GITHUB_TOKEN environment variable not set!")
        logger.info("Set it with: export GITHUB_TOKEN=your_token_here")
        sys.exit(1)
    
    # Create collector
    collector = GitHubResumeCollector(token)
    
    # Check rate limit before starting
    rate_info = collector.check_rate_limit()
    if rate_info:
        core_limit = rate_info.get('resources', {}).get('core', {})
        logger.info(f"Rate limit: {core_limit.get('remaining', 0)}/{core_limit.get('limit', 0)}")
    
    # Define search queries for diverse results
    search_queries = [
        # Technical roles
        "fullstack developer location:USA",
        "software engineer python",
        "backend developer java",
        "frontend developer react",
        "devops engineer kubernetes",
        "data scientist machine learning",
        "mobile developer ios android",
        "cloud architect aws",
        
        # Semi-technical roles
        "technical writer documentation",
        "product manager software",
        "ux designer developer",
        "qa engineer automation",
        "scrum master agile",
        
        # Geographic diversity
        "developer location:London",
        "engineer location:Berlin",
        "programmer location:Toronto",
        "developer location:Sydney",
        "engineer location:Tokyo",
        "developer location:Bangalore",
        
        # Experience levels
        "junior developer",
        "senior engineer",
        "lead developer",
        "principal engineer",
        
        # Specific technologies
        "react native developer",
        "golang developer",
        "rust programmer",
        "blockchain developer",
        "ai ml engineer",
        "cybersecurity engineer"
    ]
    
    # Collect resumes
    target_count = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
    resumes = collector.collect_resumes(search_queries, target_count)
    
    # Save final results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"resume_collections/batch_{timestamp}.json"
    
    os.makedirs("resume_collections", exist_ok=True)
    
    with open(output_file, 'w') as f:
        json.dump({
            'metadata': {
                'count': len(resumes),
                'collected_at': datetime.now().isoformat(),
                'search_queries': search_queries,
                'errors': collector.errors_encountered,
                'collection_time_seconds': time.time() - collector.start_time
            },
            'resumes': resumes
        }, f, indent=2)
    
    logger.info(f"Collection complete! Saved {len(resumes)} resumes to {output_file}")
    
    # Print summary statistics
    print("\n=== Collection Summary ===")
    print(f"Total resumes collected: {len(resumes)}")
    print(f"Unique users: {len(collector.collected_users)}")
    print(f"Errors encountered: {collector.errors_encountered}")
    print(f"Collection time: {time.time() - collector.start_time:.1f} seconds")
    print(f"Output file: {output_file}")


if __name__ == "__main__":
    main()