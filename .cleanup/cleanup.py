#!/usr/bin/env python3
"""
File Cleanup Utility
Removes temporary and unused files based on cleanup_rules.json
"""

import os
import json
import time
import glob
from datetime import datetime, timedelta
from pathlib import Path

class ProjectCleaner:
    def __init__(self, config_path=".cleanup/cleanup_rules.json"):
        self.config_path = config_path
        self.load_config()
        self.cleanup_log = []
        
    def load_config(self):
        with open(self.config_path, 'r') as f:
            self.config = json.load(f)
    
    def is_protected(self, filepath):
        """Check if file is in protected paths"""
        for protected in self.config['protected_paths']:
            if protected in str(filepath):
                return True
        return False
    
    def is_old_enough(self, filepath, max_age_days):
        """Check if file is older than max_age_days"""
        file_age = time.time() - os.path.getmtime(filepath)
        return file_age > (max_age_days * 86400)
    
    def find_files_to_clean(self):
        """Find all files matching cleanup rules"""
        files_to_clean = []
        
        for category, rules in self.config['cleanup_rules'].items():
            if category == "empty_directories":
                continue
                
            for pattern in rules['patterns']:
                for filepath in glob.glob(f"**/{pattern}", recursive=True):
                    if self.is_protected(filepath):
                        continue
                    
                    # Check exclusions
                    excluded = any(excl in filepath for excl in rules['exclude'])
                    if excluded:
                        continue
                    
                    # Check age
                    if self.is_old_enough(filepath, rules['max_age_days']):
                        files_to_clean.append({
                            'path': filepath,
                            'category': category,
                            'age_days': self.get_file_age_days(filepath)
                        })
        
        return files_to_clean
    
    def get_file_age_days(self, filepath):
        """Get file age in days"""
        file_age = time.time() - os.path.getmtime(filepath)
        return int(file_age / 86400)
    
    def clean_empty_directories(self):
        """Remove empty directories"""
        if not self.config['cleanup_rules'].get('empty_directories', {}).get('enabled'):
            return []
        
        removed_dirs = []
        for root, dirs, files in os.walk('.', topdown=False):
            for dirname in dirs:
                dirpath = os.path.join(root, dirname)
                if self.is_protected(dirpath):
                    continue
                
                try:
                    if not os.listdir(dirpath):
                        os.rmdir(dirpath)
                        removed_dirs.append(dirpath)
                except:
                    pass
        
        return removed_dirs
    
    def run_cleanup(self, dry_run=True):
        """Run cleanup process"""
        print(f"{'DRY RUN' if dry_run else 'CLEANUP'} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 50)
        
        files_to_clean = self.find_files_to_clean()
        
        if not files_to_clean:
            print("No files to clean up!")
            return
        
        # Group by category
        by_category = {}
        for file_info in files_to_clean:
            cat = file_info['category']
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(file_info)
        
        # Display and clean
        total_size = 0
        for category, files in by_category.items():
            print(f"\n{category.upper()} ({len(files)} files):")
            for file_info in files:
                filepath = file_info['path']
                size = os.path.getsize(filepath)
                total_size += size
                print(f"  - {filepath} ({file_info['age_days']} days old, {size/1024:.1f}KB)")
                
                if not dry_run:
                    try:
                        os.remove(filepath)
                        self.cleanup_log.append({
                            'file': filepath,
                            'removed': datetime.now().isoformat(),
                            'category': category
                        })
                    except Exception as e:
                        print(f"    ERROR: {e}")
        
        # Clean empty directories
        if not dry_run:
            removed_dirs = self.clean_empty_directories()
            if removed_dirs:
                print(f"\nRemoved {len(removed_dirs)} empty directories")
        
        print(f"\nTotal space {'to be freed' if dry_run else 'freed'}: {total_size/1024/1024:.2f}MB")
        
        if dry_run:
            print("\nRun with --execute to perform cleanup")
        else:
            self.save_cleanup_log()
    
    def save_cleanup_log(self):
        """Save cleanup log"""
        log_file = ".cleanup/cleanup_history.json"
        
        history = []
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                history = json.load(f)
        
        history.append({
            'timestamp': datetime.now().isoformat(),
            'files_removed': len(self.cleanup_log),
            'details': self.cleanup_log
        })
        
        # Keep only last 10 cleanup sessions
        history = history[-10:]
        
        with open(log_file, 'w') as f:
            json.dump(history, f, indent=2)

if __name__ == "__main__":
    import sys
    
    cleaner = ProjectCleaner()
    dry_run = "--execute" not in sys.argv
    cleaner.run_cleanup(dry_run=dry_run)