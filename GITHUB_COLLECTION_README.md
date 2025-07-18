# GitHub Resume Collection System

A production-ready system for collecting developer resumes from GitHub at scale with built-in progress tracking, validation, and data management.

## Quick Start (5 minutes)

### 1. Set Environment Variable
```bash
export GITHUB_TOKEN=your_github_personal_access_token_here
```

### 2. Verify Token & Check Rate Limits
```bash
curl -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/rate_limit
```

You should see your rate limit status. GitHub allows 5,000 requests per hour for authenticated users.

### 3. Run Your First Collection
```bash
# Collect 100 resumes as a test
python production_collector.py 100
```

## Collection Strategies

### Option A: Large Batch Collection (Recommended)
- **Target**: 1,000-2,000 resumes in one session
- **Time**: 2-3 hours (with rate limiting)
- **Command**: `python production_collector.py 2000`
- **Output**: Single large JSON file with comprehensive data

### Option B: Incremental Collection
- **Target**: 500 resumes per session
- **Benefit**: More manageable, can stop/resume
- **Command**: `python production_collector.py 500`
- **Output**: Multiple JSON files that can be merged

## Features

### 1. **production_collector.py** - Main Collection Script
- Optimized with 0.3s delay between requests (reduced from 0.5s)
- Auto-resume from checkpoint if interrupted
- Skips incomplete profiles automatically
- Real-time progress updates every 10 resumes
- Saves checkpoint every 100 resumes
- Handles rate limiting gracefully
- Collects:
  - User profiles with bio, location, company
  - Programming skills from repositories
  - Top 5 repositories with stars/forks
  - Account age and activity metrics

### 2. **progress_tracker.py** - Progress Monitoring
- Real-time collection statistics
- Estimates completion time
- Tracks efficiency metrics
- Merge multiple batches into one file
- Commands:
  ```bash
  # Show collection summary
  python progress_tracker.py summary
  
  # Merge all batches
  python progress_tracker.py merge
  ```

### 3. **data_validator.py** - Quality Validation
- Validates data completeness
- Removes duplicates
- Generates quality reports
- Categorizes resumes (technical/semi-technical/non-technical)
- Command:
  ```bash
  python data_validator.py resume_collections/batch_YYYYMMDD_HHMMSS.json
  ```

## File Organization

```
/resume_collections/
├── batch_20250719_120000.json      # Individual collection batches
├── batch_20250719_150000.json
├── batch_partial_20250719_*.json   # Auto-saved partial results
├── merged_all_resumes.json         # Final merged dataset
└── *_validation_report.txt         # Quality reports
```

## Recommended Workflow

### Session 1: Initial Large Collection
```bash
# 1. Set token
export GITHUB_TOKEN=your_token_here

# 2. Start collection (2000 resumes)
python production_collector.py 2000

# 3. Monitor progress (automatic every 30 seconds)
# Watch for rate limits and adjust if needed
```

### Session 2: Additional Collection
```bash
# 1. Continue collecting more resumes
python production_collector.py 1000

# 2. Check what we have so far
python progress_tracker.py summary
```

### Session 3: Final Processing
```bash
# 1. Merge all batches
python progress_tracker.py merge

# 2. Validate the merged dataset
python data_validator.py resume_collections/merged_all_resumes.json

# 3. Review the validation report
cat resume_collections/merged_all_resumes_validation_report.txt
```

## Search Query Optimization

The collector uses diverse search queries to ensure a good mix:
- **Technical**: "software engineer python", "backend developer java"
- **Semi-technical**: "technical writer", "product manager"
- **Geographic**: Multiple cities/countries for diversity
- **Experience levels**: "junior developer", "senior engineer"
- **Specific skills**: "react native", "machine learning"

## Success Metrics

Target for 5,000 resumes:
- ✓ 40% non-technical professionals
- ✓ 30% semi-technical roles
- ✓ 30% core technical developers
- ✓ Geographic diversity across continents
- ✓ Rich skills data with technology stacks
- ✓ Clean, validated, deduplicated dataset

## Troubleshooting

### Rate Limit Issues
If you hit rate limits:
1. The script will automatically wait
2. Check your limits: `curl -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/rate_limit`
3. Consider reducing collection rate or using multiple tokens

### Resuming After Interruption
The collector automatically saves progress:
1. Just run the same command again
2. It will resume from the last checkpoint
3. No duplicate collection will occur

### Memory Issues with Large Collections
For very large collections (>5000):
1. Use incremental collection approach
2. Process in smaller batches
3. Merge using `progress_tracker.py merge`

## Advanced Usage

### Custom Search Queries
Edit the `search_queries` list in `production_collector.py` to target specific:
- Technologies
- Locations
- Experience levels
- Job titles

### Adjusting Collection Speed
In `production_collector.py`:
```python
self.min_delay = 0.3  # Reduce for faster (careful with rate limits!)
self.max_results_per_page = 100  # Maximum allowed by GitHub
self.batch_save_interval = 100  # Save progress frequency
```

### Export Options
The data is saved as JSON for maximum flexibility. You can easily convert to:
- CSV for spreadsheet analysis
- Database for advanced queries
- Parquet for big data processing

## Next Steps

After collecting your dataset:
1. Use the Resume Parser to extract detailed information
2. Build analytics dashboards
3. Create ML models for resume matching
4. Develop recommendation systems

Happy collecting! 🚀