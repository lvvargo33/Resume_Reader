#!/usr/bin/env python3
"""
Progress Tracker for GitHub Resume Collection
Provides real-time monitoring and checkpoint management
"""

import json
import os
import time
from datetime import datetime, timedelta
from typing import Dict, Optional
import threading
from collections import deque


class ProgressTracker:
    def __init__(self, target_count: int, checkpoint_file: str = "collection_checkpoint.json"):
        self.target_count = target_count
        self.checkpoint_file = checkpoint_file
        self.stats_file = "collection_stats.json"
        
        # Progress metrics
        self.start_time = None
        self.resumes_collected = 0
        self.errors_encountered = 0
        self.users_processed = 0
        self.users_skipped = 0
        
        # Rate tracking
        self.recent_collections = deque(maxlen=100)  # Track last 100 collections
        self.api_calls_made = 0
        self.rate_limit_waits = 0
        
        # Session management
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.is_running = False
        
        # Real-time monitoring thread
        self.monitor_thread = None
        self.monitor_interval = 30  # seconds
    
    def start_session(self) -> None:
        """Start a new collection session"""
        self.start_time = time.time()
        self.is_running = True
        
        # Start monitoring thread
        self.monitor_thread = threading.Thread(target=self._monitor_progress)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
        
        print(f"\n=== Collection Session Started ===")
        print(f"Session ID: {self.session_id}")
        print(f"Target: {self.target_count} resumes")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 35)
    
    def update_progress(self, resumes_added: int = 0, errors: int = 0, 
                       users_processed: int = 0, users_skipped: int = 0) -> None:
        """Update collection progress"""
        self.resumes_collected += resumes_added
        self.errors_encountered += errors
        self.users_processed += users_processed
        self.users_skipped += users_skipped
        
        if resumes_added > 0:
            self.recent_collections.append(time.time())
    
    def increment_api_calls(self, count: int = 1) -> None:
        """Track API calls made"""
        self.api_calls_made += count
    
    def record_rate_limit_wait(self) -> None:
        """Record when we hit rate limits"""
        self.rate_limit_waits += 1
    
    def get_current_rate(self) -> float:
        """Calculate current collection rate (resumes/hour)"""
        if not self.recent_collections or len(self.recent_collections) < 2:
            return 0.0
        
        time_span = self.recent_collections[-1] - self.recent_collections[0]
        if time_span == 0:
            return 0.0
        
        return len(self.recent_collections) / time_span * 3600
    
    def get_estimated_completion(self) -> Optional[datetime]:
        """Estimate when collection will complete"""
        if self.resumes_collected == 0 or not self.start_time:
            return None
        
        elapsed = time.time() - self.start_time
        rate = self.resumes_collected / elapsed
        
        if rate == 0:
            return None
        
        remaining = self.target_count - self.resumes_collected
        seconds_remaining = remaining / rate
        
        return datetime.now() + timedelta(seconds=seconds_remaining)
    
    def get_efficiency_metrics(self) -> Dict:
        """Calculate efficiency metrics"""
        if self.users_processed == 0:
            return {
                'collection_efficiency': 0,
                'skip_rate': 0,
                'error_rate': 0
            }
        
        return {
            'collection_efficiency': self.resumes_collected / self.users_processed * 100,
            'skip_rate': self.users_skipped / self.users_processed * 100,
            'error_rate': self.errors_encountered / self.api_calls_made * 100 if self.api_calls_made > 0 else 0
        }
    
    def save_checkpoint(self, collected_users: set) -> None:
        """Save progress checkpoint"""
        checkpoint = {
            'session_id': self.session_id,
            'collected_users': list(collected_users),
            'resumes_collected': self.resumes_collected,
            'users_processed': self.users_processed,
            'users_skipped': self.users_skipped,
            'errors_encountered': self.errors_encountered,
            'api_calls_made': self.api_calls_made,
            'last_updated': datetime.now().isoformat(),
            'elapsed_seconds': time.time() - self.start_time if self.start_time else 0
        }
        
        with open(self.checkpoint_file, 'w') as f:
            json.dump(checkpoint, f, indent=2)
    
    def save_session_stats(self) -> None:
        """Save detailed session statistics"""
        elapsed = time.time() - self.start_time if self.start_time else 0
        efficiency = self.get_efficiency_metrics()
        
        stats = {
            'session_id': self.session_id,
            'start_time': datetime.fromtimestamp(self.start_time).isoformat() if self.start_time else None,
            'end_time': datetime.now().isoformat(),
            'duration_seconds': elapsed,
            'duration_formatted': str(timedelta(seconds=int(elapsed))),
            'target_count': self.target_count,
            'resumes_collected': self.resumes_collected,
            'completion_percentage': self.resumes_collected / self.target_count * 100,
            'users_processed': self.users_processed,
            'users_skipped': self.users_skipped,
            'errors_encountered': self.errors_encountered,
            'api_calls_made': self.api_calls_made,
            'rate_limit_waits': self.rate_limit_waits,
            'average_rate_per_hour': self.resumes_collected / elapsed * 3600 if elapsed > 0 else 0,
            'efficiency_metrics': efficiency
        }
        
        # Load existing stats if any
        existing_stats = []
        if os.path.exists(self.stats_file):
            try:
                with open(self.stats_file, 'r') as f:
                    existing_stats = json.load(f)
            except:
                pass
        
        # Append new stats
        existing_stats.append(stats)
        
        # Save updated stats
        with open(self.stats_file, 'w') as f:
            json.dump(existing_stats, f, indent=2)
    
    def print_progress(self) -> None:
        """Print current progress"""
        if not self.start_time:
            return
        
        elapsed = time.time() - self.start_time
        rate = self.resumes_collected / elapsed * 3600 if elapsed > 0 else 0
        current_rate = self.get_current_rate()
        efficiency = self.get_efficiency_metrics()
        eta = self.get_estimated_completion()
        
        print(f"\n{'=' * 50}")
        print(f"Progress Update - {datetime.now().strftime('%H:%M:%S')}")
        print(f"{'=' * 50}")
        print(f"Collected: {self.resumes_collected}/{self.target_count} "
              f"({self.resumes_collected/self.target_count*100:.1f}%)")
        print(f"Time Elapsed: {str(timedelta(seconds=int(elapsed)))}")
        print(f"Average Rate: {rate:.0f} resumes/hour")
        print(f"Current Rate: {current_rate:.0f} resumes/hour")
        print(f"ETA: {eta.strftime('%H:%M:%S') if eta else 'Unknown'}")
        print(f"\nEfficiency Metrics:")
        print(f"  - Collection Rate: {efficiency['collection_efficiency']:.1f}%")
        print(f"  - Skip Rate: {efficiency['skip_rate']:.1f}%")
        print(f"  - Error Rate: {efficiency['error_rate']:.1f}%")
        print(f"\nAPI Stats:")
        print(f"  - Total API Calls: {self.api_calls_made}")
        print(f"  - Rate Limit Waits: {self.rate_limit_waits}")
        print(f"  - Errors: {self.errors_encountered}")
        print(f"{'=' * 50}")
    
    def _monitor_progress(self) -> None:
        """Background thread to monitor progress"""
        while self.is_running:
            time.sleep(self.monitor_interval)
            if self.is_running:
                self.print_progress()
    
    def stop_session(self) -> None:
        """Stop the collection session"""
        self.is_running = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        
        # Save final stats
        self.save_session_stats()
        
        # Print final summary
        print(f"\n{'=' * 50}")
        print("Collection Session Complete!")
        print(f"{'=' * 50}")
        self.print_progress()
        print(f"\nSession stats saved to: {self.stats_file}")


