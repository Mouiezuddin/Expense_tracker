# 💰 Spendwise — Smart Expense Tracker

A clean, professional Django web application for tracking personal expenses.
Built with Django 4.2, Bootstrap 5, Chart.js, and DM Sans typography.

---

## 🚀 Quick Start

### 1. Clone / Download the project
```bash
cd expense_tracker
```

### 2. Create a virtual environment (recommended)
```bash
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create a superuser (optional — for admin panel)
```bash
python manage.py createsuperuser
```

### 6. Run the server
```bash
python manage.py runserver
```

### 7. Open in browser
```
http://127.0.0.1:8000
```

---

## 🔑 Demo Login

| Field    | Value      |
|----------|------------|
| Username | `demo`     |
| Password | `demo1234` |

---

## 🎯 Features

- **Auth** — Register, Login, Logout (user-specific data)
- **Dashboard** — 4 stat cards, monthly bar chart, category donut chart
- **Smart Insights** — Highest category, week-over-week comparison
- **Expense CRUD** — Add, Edit, Delete expenses
- **Categories** — Food, Travel, Bills, Shopping, Health, Entertainment, Others
- **Filters** — By category and date range
- **Recent Transactions** — Last 8 on dashboard
- **Category Progress Bars** — Visual breakdown by month
- **Mobile Responsive** — Sidebar collapses on small screens

---

## 📁 Project Structure

```
expense_tracker/
├── manage.py
├── requirements.txt
├── README.md
├── db.sqlite3                    ← auto-created after migrate
├── expense_tracker/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── tracker/
    ├── admin.py
    ├── models.py
    ├── views.py
    ├── forms.py
    ├── urls.py
    ├── migrations/
    │   └── 0001_initial.py
    ├── static/tracker/css/
    │   └── style.css
    └── templates/
        ├── registration/
        │   ├── login.html
        │   └── register.html
        └── tracker/
            ├── base.html
            ├── dashboard.html
            ├── add_expense.html
            └── expense_list.html
```

---

## 🛠️ Tech Stack

| Layer       | Technology           |
|-------------|----------------------|
| Backend     | Django 4.2           |
| Database    | SQLite (default)     |
| Frontend    | Bootstrap 5 + DM Sans|
| Charts      | Chart.js 4.4         |
| Icons       | Bootstrap Icons 1.11 |

---

## 🎨 Design System

| Token        | Value              |
|--------------|--------------------|
| Primary      | `#0ea5e9` (Sky)    |
| Background   | `#f8fafc`          |
| Surface      | `#ffffff`          |
| Sidebar      | `#0f172a` (Navy)   |
| Border       | `#e2e8f0`          |
| Font         | DM Sans            |
| Border Radius| 12px               |

---

## 📝 Environment Variables (Production)

For production, update `settings.py`:
```python
SECRET_KEY = 'your-secure-secret-key'
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com']
```
