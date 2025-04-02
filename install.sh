#!/bin/bash
# Install Claude Workflow Framework into your project
#
# NOTE: The recommended installation method is using pip:
#   pip install claude-workflow
#
# This script is provided for users who prefer a direct file copy approach
# without installing the Python package.
#
# Check if target directory is specified
if [ $# -eq 0 ]; then
  echo "Usage: ./install.sh /path/to/your/project"
  exit 1
fi

TARGET_DIR="$1"

# Check if target directory exists
if [ ! -d "$TARGET_DIR" ]; then
  echo "Target directory does not exist: $TARGET_DIR"
  exit 1
fi

# Check if target directory is a git repository
if [ ! -d "$TARGET_DIR/.git" ]; then
  echo "Warning: Target directory does not appear to be a git repository."
  read -p "Continue anyway? (y/n): " CONFIRM
  if [ "$CONFIRM" != "y" ]; then
    exit 1
  fi
fi

# Copy framework files
echo "Installing Claude Workflow Framework to $TARGET_DIR..."

# Create planning directory and subdirectories
mkdir -p "$TARGET_DIR/planning/templates"

# Copy files
cp -f CLAUDE.md "$TARGET_DIR/"
cp -f claude_workflow/new_project.py "$TARGET_DIR/planning/"
chmod +x "$TARGET_DIR/planning/new_project.py"
cp -f claude_workflow/templates/* "$TARGET_DIR/planning/templates/"

echo "Installation complete!"
echo ""
echo "Next steps:"
echo "1. Edit $TARGET_DIR/CLAUDE.md with your specific project details"
echo "2. Create a feature branch: git checkout -b feature/your-feature"
echo "3. Run the project script: python planning/new_project.py"
echo ""
echo "Refer to README.md for full documentation."