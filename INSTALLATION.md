# Spendwise - Installation Guide

Complete installation instructions for setting up Spendwise Expense Tracker.

---

## Method 1: Automated Setup (Recommended)

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Steps

1. **Clone or download the repository**
```bash
git clone https://github.com/YOUR_USERNAME/spendwise-expense-tracker.git
cd spendwise-expense-tracker/expense_tracker
```

2. **Run the automated setup script**
```bash
python setup.py
```

This will automatically:
- ✅ Create a virtual environment
- ✅ Install Django and ReportLab
- ✅ Run database migrations
- ✅ Set up the project structure

3. **Activate the virtual environment**

**Windows:**
```bash
.venv\Scripts\activate
```

**macOS/Linux:**
```bash
source .venv/bin/activate
```

4. **Create a superuser (optional)**
```bash
python manage.py createsuperuser
```

5. **Start the development server**
```bash
python manage.py runserver
```

6. **Open your browser**
```
http://127.0.0.1:8000
```

---

## Method 2: Manual Setup

### Step 1: Create Virtual Environment

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install Django==4.2.11 reportlab==4.1.0
```

### Step 3: Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 4: Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### Step 5: Start Server

```bash
python manage.py runserver
```

---

## What Gets Installed

### Python Packages
- **Django 4.2.11** - Web framework
- **ReportLab 4.1.0** - PDF generation library

### Project Structure
```
expense_tracker/
├── manage.py                    # Django management script
├── db.sqlite3                   # Database (created after migration)
├── requirements.txt             # Python dependencies
├── setup.py                     # Automated setup script
├── expense_tracker/             # Project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── tracker/                     # Main application
    ├── models.py                # Database models
    ├── views.py                 # View functions
    ├── forms.py                 # Form classes
    ├── urls.py                  # URL routing
    ├── admin.py                 # Admin configuration
    ├── static/                  # Static files (CSS, JS)
    │   └── tracker/
    │       └── css/
    │           └── style.css    # Main stylesheet
    ├── templates/               # HTML templates
    │   ├── registration/
    │   │   ├── login.html
    │   │   └── register.html
    │   └── tracker/
    │       ├── base.html
    │       ├── dashboard.html
    │       ├── add_expense.html
    │       ├── expense_list.html
    │       └── profile.html
    └── migrations/              # Database migrations
```

---

## Verification

After installation, verify everything works:

### 1. Check Django Installation
```bash
python -m django --version
```
Should output: `4.2.11`

### 2. Check Database
```bash
python manage.py showmigrations
```
All migrations should show `[X]` (applied)

### 3. Check Static Files
Navigate to `tracker/static/tracker/css/` and verify `style.css` exists

### 4. Access Admin Panel
1. Start server: `python manage.py runserver`
2. Go to: `http://127.0.0.1:8000/admin/`
3. Login with superuser credentials

---

## Troubleshooting

### Issue: "No module named 'django'"
**Solution:** Activate virtual environment first
```bash
# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

### Issue: "Table doesn't exist"
**Solution:** Run migrations
```bash
python manage.py migrate
```

### Issue: "Static files not loading"
**Solution:** Check DEBUG setting in settings.py
```python
DEBUG = True  # Should be True for development
```

### Issue: "Port already in use"
**Solution:** Use a different port
```bash
python manage.py runserver 8080
```

### Issue: "Permission denied" on setup.py
**Solution:** Run with python explicitly
```bash
python setup.py
```

---

## Default Credentials

After running setup, you can:
- **Register** a new account at `/register/`
- **Login** at `/login/`
- **Access admin** at `/admin/` (if superuser created)

---

## Features Included

✅ User authentication (register, login, logout)
✅ Expense management (add, edit, delete)
✅ Budget tracking
✅ Dashboard with analytics
✅ Category-based filtering
✅ Monthly spending charts (Chart.js)
✅ PDF report generation (ReportLab)
✅ Responsive design (Bootstrap 5)
✅ Custom 3D neumorphic UI

---

## Production Deployment

For production deployment, additional steps are needed:

1. Set `DEBUG = False` in settings.py
2. Configure `ALLOWED_HOSTS`
3. Use PostgreSQL instead of SQLite
4. Set up static file serving
5. Configure HTTPS
6. Use environment variables for secrets

See Django deployment documentation for details.

---

## Support

If you encounter issues:
1. Check the troubleshooting section above
2. Verify Python version: `python --version` (3.8+)
3. Ensure virtual environment is activated
4. Check Django documentation: https://docs.djangoproject.com/

---

## Quick Reference

```bash
# Activate virtual environment
.venv\Scripts\activate          # Windows
source .venv/bin/activate       # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Database operations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver

# Access application
http://127.0.0.1:8000

# Access admin panel
http://127.0.0.1:8000/admin/
```
