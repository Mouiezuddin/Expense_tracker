# Spendwise — Lab Exam Q&A

Complete set of questions and answers for lab examination.

---

## 1. Project Overview

**Q: What is the name of your project and what does it do?**

A: The project is called **Spendwise**. It is a personal expense tracking web application built with Django. It allows users to register, log in, add/edit/delete expenses, set a budget, view spending analytics on a dashboard, and download a PDF report.

---

**Q: What tech stack did you use?**

A:
- Backend: Python 3, Django 4.2
- Database: SQLite3
- Frontend: Bootstrap 5, Bootstrap Icons, DM Sans (Google Fonts)
- Charts: Chart.js 4.4
- PDF Generation: ReportLab
- Styling: Custom CSS with neumorphic/3D design

---

## 2. Models

**Q: How many models do you have? Explain each.**

A: Three models:
1. **UserProfile** — stores the user's budget (linked to Django's built-in `User` via `OneToOneField`)
2. **Category** — a `TextChoices` enum defining 7 categories: Food, Travel, Bills, Shopping, Health, Entertainment, Others
3. **Expense** — stores each expense with fields: `user` (ForeignKey), `amount`, `category`, `description`, `date`, `created_at`, `updated_at`

---

**Q: What is `OneToOneField` and where did you use it?**

A: `OneToOneField` creates a one-to-one relationship between two models — meaning each record in one table maps to exactly one record in another. Used in `UserProfile` to link each user to exactly one profile:
```python
user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
```

---

**Q: What is `ForeignKey` and where did you use it?**

A: `ForeignKey` creates a many-to-one relationship. Used in `Expense` so many expenses can belong to one user:
```python
user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses')
```

---

**Q: What does `on_delete=models.CASCADE` mean?**

A: It means if the parent record (User) is deleted, all related child records (Expenses / UserProfile) are automatically deleted too.

---

**Q: What is `auto_now_add` vs `auto_now`?**

A:
- `auto_now_add=True` — sets the field to the current datetime only when the record is **created**. Used in `created_at`.
- `auto_now=True` — updates the field to the current datetime every time the record is **saved**. Used in `updated_at`.

---

**Q: What are Django signals? Where did you use them?**

A: Signals allow certain senders to notify a set of receivers when some action occurs. Used `post_save` signal on the `User` model to automatically create a `UserProfile` whenever a new user registers:
```python
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
```

---

**Q: What is `TextChoices` and why did you use it?**

A: `TextChoices` is a Django enum class for defining a fixed set of string choices for a model field. Used for `Category` so the expense category is always one of the 7 predefined values (Food, Travel, Bills, etc.), ensuring data consistency.

---

**Q: What is `class Meta` in a Django model?**

A: `Meta` is an inner class used to define model-level metadata. In `Expense`:
```python
class Meta:
    ordering = ['-date', '-created_at']
```
This means all queries return expenses sorted by newest date first by default.

---

## 3. Views

**Q: What is the `@login_required` decorator? Where did you use it?**

A: It's a Django decorator that redirects unauthenticated users to the login page. Applied to all protected views: `dashboard`, `add_expense`, `edit_expense`, `delete_expense`, `expense_list`, `profile`, and `generate_pdf`.

---

**Q: Explain the `dashboard` view.**

A: It fetches all expenses for the logged-in user, calculates totals (all-time, this month, this week, last week), retrieves the user's budget and balance, builds category breakdown data, generates monthly trend data for the last 6 months, creates smart insights, and passes everything to `dashboard.html` via context.

---

**Q: What is `commit=False` in `form.save(commit=False)`?**

A: It creates the model instance in memory without saving it to the database. This allows you to modify the instance before saving. Used in `add_expense` to attach the logged-in user before saving:
```python
expense = form.save(commit=False)
expense.user = request.user
expense.save()
```

---

**Q: What is `get_object_or_404`? Where did you use it?**

A: It fetches an object from the database or raises a 404 error if not found. Used in `edit_expense` and `delete_expense` to safely retrieve an expense by its primary key and ensure it belongs to the current user:
```python
expense = get_object_or_404(Expense, pk=pk, user=request.user)
```

