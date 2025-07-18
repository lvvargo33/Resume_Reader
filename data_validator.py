#!/usr/bin/env python3
"""
Data Validator for GitHub Resume Collection
Quality checks, deduplication, and comprehensive statistics
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Set, Tuple
from collections import Counter, defaultdict
import statistics
import re


class ResumeDataValidator:
    def __init__(self):
        self.validation_results = {
            'total_resumes': 0,
            'valid_resumes': 0,
            'invalid_resumes': 0,
            'duplicates': 0,
            'quality_issues': defaultdict(int),
            'field_completeness': defaultdict(int),
            'skill_distribution': Counter(),
            'location_distribution': Counter(),
            'experience_distribution': defaultdict(int)
        }
    
    def validate_email(self, email: str) -> bool:
        """Validate email format"""
        if not email:
            return False
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    def validate_url(self, url: str) -> bool:
        """Validate URL format"""
        if not url:
            return False
        pattern = r'^https?://[^\s/$.?#].[^\s]*$'
        return bool(re.match(pattern, url))
    
    def calculate_resume_quality_score(self, resume: Dict) -> Tuple[float, List[str]]:
        """Calculate quality score for a resume (0-100)"""
        score = 0
        issues = []
        
        # Required fields (40 points)
        required_fields = ['github_username', 'github_url', 'name']
        for field in required_fields:
            if resume.get(field):
                score += 40 / len(required_fields)
            else:
                issues.append(f"Missing required field: {field}")
        
        # Contact information (20 points)
        if resume.get('email') and self.validate_email(resume['email']):
            score += 10
        elif resume.get('email'):
            issues.append("Invalid email format")
        
        if resume.get('location'):
            score += 5
        
        if resume.get('blog') and self.validate_url(resume['blog']):
            score += 5
        
        # Professional information (20 points)
        if resume.get('bio') and len(resume['bio']) > 20:
            score += 10
        elif resume.get('bio'):
            issues.append("Bio too short")
        
        if resume.get('company'):
            score += 10
        
        # Technical information (20 points)
        if resume.get('skills') and len(resume['skills']) > 0:
            score += 10
        else:
            issues.append("No skills identified")
        
        if resume.get('public_repos', 0) > 5:
            score += 5
        
        if resume.get('top_repos') and len(resume['top_repos']) > 0:
            score += 5
        else:
            issues.append("No repository information")
        
        return score, issues
    
    def analyze_experience_level(self, resume: Dict) -> str:
        """Estimate experience level based on account age and activity"""
        created_at = resume.get('created_at', '')
        if not created_at:
            return 'unknown'
        
        try:
            created_date = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
            years_active = (datetime.now() - created_date.replace(tzinfo=None)).days / 365
            
            repos = resume.get('public_repos', 0)
            followers = resume.get('followers', 0)
            
            # Simple heuristic for experience level
            if years_active < 1:
                return 'entry'
            elif years_active < 3 and repos < 20:
                return 'junior'
            elif years_active < 5 or (repos < 50 and followers < 100):
                return 'mid'
            elif years_active < 8 or (repos < 100 and followers < 500):
                return 'senior'
            else:
                return 'expert'
        except:
            return 'unknown'
    
    def categorize_technical_level(self, resume: Dict) -> str:
        """Categorize resume as technical, semi-technical, or non-technical"""
        skills = resume.get('skills', [])
        repos = resume.get('public_repos', 0)
        top_repos = resume.get('top_repos', [])
        
        # Count technical indicators
        technical_score = 0
        
        # Programming languages
        programming_languages = {
            'Python', 'JavaScript', 'Java', 'C++', 'C', 'C#', 'Go', 'Rust', 
            'Ruby', 'PHP', 'Swift', 'Kotlin', 'TypeScript', 'Scala', 'R'
        }
        
        technical_skills = set(skills) & programming_languages
        technical_score += len(technical_skills) * 2
        
        # Repository activity
        if repos > 10:
            technical_score += 3
        elif repos > 5:
            technical_score += 2
        elif repos > 0:
            technical_score += 1
        
        # Check repository languages
        for repo in top_repos[:5]:
            if repo.get('language') in programming_languages:
                technical_score += 1
        
        # Categorize based on score
        if technical_score >= 8:
            return 'technical'
        elif technical_score >= 3:
            return 'semi-technical'
        else:
            return 'non-technical'
    
    def validate_batch(self, resumes: List[Dict]) -> Dict:
        """Validate a batch of resumes"""
        seen_usernames = set()
        valid_resumes = []
        
        for resume in resumes:
            self.validation_results['total_resumes'] += 1
            
            # Check for duplicates
            username = resume.get('github_username')
            if username in seen_usernames:
                self.validation_results['duplicates'] += 1
                continue
            seen_usernames.add(username)
            
            # Calculate quality score
            quality_score, issues = self.calculate_resume_quality_score(resume)
            
            if quality_score >= 40:  # Minimum acceptable quality
                self.validation_results['valid_resumes'] += 1
                valid_resumes.append(resume)
                
                # Track field completeness
                for field in ['name', 'email', 'location', 'bio', 'company', 'blog']:
                    if resume.get(field):
                        self.validation_results['field_completeness'][field] += 1
                
                # Track skills
                for skill in resume.get('skills', []):
                    self.validation_results['skill_distribution'][skill] += 1
                
                # Track location
                location = resume.get('location', 'Unknown')
                if location:
                    # Extract country/city
                    location_parts = location.split(',')
                    if len(location_parts) > 1:
                        country = location_parts[-1].strip()
                    else:
                        country = location_parts[0].strip()
                    self.validation_results['location_distribution'][country] += 1
                
                # Track experience level
                exp_level = self.analyze_experience_level(resume)
                self.validation_results['experience_distribution'][exp_level] += 1
                
                # Track technical level
                tech_level = self.categorize_technical_level(resume)
                self.validation_results['experience_distribution'][f'category_{tech_level}'] += 1
            
            else:
                self.validation_results['invalid_resumes'] += 1
                for issue in issues:
                    self.validation_results['quality_issues'][issue] += 1
        
        return {
            'valid_resumes': valid_resumes,
            'validation_summary': self.get_validation_summary()
        }
    
    def get_validation_summary(self) -> Dict:
        """Get comprehensive validation summary"""
        total = self.validation_results['total_resumes']
        if total == 0:
            return {}
        
        # Calculate percentages
        field_completeness_pct = {}
        for field, count in self.validation_results['field_completeness'].items():
            field_completeness_pct[field] = (count / self.validation_results['valid_resumes'] * 100 
                                           if self.validation_results['valid_resumes'] > 0 else 0)
        
        # Top skills
        top_skills = self.validation_results['skill_distribution'].most_common(20)
        
        # Top locations
        top_locations = self.validation_results['location_distribution'].most_common(10)
        
        # Category distribution
        categories = {
            'technical': self.validation_results['experience_distribution'].get('category_technical', 0),
            'semi_technical': self.validation_results['experience_distribution'].get('category_semi-technical', 0),
            'non_technical': self.validation_results['experience_distribution'].get('category_non-technical', 0)
        }
        
        return {
            'total_processed': total,
            'valid_resumes': self.validation_results['valid_resumes'],
            'invalid_resumes': self.validation_results['invalid_resumes'],
            'duplicates_found': self.validation_results['duplicates'],
            'validation_rate': self.validation_results['valid_resumes'] / total * 100,
            'field_completeness_percentage': field_completeness_pct,
            'top_skills': top_skills,
            'top_locations': top_locations,
            'experience_levels': {
                'entry': self.validation_results['experience_distribution'].get('entry', 0),
                'junior': self.validation_results['experience_distribution'].get('junior', 0),
                'mid': self.validation_results['experience_distribution'].get('mid', 0),
                'senior': self.validation_results['experience_distribution'].get('senior', 0),
                'expert': self.validation_results['experience_distribution'].get('expert', 0),
                'unknown': self.validation_results['experience_distribution'].get('unknown', 0)
            },
            'technical_categories': categories,
            'category_percentages': {
                'technical': categories['technical'] / self.validation_results['valid_resumes'] * 100 
                           if self.validation_results['valid_resumes'] > 0 else 0,
                'semi_technical': categories['semi_technical'] / self.validation_results['valid_resumes'] * 100 
                                if self.validation_results['valid_resumes'] > 0 else 0,
                'non_technical': categories['non_technical'] / self.validation_results['valid_resumes'] * 100 
                               if self.validation_results['valid_resumes'] > 0 else 0
            },
            'quality_issues': dict(self.validation_results['quality_issues'])
        }
    
    def generate_detailed_report(self, output_file: str = "validation_report.txt") -> None:
        """Generate a detailed validation report"""
        summary = self.get_validation_summary()
        
        with open(output_file, 'w') as f:
            f.write("=" * 60 + "\n")
            f.write("GitHub Resume Collection - Data Validation Report\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 60 + "\n\n")
            
            # Overall Statistics
            f.write("OVERALL STATISTICS\n")
            f.write("-" * 30 + "\n")
            f.write(f"Total Resumes Processed: {summary['total_processed']}\n")
            f.write(f"Valid Resumes: {summary['valid_resumes']} ({summary['validation_rate']:.1f}%)\n")
            f.write(f"Invalid Resumes: {summary['invalid_resumes']}\n")
            f.write(f"Duplicates Found: {summary['duplicates_found']}\n\n")
            
            # Field Completeness
            f.write("FIELD COMPLETENESS\n")
            f.write("-" * 30 + "\n")
            for field, pct in summary['field_completeness_percentage'].items():
                f.write(f"{field.capitalize()}: {pct:.1f}%\n")
            f.write("\n")
            
            # Technical Categories
            f.write("TECHNICAL CATEGORIES\n")
            f.write("-" * 30 + "\n")
            for cat, pct in summary['category_percentages'].items():
                count = summary['technical_categories'][cat]
                f.write(f"{cat.replace('_', ' ').title()}: {count} ({pct:.1f}%)\n")
            f.write("\n")
            
            # Experience Levels
            f.write("EXPERIENCE LEVELS\n")
            f.write("-" * 30 + "\n")
            for level, count in summary['experience_levels'].items():
                f.write(f"{level.capitalize()}: {count}\n")
            f.write("\n")
            
            # Top Skills
            f.write("TOP 20 SKILLS\n")
            f.write("-" * 30 + "\n")
            for skill, count in summary['top_skills']:
                f.write(f"{skill}: {count}\n")
            f.write("\n")
            
            # Top Locations
            f.write("TOP 10 LOCATIONS\n")
            f.write("-" * 30 + "\n")
            for location, count in summary['top_locations']:
                f.write(f"{location}: {count}\n")
            f.write("\n")
            
            # Quality Issues
            if summary['quality_issues']:
                f.write("QUALITY ISSUES FOUND\n")
                f.write("-" * 30 + "\n")
                for issue, count in sorted(summary['quality_issues'].items(), 
                                         key=lambda x: x[1], reverse=True):
                    f.write(f"{issue}: {count}\n")
        
        print(f"Validation report saved to: {output_file}")


class DataCleaner:
    """Clean and standardize resume data"""
    
    @staticmethod
    def clean_location(location: str) -> Dict[str, str]:
        """Parse and standardize location data"""
        if not location:
            return {'city': '', 'state': '', 'country': ''}
        
        # Common patterns
        parts = [p.strip() for p in location.split(',')]
        
        if len(parts) >= 3:
            return {'city': parts[0], 'state': parts[1], 'country': parts[2]}
        elif len(parts) == 2:
            # Could be City, Country or City, State
            if parts[1].upper() in ['USA', 'US', 'UK', 'CA', 'AU']:
                return {'city': parts[0], 'state': '', 'country': parts[1]}
            else:
                return {'city': parts[0], 'state': parts[1], 'country': ''}
        else:
            return {'city': parts[0], 'state': '', 'country': ''}
    
    @staticmethod
    def normalize_skills(skills: List[str]) -> List[str]:
        """Normalize skill names"""
        # Common mappings
        skill_mappings = {
            'Javascript': 'JavaScript',
            'Typescript': 'TypeScript',
            'nodejs': 'Node.js',
            'Nodejs': 'Node.js',
            'node': 'Node.js',
            'react': 'React',
            'React.js': 'React',
            'vue': 'Vue.js',
            'angular': 'Angular',
            'golang': 'Go',
            'cpp': 'C++',
            'csharp': 'C#',
            'objective-c': 'Objective-C',
            'Jupyter Notebook': 'Python',  # Often Jupyter files are categorized separately
        }
        
        normalized = []
        for skill in skills:
            normalized_skill = skill_mappings.get(skill, skill)
            if normalized_skill not in normalized:
                normalized.append(normalized_skill)
        
        return normalized
    
    @staticmethod
    def clean_resume_batch(resumes: List[Dict]) -> List[Dict]:
        """Clean a batch of resumes"""
        cleaned = []
        
        for resume in resumes:
            # Clean location
            location_data = DataCleaner.clean_location(resume.get('location', ''))
            resume['location_parsed'] = location_data
            
            # Normalize skills
            if resume.get('skills'):
                resume['skills'] = DataCleaner.normalize_skills(resume['skills'])
            
            # Clean URLs
            if resume.get('blog'):
                blog = resume['blog'].strip()
                if blog and not blog.startswith(('http://', 'https://')):
                    resume['blog'] = f"https://{blog}"
            
            # Ensure consistent date formats
            for date_field in ['created_at', 'updated_at', 'collected_at']:
                if resume.get(date_field):
                    try:
                        # Ensure ISO format
                        if 'Z' in resume[date_field]:
                            resume[date_field] = resume[date_field].replace('Z', '+00:00')
                    except:
                        pass
            
            cleaned.append(resume)
        
        return cleaned


def validate_collection_file(file_path: str) -> None:
    """Validate a single collection file"""
    print(f"\nValidating: {file_path}")
    print("=" * 60)
    
    # Load data
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    resumes = data.get('resumes', [])
    metadata = data.get('metadata', {})
    
    print(f"File metadata:")
    print(f"  - Count: {metadata.get('count', 'Unknown')}")
    print(f"  - Collected at: {metadata.get('collected_at', 'Unknown')}")
    print(f"  - Errors: {metadata.get('errors', 'Unknown')}")
    
    # Validate data
    validator = ResumeDataValidator()
    results = validator.validate_batch(resumes)
    
    # Print summary
    summary = results['validation_summary']
    print(f"\nValidation Results:")
    print(f"  - Valid resumes: {summary['valid_resumes']}")
    print(f"  - Invalid resumes: {summary['invalid_resumes']}")
    print(f"  - Duplicates: {summary['duplicates_found']}")
    print(f"  - Validation rate: {summary['validation_rate']:.1f}%")
    
    print(f"\nCategory Distribution:")
    for cat, pct in summary['category_percentages'].items():
        print(f"  - {cat.replace('_', ' ').title()}: {pct:.1f}%")
    
    # Generate detailed report
    report_name = file_path.replace('.json', '_validation_report.txt')
    validator.generate_detailed_report(report_name)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # Validate specific file
        validate_collection_file(sys.argv[1])
    else:
        # Example usage
        print("Usage: python data_validator.py <collection_file.json>")
        print("\nExample:")
        print("  python data_validator.py resume_collections/batch_20240719_120000.json")