#!/usr/bin/env python3
"""
Monitor GitHub resume collection progress
"""

import time
import os
import json
from datetime import datetime, timedelta

def monitor_collection():
    print("\n=== GitHub Resume Collection Monitor ===")
    print("Press Ctrl+C to stop monitoring\n")
    
    last_count = 0
    
    while True:
        try:
            # Check for checkpoint file
            if os.path.exists('collection_checkpoint.json'):
                with open('collection_checkpoint.json', 'r') as f:
                    checkpoint = json.load(f)
                    
                count = checkpoint.get('resumes_collected', 0)
                last_updated = checkpoint.get('last_updated', 'Unknown')
                
                if count != last_count:
                    print(f"\r[{datetime.now().strftime('%H:%M:%S')}] "
                          f"Progress: {count}/2000 ({count/2000*100:.1f}%) "
                          f"| Last update: {last_updated}", end='', flush=True)
                    last_count = count
                    
                    # Check if collection is complete
                    if count >= 2000:
                        print("\n\n✅ Collection Complete!")
                        break
            
            # Also check for final output files
            files = [f for f in os.listdir('resume_collections') 
                    if f.startswith('batch_') and f.endswith('.json') 
                    and 'partial' not in f]
            
            if files:
                latest_file = sorted(files)[-1]
                file_path = os.path.join('resume_collections', latest_file)
                
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    final_count = data.get('metadata', {}).get('count', 0)
                    
                if final_count >= 2000:
                    print(f"\n\n✅ Collection Complete! Final file: {latest_file}")
                    print(f"Total resumes: {final_count}")
                    break
            
            time.sleep(5)  # Check every 5 seconds
            
        except KeyboardInterrupt:
            print("\n\nMonitoring stopped.")
            break
        except Exception as e:
            print(f"\nError: {e}")
            time.sleep(5)

if __name__ == "__main__":
    monitor_collection()