---

**Q: How does filtering work in `expense_list`?**

A: A `FilterForm` is submitted via GET request. The view reads `category`, `date_from`, and `date_to` from `request.GET`, then chains `.filter()` calls on the queryset:
```python
if cat:
    expenses = expenses.filter(category=cat)
if date_from:
    expenses = expenses.filter(date__gte=date_from)
```

---

**Q: What does `aggregate` do? Give an example from your project.**

A: `aggregate` computes a summary value over a queryset. Used to calculate total spending:
```python
total_all = expenses.aggregate(t=Sum('amount'))['t'] or 0
```

---

**Q: What does `annotate` do? How is it different from `aggregate`?**

A: `annotate` adds a computed field to **each row** in the queryset, while `aggregate` returns a **single summary value** for the whole queryset. Used in category breakdown:
```python
cat_data = expenses.values('category').annotate(total=Sum('amount'), count=Count('id'))
```

---

## 4. Forms

**Q: What forms did you create? Explain each.**

A:
1. **RegisterForm** — extends `UserCreationForm`, adds `email` and `first_name` fields
2. **ExpenseForm** — ModelForm for `Expense`, includes amount, category, description, date
3. **FilterForm** — plain `Form` (not ModelForm) for filtering expenses by category and date range
4. **ProfileForm** — ModelForm for `User`, updates first_name, email, username
5. **BudgetForm** — ModelForm for `UserProfile`, updates the budget field

---

**Q: What is the difference between `forms.Form` and `forms.ModelForm`?**

A: `ModelForm` is tied to a database model and can automatically save data to it. `Form` is a standalone form not linked to any model. `FilterForm` uses `forms.Form` because it's only used for filtering, not saving data.

---

**Q: What is `{% csrf_token %}` and why is it important?**

A: It generates a hidden input field with a CSRF (Cross-Site Request Forgery) token. Django validates this token on every POST request to prevent malicious sites from submitting forms on behalf of authenticated users.

---

## 5. URLs

**Q: Explain the URL structure of your project.**

A: The main `urls.py` includes all routes from `tracker/urls.py`. Key routes:
- `/` and `/login/` → login page
- `/register/` → registration
- `/dashboard/` → main dashboard
- `/expenses/` → list all expenses
- `/expenses/add/` → add new expense
- `/expenses/edit/<int:pk>/` → edit expense by ID
- `/expenses/delete/<int:pk>/` → delete expense by ID
- `/profile/` → user profile & budget
- `/pdf-report/` → download PDF

---

**Q: What is `<int:pk>` in a URL pattern?**

A: It's a URL path converter that captures an integer from the URL and passes it as a keyword argument `pk` to the view. Used to identify which specific expense to edit or delete.

---

## 6. Templates

**Q: What is template inheritance? How did you use it?**

A: Template inheritance allows child templates to extend a base template and override specific blocks. `base.html` defines the sidebar, topbar, and layout. All other templates use:
```html
{% extends 'tracker/base.html' %}
{% block content %}...{% endblock %}
```

---

**Q: What is `{% load static %}` and why is it needed?**

A: It loads Django's static files template tag library, which is required before using `{% static 'path/to/file' %}` to reference CSS, JS, or image files.

---

**Q: How do you display flash messages in your templates?**

A: Using Django's messages framework. In `base.html`:
```html
{% for msg in messages %}
  <div class="custom-alert alert-{{ msg.tags }}">{{ msg }}</div>
{% endfor %}
```
In views, messages are added with `messages.success(request, '...')` or `messages.error(request, '...')`.

---

## 7. Dashboard & Charts

**Q: What charts are on the dashboard and what library powers them?**

A: Two charts powered by **Chart.js 4.4**:
1. **Monthly Spending Trend** — a bar chart showing spending for the last 6 months
2. **Category Breakdown** — a doughnut chart showing spending split by category for the current month

---

**Q: How do you pass Python data to JavaScript for the charts?**

