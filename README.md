# Spendwise — Expense Tracker

A full-featured personal expense tracking web app built with Django. Track your spending, set a budget, visualize trends, and export PDF reports — all in a clean 3D-styled dashboard.

---

## Features

- **Dashboard** — Budget overview, total expenses, and remaining balance at a glance
- **Expense Management** — Add, edit, and delete expenses with category tagging
- **Filters** — Filter expenses by category and date range
- **Charts** — Monthly spending trend (bar) and category breakdown (doughnut) via Chart.js
- **Smart Insights** — Auto-generated spending tips based on your data
- **PDF Reports** — Download a styled PDF report of your expenses (respects active filters)
- **Budget Tracking** — Set your total budget and see live balance remaining
- **User Auth** — Register, login, logout with per-user data isolation
- **3D UI** — Neumorphic / layered 3D design with raised cards, inset inputs, and glowing buttons

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3, Django 4 |
| Database | SQLite3 |
| Frontend | Bootstrap 5, Bootstrap Icons, Chart.js |
| PDF | ReportLab |
| Font | DM Sans (Google Fonts) |

---

## Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/Mouiezuddin/Expense_tracker.git
cd Expense_tracker
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install django reportlab
```

### 4. Run migrations

```bash
cd expense_tracker
python manage.py migrate
```

### 5. Start the development server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` in your browser.

---

## Project Structure

```
Expense_tracker/
├── expense_tracker/          # Django project root
│   ├── expense_tracker/      # Settings, URLs, WSGI
│   └── tracker/              # Main app
│       ├── models.py         # Expense, UserProfile models
│       ├── views.py          # All views including PDF generation
│       ├── forms.py          # Forms for expenses, profile, budget
│       ├── urls.py           # URL routing
│       ├── templates/        # HTML templates
│       └── static/           # CSS stylesheet
└── README.md
```

---

## Usage

1. **Register** an account at `/register/`
2. Go to **Profile** and set your total budget
3. Use **Add Expense** to log your spending
4. View the **Dashboard** for live budget vs expense vs balance cards
5. Use **All Expenses** to filter and browse transactions
6. Click **Download PDF** in the sidebar to export a report

---

## License

MIT — free to use and modify.
