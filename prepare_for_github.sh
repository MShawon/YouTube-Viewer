#!/bin/bash

# YouTube Viewer - GitHub Preparation Script
# This script prepares the project for GitHub publishing

set -e

echo "🎬 YouTube Viewer - GitHub Preparation Script"
echo "=============================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the right directory
if [ ! -f "youtube_viewer.py" ]; then
    print_error "This script must be run from the YouTube-Viewer directory"
    exit 1
fi

print_status "Checking project structure..."

# Clean up sensitive files and directories
print_status "Cleaning up sensitive files..."

# Remove sensitive config files
[ -f "config.json" ] && rm -f "config.json" && print_warning "Removed config.json (contains sensitive data)"
[ -f "database.db" ] && rm -f "database.db" && print_warning "Removed database.db"
[ -f "database_backup.db" ] && rm -f "database_backup.db" && print_warning "Removed database_backup.db"
[ -f "version.txt" ] && rm -f "version.txt" && print_warning "Removed version.txt"

# Remove driver files
[ -f "chromedriver" ] && rm -f "chromedriver" && print_warning "Removed chromedriver binary"
[ -f "chromedriver.exe" ] && rm -f "chromedriver.exe" && print_warning "Removed chromedriver.exe"
[ -d "patched_drivers" ] && rm -rf "patched_drivers" && print_warning "Removed patched_drivers directory"

# Clean up virtual environments
[ -d ".venv" ] && rm -rf ".venv" && print_warning "Removed .venv directory"
[ -d ".venv311" ] && rm -rf ".venv311" && print_warning "Removed .venv311 directory"

# Clean up Python cache
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -delete 2>/dev/null || true
find . -name "*.pyo" -delete 2>/dev/null || true
find . -name "*.pyd" -delete 2>/dev/null || true
find . -name ".coverage" -delete 2>/dev/null || true
find . -name "coverage.xml" -delete 2>/dev/null || true
find . -name "*.cover" -delete 2>/dev/null || true
find . -name "*.log" -delete 2>/dev/null || true

print_success "Cleanup completed"

# Create example configuration files
print_status "Creating example configuration files..."

# Create example urls.txt if it doesn't exist or is empty
if [ ! -s "urls.txt" ]; then
    cat > urls.txt << 'EOF'
# Add your YouTube video URLs here (one per line)
# Examples:
# https://www.youtube.com/watch?v=dQw4w9WgXcQ
# https://www.youtube.com/watch?v=jNQXAC9IVRw
# https://music.youtube.com/watch?v=dQw4w9WgXcQ

# For external traffic simulation, you can also use redirect URLs:
# https://t.co/shortened_link
# https://bit.ly/shortened_link
EOF
    print_success "Created example urls.txt"
fi

# Create example search.txt if it doesn't exist or is empty
if [ ! -s "search.txt" ]; then
    cat > search.txt << 'EOF'
# Add your search queries and video titles here
# Format: search_keyword :::: exact_video_title
# Examples:
# python tutorial :::: Learn Python in 2025
# music video :::: Best Songs of 2025
# gaming :::: Epic Gaming Moments
# tech review :::: iPhone 15 Review
# cooking :::: Easy Pasta Recipe
# travel vlog :::: Amazing Places to Visit

# You can also use video IDs instead of titles:
# search_keyword :::: VIDEO_ID_HERE
EOF
    print_success "Created example search.txt"
fi

# Update README if the updated version exists
if [ -f "README_UPDATED.md" ]; then
    mv "README_UPDATED.md" "README.md"
    print_success "Updated README.md with latest version"
fi

# Use updated requirements if available
if [ -f "requirements-updated.txt" ]; then
    cp "requirements-updated.txt" "requirements.txt"
    print_success "Updated requirements.txt with latest dependencies"
fi

# Check Git status
print_status "Checking Git status..."

# Initialize git if not already initialized
if [ ! -d ".git" ]; then
    git init
    print_success "Initialized Git repository"
fi

# Add all files to git
git add .

# Show git status
echo ""
print_status "Git status:"
git status

echo ""
print_status "Project preparation completed!"
echo ""
echo -e "${GREEN}✅ Next steps:${NC}"
echo "1. Review the changes: git diff --cached"
echo "2. Commit your changes: git commit -m 'feat: update for modern Chrome compatibility'"
echo "3. Add your GitHub repository: git remote add origin https://github.com/yourusername/YouTube-Viewer.git"
echo "4. Push to GitHub: git push -u origin master"
echo ""
echo -e "${YELLOW}📝 Don't forget to:${NC}"
echo "• Update the repository URL in setup.py and README.md"
echo "• Add your actual email in setup.py"
echo "• Configure GitHub repository settings"
echo "• Add repository secrets if needed for CI/CD"
echo ""
echo -e "${BLUE}🎉 Your YouTube Viewer project is ready for GitHub!${NC}"