class BatchManager:
    """Manages multiple collection batches and merging"""
    
    def __init__(self, collection_dir: str = "resume_collections"):
        self.collection_dir = collection_dir
        os.makedirs(collection_dir, exist_ok=True)
    
    def list_batches(self) -> list:
        """List all batch files"""
        batches = []
        for file in os.listdir(self.collection_dir):
            if file.startswith('batch_') and file.endswith('.json'):
                path = os.path.join(self.collection_dir, file)
                try:
                    with open(path, 'r') as f:
                        data = json.load(f)
                        metadata = data.get('metadata', {})
                        batches.append({
                            'filename': file,
                            'path': path,
                            'count': metadata.get('count', 0),
                            'collected_at': metadata.get('collected_at', ''),
                            'errors': metadata.get('errors', 0)
                        })
                except:
                    pass
        
        return sorted(batches, key=lambda x: x['collected_at'])
    
    def merge_batches(self, output_file: str = None) -> Dict:
        """Merge all batch files into one"""
        if not output_file:
            output_file = os.path.join(self.collection_dir, 'merged_all_resumes.json')
        
        all_resumes = []
        seen_users = set()
        total_errors = 0
        batch_count = 0
        
        batches = self.list_batches()
        
        for batch in batches:
            print(f"Processing {batch['filename']} ({batch['count']} resumes)...")
            
            with open(batch['path'], 'r') as f:
                data = json.load(f)
                resumes = data.get('resumes', [])
                metadata = data.get('metadata', {})
                total_errors += metadata.get('errors', 0)
                
                # Deduplicate
                for resume in resumes:
                    username = resume.get('github_username')
                    if username and username not in seen_users:
                        seen_users.add(username)
                        all_resumes.append(resume)
                
                batch_count += 1
        
        # Sort by some criteria (e.g., followers)
        all_resumes.sort(key=lambda x: x.get('followers', 0), reverse=True)
        
        # Save merged file
        merged_data = {
            'metadata': {
                'total_count': len(all_resumes),
                'batch_count': batch_count,
                'total_errors': total_errors,
                'merged_at': datetime.now().isoformat(),
                'source_batches': [b['filename'] for b in batches]
            },
            'resumes': all_resumes
        }
        
        with open(output_file, 'w') as f:
            json.dump(merged_data, f, indent=2)
        
        print(f"\nMerge Complete!")
        print(f"Total unique resumes: {len(all_resumes)}")
        print(f"Batches merged: {batch_count}")
        print(f"Output: {output_file}")
        
        return merged_data
    
    def get_collection_summary(self) -> None:
        """Print summary of all collections"""
        batches = self.list_batches()
        
        if not batches:
            print("No batch files found.")
            return
        
        total_resumes = sum(b['count'] for b in batches)
        total_errors = sum(b['errors'] for b in batches)
        
        print(f"\n{'=' * 60}")
        print("Collection Summary")
        print(f"{'=' * 60}")
        print(f"Total batches: {len(batches)}")
        print(f"Total resumes: {total_resumes}")
        print(f"Total errors: {total_errors}")
        print(f"\nBatch Details:")
        print(f"{'Filename':<30} {'Count':<10} {'Errors':<10} {'Date'}")
        print("-" * 60)
        
        for batch in batches:
            date = batch['collected_at'][:10] if batch['collected_at'] else 'Unknown'
            print(f"{batch['filename']:<30} {batch['count']:<10} {batch['errors']:<10} {date}")


if __name__ == "__main__":
    # Example usage
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "merge":
        # Merge batches
        manager = BatchManager()
        manager.merge_batches()
    elif len(sys.argv) > 1 and sys.argv[1] == "summary":
        # Show summary
        manager = BatchManager()
        manager.get_collection_summary()
    else:
        # Demo progress tracking
        tracker = ProgressTracker(target_count=100)
        tracker.start_session()
        
        # Simulate progress
        for i in range(10):
            time.sleep(2)
            tracker.update_progress(resumes_added=10, users_processed=15, users_skipped=5)
            tracker.increment_api_calls(20)
        
        tracker.stop_session()