# Resume Reader - Quick Start Guide

## 🚀 Resuming Work

1. **Check Project Status**
   ```bash
   cat PROJECT_STATUS.md
   ```

2. **Review Last Session**
   ```bash
   cat SESSION_LOG.md
   ```

3. **Continue Where You Left Off**
   - Check "Next Steps" in SESSION_LOG.md
   - Review "Active Tasks" in PROJECT_STATUS.md

## 🧹 File Cleanup

### Run Cleanup (Dry Run)
```bash
python .cleanup/cleanup.py
```

### Execute Cleanup
```bash
python .cleanup/cleanup.py --execute
```

### Customize Cleanup Rules
Edit `.cleanup/cleanup_rules.json` to:
- Add new file patterns
- Adjust retention periods
- Protect important paths

## 📝 Session Documentation

### Automatic Documentation (Git Hooks)
Session logs now update automatically when you commit!

1. **Install hooks** (one time):
   ```bash
   ./.githooks/install-hooks.sh
   ```

2. **Make commits** - Fill in the template that appears:
   - What was done
   - Key decisions
   - Next steps
   - Technical notes

3. **SESSION_LOG.md** updates automatically after commit

### Manual Documentation
If needed, you can still manually update:
- SESSION_LOG.md - Detailed session history
- PROJECT_STATUS.md - Current state dashboard

## 🏗️ Architecture Commands (SuperClaude)

### System Design
```bash
/design --think-hard --persona-architect
```

### Technical Analysis
```bash
/analyze --scope project --think
```

### Build Planning
```bash
/build --plan
```

## 📁 Project Structure
```
Resume_Reader/
├── SESSION_LOG.md        # Detailed session history
├── PROJECT_STATUS.md     # Current project state
├── QUICKSTART.md        # This file
├── .cleanup/            # Cleanup utilities
│   ├── cleanup.py       # Cleanup script
│   └── cleanup_rules.json # Cleanup configuration
├── docs/                # Documentation (to be created)
├── src/                 # Source code (to be created)
└── tests/               # Test files (to be created)
```