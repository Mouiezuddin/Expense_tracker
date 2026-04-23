# 📁 Project Structure

## Clean and Organized File Structure

All files are now consolidated in the `expense_tracker` directory.

---

## 📂 Directory Layout

```
expense_tracker/                         # Main project directory
│
├── 📄 manage.py                         # Django management script
├── 📄 setup.py                          # Automated setup script
├── 📄 requirements.txt                  # Python dependencies
├── 📄 db.sqlite3                        # Database (created after setup)
│
├── 📚 Documentation Files
│   ├── README.md                        # Main project documentation
│   ├── INSTALLATION.md                  # Detailed setup guide
│   ├── EXAM_QA.md                       # Exam questions & answers
│   ├── GITHUB_SETUP.md                  # Git commands reference
│   ├── GITHUB_UPLOAD_INSTRUCTIONS.md    # Upload guide
│   ├── QUICK_START.md                   # Quick reference
│   ├── UPLOAD_SUCCESS.md                # Upload confirmation
│   ├── LICENSE                          # MIT License
│   ├── MANIFEST.in                      # Package manifest
│   └── .gitignore                       # Git ignore rules
│
├── 📁 expense_tracker/                  # Django project settings
│   ├── __init__.py
│   ├── settings.py                      # Project settings
│   ├── urls.py                          # Main URL configuration
│   ├── wsgi.py                          # WSGI configuration
│   └── asgi.py                          # ASGI configuration
│
└── 📁 tracker/                          # Main application
    │
    ├── 📄 Python Files
    │   ├── __init__.py
    │   ├── models.py                    # Database models
    │   ├── views.py                     # View functions
    │   ├── forms.py                     # Form classes
    │   ├── urls.py                      # App URL routing
    │   ├── admin.py                     # Admin configuration
    │   ├── apps.py                      # App configuration
    │   └── tests.py                     # Test cases
    │
    ├── 📁 migrations/                   # Database migrations
    │   ├── __init__.py
    │   ├── 0001_initial.py              # Initial migration
    │   └── 0002_userprofile.py          # UserProfile migration
    │
    ├── 📁 static/                       # Static files
    │   └── tracker/
    │       └── css/
    │           └── style.css            # Custom 3D neumorphic CSS
    │
    └── 📁 templates/                    # HTML templates
        ├── registration/
        │   ├── login.html               # Login page
        │   └── register.html            # Registration page
        └── tracker/
            ├── base.html                # Base template
            ├── dashboard.html           # Dashboard
            ├── add_expense.html         # Add/Edit expense
            ├── expense_list.html        # Expense list
            └── profile.html             # User profile
```

---

## 📊 File Count

- **Total Files:** 60+
- **Python Files:** 15+
- **HTML Templates:** 7
- **CSS Files:** 1
- **Documentation:** 9
- **Configuration:** 5+

---

## 🎯 Key Files Explained

### Core Files
- **manage.py** - Django's command-line utility
- **setup.py** - One-command automated setup
- **requirements.txt** - Django 4.2.11, ReportLab 4.1.0

### Models (models.py)
- `UserProfile` - User budget information
- `Expense` - Expense records
- `Category` - Expense categories (TextChoices)

### Views (views.py)
- `dashboard` - Main dashboard with analytics
- `add_expense` - Add new expense
- `edit_expense` - Edit existing expense
- `expense_list` - List and filter expenses
- `profile` - User profile and budget
- `generate_pdf` - PDF report generation
- `register_view` - User registration
- `login_view` - User login
- `logout_view` - User logout

### Forms (forms.py)
- `RegisterForm` - User registration
- `ExpenseForm` - Add/edit expenses
- `FilterForm` - Filter expenses
- `ProfileForm` - Update profile
- `BudgetForm` - Set budget

### Templates
- **base.html** - Main layout with sidebar
- **dashboard.html** - Dashboard with charts
- **add_expense.html** - Expense form
- **expense_list.html** - Expense table
- **profile.html** - User profile
- **login.html** - Login form
- **register.html** - Registration form

### Static Files
- **style.css** - 3D neumorphic design with:
  - Custom color palette
  - Raised cards with shadows
  - Inset form inputs
  - Gradient buttons
  - Smooth animations

---

## 🚀 Quick Access

### Run Project
```bash
cd expense_tracker
python setup.py
.venv\Scripts\activate  # Windows
python manage.py runserver
```

### Documentation
- Main docs: `README.md`
- Setup guide: `INSTALLATION.md`
- Exam prep: `EXAM_QA.md`
- Quick ref: `QUICK_START.md`

### Development
- Models: `tracker/models.py`
- Views: `tracker/views.py`
- Forms: `tracker/forms.py`
- URLs: `tracker/urls.py`
- Templates: `tracker/templates/`
- CSS: `tracker/static/tracker/css/style.css`

---

## 📝 Notes

- All documentation is in the root of `expense_tracker/`
- No duplicate files
- Clean and organized structure
- Easy to navigate
- Ready for development and deployment

---

**Last Updated:** After cleanup and consolidation
**Status:** ✅ Clean and organized
