# Git Hooks for Automatic Session Logging

This directory contains Git hooks that automatically update your session documentation when you commit code.

## Installation

```bash
# Run from project root
./.githooks/install-hooks.sh
```

## How It Works

### 1. **prepare-commit-msg** Hook
- Adds a session update template to your commit message
- You fill in what was done, decisions made, and next steps

### 2. **post-commit** Hook
- Extracts information from your commit message
- Updates SESSION_LOG.md with a new session entry
- Updates PROJECT_STATUS.md with recent commit info

## Commit Message Format

When you run `git commit`, you'll see a template like this:

```
feat: your commit message here

## Session Update - 2025-07-16 15:30
### What was done:
- [Fill in what you accomplished]

### Key decisions:
- [Document important decisions]

### Next steps:
- [List what needs to be done next]

### Technical notes:
- [Any technical details worth noting]
```

## Features

- **Automatic session numbering** - Sessions are numbered sequentially
- **File tracking** - Lists which files were modified in each commit
- **Next steps tracking** - Creates checkboxes for future tasks
- **Non-intrusive** - Won't interfere with merge commits or CI/CD

## Customization

Edit the hook files to customize:
- Template format in `prepare-commit-msg`
- Session log format in `post-commit`
- Which sections to track

## Disable/Enable

```bash
# Disable hooks
git config --unset core.hooksPath

# Re-enable hooks
git config core.hooksPath .githooks
```

## Tips

1. **Keep entries concise** - Bullet points work best
2. **Focus on decisions** - Document WHY not just WHAT
3. **Update next steps** - Helps you resume work quickly
4. **Use conventional commits** - feat:, fix:, docs:, etc.