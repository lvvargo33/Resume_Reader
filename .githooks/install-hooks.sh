#!/bin/bash
# Install Git hooks for automatic session logging

echo "Installing Git hooks for automatic session logging..."

# Configure Git to use our hooks directory
git config core.hooksPath .githooks

echo "✅ Git hooks installed successfully!"
echo ""
echo "How it works:"
echo "1. When you commit, a template will be added to your commit message"
echo "2. Fill in the template sections (What was done, Key decisions, etc.)"
echo "3. After commit, SESSION_LOG.md will be automatically updated"
echo ""
echo "Example commit message format:"
echo "  feat: implement user authentication"
echo "  "
echo "  ## Session Update - 2025-07-16 15:30"
echo "  ### What was done:"
echo "  - Implemented JWT authentication"
echo "  - Added login/logout endpoints"
echo "  "
echo "  ### Key decisions:"
echo "  - Use JWT instead of sessions for stateless auth"
echo "  "
echo "  ### Next steps:"
echo "  - Add password reset functionality"
echo ""
echo "To disable: git config --unset core.hooksPath"