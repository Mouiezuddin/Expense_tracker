# GitHub Setup Guide for Spendwise

## Step 1: Initialize Git Repository

Open your terminal in the project root directory and run:

```bash
cd expense_tracker
git init
```

## Step 2: Add All Files

```bash
git add .
```

## Step 3: Create Initial Commit

```bash
git commit -m "Initial commit: Spendwise Expense Tracker with budget management"
```

## Step 4: Create GitHub Repository

1. Go to https://github.com
2. Click the "+" icon in the top right
3. Select "New repository"
4. Name it: `spendwise-expense-tracker` (or your preferred name)
5. Add description: "Personal expense tracking web app with Django - Budget management, analytics, and PDF reports"
6. Choose Public or Private
7. **DO NOT** initialize with README, .gitignore, or license (we already have these)
8. Click "Create repository"

## Step 5: Connect Local Repository to GitHub

Replace `YOUR_USERNAME` with your actual GitHub username:

```bash
git remote add origin https://github.com/YOUR_USERNAME/spendwise-expense-tracker.git
```

## Step 6: Push to GitHub

```bash
git branch -M main
git push -u origin main
```

## Step 7: Verify Upload

Go to your GitHub repository URL and verify all files are uploaded.

---

## Alternative: Using GitHub Desktop

1. Download and install GitHub Desktop from https://desktop.github.com/
2. Open GitHub Desktop
3. Click "File" → "Add Local Repository"
4. Browse to your `expense_tracker` folder
5. Click "Publish repository"
6. Choose repository name and visibility
7. Click "Publish Repository"

---

## What Gets Uploaded

✅ All Python files (models, views, forms, urls)
✅ All templates (HTML files)
✅ All static files (CSS)
✅ Configuration files (settings.py, urls.py)
✅ README.md
✅ requirements.txt
✅ .gitignore

❌ Virtual environment (venv/)
❌ Database file (db.sqlite3)
❌ Python cache (__pycache__/)
❌ IDE settings (.vscode/)

---

## Troubleshooting

### Error: "remote origin already exists"
```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/spendwise-expense-tracker.git
```

### Error: "failed to push some refs"
```bash
git pull origin main --rebase
git push -u origin main
```

### Want to update after making changes?
```bash
git add .
git commit -m "Description of changes"
git push
```

---

## Repository Description Suggestions

**Short Description:**
"Personal expense tracking web app with Django - Budget management, analytics, and PDF reports"

**Topics/Tags:**
- django
- python
- expense-tracker
- budget-management
- web-application
- bootstrap
- chartjs
- pdf-generation
- personal-finance

---

## README Badges (Optional)

Add these to the top of your README.md:

```markdown
![Django](https://img.shields.io/badge/Django-4.2-green)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)
```

---

## Next Steps After Upload

1. Add a LICENSE file (MIT recommended)
2. Add screenshots to README
3. Create a demo video/GIF
4. Add installation instructions
5. Document API endpoints (if any)
6. Set up GitHub Actions for CI/CD (optional)

---

## Quick Commands Reference

```bash
# Check status
git status

# Add specific file
git add filename.py

# Add all files
git add .

# Commit changes
git commit -m "Your message"

# Push to GitHub
git push

# Pull latest changes
git pull

# View commit history
git log --oneline

# Create new branch
git checkout -b feature-name

# Switch branches
git checkout main
```
