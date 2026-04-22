# 💰 Spendwise — Smart Expense Tracker

A modern, feature-rich personal expense tracking web application built with Django. Track your spending, set budgets, visualize trends, and generate professional PDF reports — all with a beautiful 3D neumorphic UI.

![Django](https://img.shields.io/badge/Django-4.2-green)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## ✨ Features

- 🔐 **User Authentication** — Secure registration, login, and logout
- 💵 **Budget Management** — Set your total budget and track remaining balance
- 📊 **Dashboard Analytics** — Visual insights with Chart.js
- 📝 **Expense CRUD** — Add, edit, delete expenses with categories
- 🎯 **Smart Insights** — Auto-generated spending tips and warnings
- 📈 **Charts & Graphs** — Monthly trends and category breakdowns
- 🔍 **Advanced Filtering** — Filter by category, date range
- 📄 **PDF Reports** — Download professional expense reports
- 📱 **Responsive Design** — Works on desktop, tablet, and mobile
- 🎨 **Modern UI** — 3D neumorphic design with smooth animations

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/spendwise-expense-tracker.git

# Navigate to project
cd spendwise-expense-tracker/expense_tracker

# Run automated setup (creates venv, installs dependencies, runs migrations)
python setup.py

# Activate virtual environment
.venv\Scripts\activate          # Windows
source .venv/bin/activate       # Mac/Linux

# Start development server
python manage.py runserver

# Open browser at http://127.0.0.1:8000
```

That's it! The automated setup handles everything. 🎉

---

## 📸 Screenshots

### Dashboard
- Budget overview with 3 main cards (Total Money, Spent Amount, Remaining Balance)
- Monthly spending trend chart
- Category breakdown donut chart
- Smart insights and recent transactions

### Expense Management
- Add/Edit expenses with categories
- Filter by category and date range
- Bulk view with edit/delete actions

### Profile & Budget
- Update personal information
- Set and manage budget
- View spending statistics

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| **Backend** | Python 3, Django 4.2 |
| **Database** | SQLite3 (development) |
| **Frontend** | Bootstrap 5, DM Sans Font |
| **Charts** | Chart.js 4.4 |
| **PDF** | ReportLab 4.1 |
| **Icons** | Bootstrap Icons 1.11 |

---

## 📁 Project Structure

```
expense_tracker/
├── manage.py                    # Django management script
├── setup.py                     # Automated setup script
├── requirements.txt             # Python dependencies
├── db.sqlite3                   # Database (created after setup)
├── expense_tracker/             # Project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── tracker/                     # Main application
    ├── models.py                # Database models (Expense, UserProfile, Category)
    ├── views.py                 # View functions
    ├── forms.py                 # Form classes
    ├── urls.py                  # URL routing
    ├── admin.py                 # Admin configuration
    ├── static/                  # Static files
    │   └── tracker/
    │       └── css/
    │           └── style.css    # Custom 3D neumorphic styles
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

## 🎯 Key Features Explained

### Budget Tracking
Set your total budget in the profile page. The dashboard displays:
- **Total Money** — Your available budget
- **Spent Amount** — All-time expenses
- **Remaining Balance** — Budget minus expenses (with warnings if over budget)

### Smart Insights
Auto-generated tips based on your spending:
- Highest spending category
- Week-over-week comparison
- Budget warnings and alerts
- Average daily spending

### Category System
7 predefined categories with color coding:
- 🍽️ Food & Dining
- ✈️ Travel & Transport
- ⚡ Bills & Utilities
- 🛍️ Shopping
- 💊 Health & Medical
- 🎬 Entertainment
- 📌 Others

### PDF Reports
Download professional PDF reports with:
- Budget summary cards
- Category breakdown table
- Complete transaction list
- Respects active filters

---

## 📚 Documentation

- **[Installation Guide](../INSTALLATION.md)** — Detailed setup instructions
- **[GitHub Setup](../GITHUB_SETUP.md)** — How to upload to GitHub
- **[Exam Q&A](../EXAM_QA.md)** — Complete exam preparation guide

---

## 🔧 Development

### Manual Setup (Alternative)

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
.venv\Scripts\activate          # Windows
source .venv/bin/activate       # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Start server
python manage.py runserver
```

### Useful Commands

```bash
# Create superuser for admin access
python manage.py createsuperuser

# Access admin panel
http://127.0.0.1:8000/admin/

# Run on different port
python manage.py runserver 8080

# Make new migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Check for issues
python manage.py check
```

---

## 🎨 Design System

### Color Palette
- **Primary:** `#6366f1` (Indigo)
- **Success:** `#10b981` (Green)
- **Warning:** `#f59e0b` (Amber)
- **Danger:** `#ef4444` (Red)
- **Background:** `#eef0f8` (Light Gray)
- **Surface:** `#f4f5fb` (White)

### Typography
- **Font:** DM Sans (Google Fonts)
- **Weights:** 300, 400, 500, 600, 700, 800

### UI Style
- 3D Neumorphic design
- Raised cards with shadows
- Inset form inputs
- Gradient buttons with glow effects
- Smooth animations and transitions

---

## 🔒 Security Features

- ✅ CSRF protection on all forms
- ✅ User authentication required for protected views
- ✅ Password hashing (Django's built-in auth)
- ✅ SQL injection prevention (Django ORM)
- ✅ User data isolation (per-user filtering)
- ✅ XSS protection (Django template escaping)

---

## 🚀 Deployment

For production deployment:

1. Set `DEBUG = False` in settings.py
2. Configure `ALLOWED_HOSTS` with your domain
3. Change `SECRET_KEY` to a secure random value
4. Use PostgreSQL instead of SQLite
5. Set up static file serving (WhiteNoise or CDN)
6. Configure HTTPS
7. Use environment variables for secrets
8. Set up proper logging

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.

---

## 👨‍💻 Author

Created with ❤️ for personal finance management

---

## 🙏 Acknowledgments

- Django framework for the robust backend
- Bootstrap for responsive design
- Chart.js for beautiful visualizations
- ReportLab for PDF generation
- DM Sans font by Google Fonts

---

## 📞 Support

If you encounter any issues:
1. Check the [Installation Guide](../INSTALLATION.md)
2. Review the [Troubleshooting section](../INSTALLATION.md#troubleshooting)
3. Open an issue on GitHub

---

## 🎓 Educational Use

This project is perfect for:
- Learning Django web development
- Understanding MVC/MVT architecture
- Practicing database relationships
- Studying user authentication
- Learning PDF generation
- Understanding data visualization

---

## ⭐ Star This Repository

If you find this project helpful, please give it a star! ⭐

---

**Happy Expense Tracking! 💰📊**