A: The view serializes data to JSON using `json.dumps()` and passes it in the context. In the template, it's embedded in `<script>` tags with `type="application/json"`, then read by JavaScript:
```html
<script id="monthlyLabelsData" type="application/json">{{ monthly_labels_json|safe }}</script>
```
```js
const monthlyLabels = JSON.parse(document.getElementById('monthlyLabelsData').textContent);
```

---

## 8. PDF Generation

**Q: How did you generate the PDF report?**

A: Using the **ReportLab** library. The `generate_pdf` view builds a PDF in memory using `BytesIO`, creates a `SimpleDocTemplate`, and adds styled tables (header, summary cards, category breakdown, transactions table). It returns an `HttpResponse` with `content_type='application/pdf'` and a `Content-Disposition` header to trigger a download.

---

**Q: What is `BytesIO` and why is it used in PDF generation?**

A: `BytesIO` is an in-memory binary stream from Python's `io` module. It's used instead of writing to a file on disk — the PDF is built entirely in memory and streamed directly to the HTTP response, which is faster and doesn't leave files on the server.

---

## 9. Authentication

**Q: How does user authentication work in your project?**

A: Uses Django's built-in auth system:
- **Register**: `RegisterForm` (extends `UserCreationForm`) creates a new `User`, then `login()` is called automatically
- **Login**: `AuthenticationForm` validates credentials, `authenticate()` checks them, `login()` creates the session
- **Logout**: `logout()` clears the session, redirects to login page
- Settings define `LOGIN_URL`, `LOGIN_REDIRECT_URL`, and `LOGOUT_REDIRECT_URL`

---

**Q: How is user data kept separate between users?**

A: Every query filters by `user=request.user`:
```python
expenses = Expense.objects.filter(user=request.user)
```
This ensures each user only sees their own data.

---

## 10. Settings & Configuration

**Q: What database does your project use and where is it configured?**

A: SQLite3, configured in `settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

---

**Q: What is `DEBUG = True` and should it be used in production?**

A: `DEBUG = True` shows detailed error pages with tracebacks. It must be set to `False` in production for security — detailed errors could expose sensitive code and configuration to attackers.

---

**Q: What command do you run to apply model changes to the database?**

A: Two commands:
```bash
python manage.py makemigrations   # creates migration files
python manage.py migrate          # applies them to the database
```

---

## 11. Additional Features

**Q: What is the budget tracking feature?**

A: Users can set a total budget in their profile. The dashboard displays three main cards:
1. **My Budget** - Total money available
2. **Total Expenses** - All-time spending
3. **Balance Left** - Budget minus expenses (shows warning if over budget)

---

**Q: What are smart insights?**

A: Auto-generated spending tips based on user data:
- Highest spending category
- Week-over-week comparison
- Budget warnings
- Average daily spending

---

**Q: How does the PDF report respect filters?**

A: The `generate_pdf` view reads filter parameters from `request.GET` (category, date_from, date_to) and applies the same filters used in `expense_list` before generating the PDF.

---

## 12. Best Practices

**Q: What security measures did you implement?**

A:
- CSRF protection on all forms
- `@login_required` decorator on protected views
- User data isolation (filter by `request.user`)
- Password hashing (Django's built-in auth)
- SQL injection prevention (Django ORM)

---

**Q: How is the code organized?**

A: Following Django's MVT (Model-View-Template) pattern:
- **Models** - Data structure and business logic
- **Views** - Request handling and response generation
- **Templates** - HTML presentation layer
- **Forms** - Data validation and cleaning
- **Static files** - CSS, JS, images
- **URLs** - Route mapping

---

## 13. Deployment Considerations

**Q: What changes are needed for production deployment?**

A:
1. Set `DEBUG = False`
2. Change `SECRET_KEY` to a secure random value
3. Update `ALLOWED_HOSTS` with your domain
4. Use PostgreSQL instead of SQLite
5. Configure static files serving
6. Set up HTTPS
7. Use environment variables for sensitive data
8. Enable security middleware

---

**Q: What is the purpose of `requirements.txt`?**

A: It lists all Python packages and their versions needed to run the project. Anyone can install all dependencies with:
```bash
pip install -r requirements.txt
```
