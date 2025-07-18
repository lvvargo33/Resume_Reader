#!/usr/bin/env python3
"""
Automated GitHub Resume Collection Manager
Monitors current collection and starts the next batch automatically
"""

import os
import sys
import time
import json
import subprocess
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('auto_collection.log')
    ]
)
logger = logging.getLogger(__name__)

def check_collection_status():
    """Check if current collection is complete"""
    # Check for batch files in resume_collections
    try:
        files = [f for f in os.listdir('resume_collections') 
                if f.startswith('batch_') and f.endswith('.json') 
                and 'partial' not in f]
        
        total_collected = 0
        for file in files:
            with open(os.path.join('resume_collections', file), 'r') as f:
                data = json.load(f)
                count = data.get('metadata', {}).get('count', 0)
                total_collected += count
                logger.info(f"Found {count} resumes in {file}")
        
        return total_collected
    except Exception as e:
        logger.error(f"Error checking collection status: {e}")
        return 0

def is_collection_running():
    """Check if collection process is still running"""
    try:
        # Check if python process with production_collector.py is running
        result = subprocess.run(['pgrep', '-f', 'production_collector.py'], 
                              capture_output=True, text=True)
        return result.returncode == 0
    except:
        return False

def wait_for_current_collection():
    """Wait for current collection to complete"""
    logger.info("Monitoring current collection progress...")
    
    last_checkpoint_time = None
    stale_threshold = 300  # 5 minutes without update
    
    while True:
        try:
            # Check if collection is still running
            if not is_collection_running():
                logger.info("Collection process has stopped")
                break
            
            # Check checkpoint file
            if os.path.exists('collection_checkpoint.json'):
                checkpoint_mtime = os.path.getmtime('collection_checkpoint.json')
                
                with open('collection_checkpoint.json', 'r') as f:
                    checkpoint = json.load(f)
                    current_count = checkpoint.get('resumes_collected', 0)
                    
                logger.info(f"Current progress: {current_count} resumes collected")
                
                # Check if checkpoint is stale
                if last_checkpoint_time and (time.time() - checkpoint_mtime) > stale_threshold:
                    logger.warning("Checkpoint hasn't updated in 5 minutes, collection may have stopped")
                    break
                
                last_checkpoint_time = checkpoint_mtime
                
                # Check if we've reached target
                if current_count >= 2000:
                    logger.info("Current collection target reached!")
                    time.sleep(10)  # Wait for final save
                    break
            
            time.sleep(30)  # Check every 30 seconds
            
        except Exception as e:
            logger.error(f"Error monitoring collection: {e}")
            time.sleep(30)

def start_next_collection(target_count):
    """Start the next collection batch"""
    logger.info(f"Starting new collection for {target_count} resumes...")
    
    # Set environment variable
    env = os.environ.copy()
    if 'GITHUB_TOKEN' not in env:
        raise ValueError("GITHUB_TOKEN environment variable not set!")
    
    # Start collection in background
    process = subprocess.Popen(
        ['python3', 'production_collector.py', str(target_count)],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    logger.info(f"Started collection process with PID: {process.pid}")
    return process

def main():
    logger.info("=== Auto Collection Manager Started ===")
    
    # Wait for current collection to complete
    wait_for_current_collection()
    
    # Check total collected so far
    total_collected = check_collection_status()
    logger.info(f"Total resumes collected so far: {total_collected}")
    
    # Calculate how many more we need
    target_total = 5000
    remaining = target_total - total_collected
    
    if remaining <= 0:
        logger.info("Target of 5000 resumes already reached!")
        return
    
    # Start next collection
    logger.info(f"Need {remaining} more resumes to reach target of {target_total}")
    
    # Clear old checkpoint to start fresh
    if os.path.exists('collection_checkpoint.json'):
        os.rename('collection_checkpoint.json', 
                 f'collection_checkpoint_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json')
    
    # Start collection for remaining resumes (max 3000 as requested)
    next_batch_size = min(remaining, 3000)
    process = start_next_collection(next_batch_size)
    
    # Monitor the new collection
    logger.info("Monitoring new collection...")
    while True:
        try:
            # Check if process is still running
            if process.poll() is not None:
                logger.info("Collection process completed")
                break
            
            # Check progress
            if os.path.exists('collection_checkpoint.json'):
                with open('collection_checkpoint.json', 'r') as f:
                    checkpoint = json.load(f)
                    current = checkpoint.get('resumes_collected', 0)
                    logger.info(f"Progress: {current}/{next_batch_size} resumes")
            
            time.sleep(60)  # Check every minute
            
        except KeyboardInterrupt:
            logger.info("Monitoring stopped by user")
            break
        except Exception as e:
            logger.error(f"Error during monitoring: {e}")
            time.sleep(60)
    
    # Final summary
    final_total = check_collection_status()
    logger.info(f"\n=== Final Summary ===")
    logger.info(f"Total resumes collected: {final_total}")
    logger.info(f"Target was: {target_total}")
    
    if final_total >= target_total:
        logger.info("✅ Target reached successfully!")
    else:
        logger.info(f"📊 Still need {target_total - final_total} more resumes")

if __name__ == "__main__":
    main()