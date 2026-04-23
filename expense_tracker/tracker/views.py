from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import date, timedelta
from collections import defaultdict
import json

from .models import Expense, Category, UserProfile
from .forms import RegisterForm, ExpenseForm, FilterForm, ProfileForm, BudgetForm
from django.contrib.auth.models import User
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from io import BytesIO
from django.http import HttpResponse
from datetime import date
from django.db.models import Sum


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome, {user.first_name}! Your account is ready.')
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    # Add CSS classes to auth form
    for field in form.fields.values():
        field.widget.attrs['class'] = 'form-control'
    return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    user = request.user
    expenses = Expense.objects.filter(user=user)

    today = date.today()
    this_week_start = today - timedelta(days=today.weekday())
    last_week_start = this_week_start - timedelta(days=7)
    last_week_end = this_week_start - timedelta(days=1)
    this_month_start = today.replace(day=1)

    total_all = expenses.aggregate(t=Sum('amount'))['t'] or 0
    total_this_month = expenses.filter(date__gte=this_month_start).aggregate(t=Sum('amount'))['t'] or 0
    total_this_week = expenses.filter(date__gte=this_week_start).aggregate(t=Sum('amount'))['t'] or 0
    total_last_week = expenses.filter(date__gte=last_week_start, date__lte=last_week_end).aggregate(t=Sum('amount'))['t'] or 0

    # Budget & balance
    user_profile, _ = UserProfile.objects.get_or_create(user=user)
    budget = user_profile.budget
    balance = budget - total_all

    # Category breakdown
    cat_data = expenses.filter(date__gte=this_month_start).values('category').annotate(
        total=Sum('amount'), count=Count('id')
    ).order_by('-total')

    cat_labels = []
    cat_totals = []
    cat_display = []
    for item in cat_data:
        label = dict(Category.choices).get(item['category'], item['category'])
        cat_labels.append(label)
        cat_totals.append(float(item['total']))
        cat_display.append({'category': item['category'], 'label': label, 'total': item['total'], 'count': item['count']})

    # Recent transactions
    recent = expenses[:8]

    # Smart insights
    insights = []
    if cat_display:
        top_cat = cat_display[0]
        insights.append(f"Highest spending: <strong>{top_cat['label']}</strong> (₹{top_cat['total']:.0f} this month)")
    if total_this_week > total_last_week and total_last_week > 0:
        diff = total_this_week - total_last_week
        insights.append(f"You spent <strong>₹{diff:.0f} more</strong> this week than last week")
    elif total_last_week > total_this_week and total_last_week > 0:
        diff = total_last_week - total_this_week
        insights.append(f"Great! You spent <strong>₹{diff:.0f} less</strong> this week than last week")
    if total_this_month > 10000:
        insights.append("Monthly spending is <strong>above ₹10,000</strong> — consider reviewing your budget")
    if not insights:
        insights.append("Add more expenses to see personalized spending insights")

    # Monthly trend (last 6 months)
    monthly_labels = []
    monthly_totals = []
    for i in range(5, -1, -1):
        d = today.replace(day=1) - timedelta(days=i * 28)
        month_start = d.replace(day=1)
        if month_start.month == 12:
            month_end = month_start.replace(year=month_start.year + 1, month=1, day=1) - timedelta(days=1)
        else:
            month_end = month_start.replace(month=month_start.month + 1, day=1) - timedelta(days=1)
        total = expenses.filter(date__gte=month_start, date__lte=month_end).aggregate(t=Sum('amount'))['t'] or 0
        monthly_labels.append(month_start.strftime('%b %Y'))
        monthly_totals.append(float(total))

    avg_daily = total_this_month / today.day if today.day else 0

    context = {
        'total_all': total_all,
        'total_this_month': total_this_month,
        'total_this_week': total_this_week,
        'total_last_week': total_last_week,
        'budget': budget,
        'balance': balance,
        'cat_display': cat_display,
        'recent': recent,
        'insights': insights,
        'cat_labels_json': json.dumps(cat_labels),
        'cat_totals_json': json.dumps(cat_totals),
        'monthly_labels_json': json.dumps(monthly_labels),
        'monthly_totals_json': json.dumps(monthly_totals),
        'avg_daily': avg_daily,
        'active': 'dashboard',
    }
    return render(request, 'tracker/dashboard.html', context)


@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            messages.success(request, 'Expense added successfully!')
            return redirect('expense_list')
    else:
        form = ExpenseForm(initial={'date': date.today()})
    return render(request, 'tracker/add_expense.html', {'form': form, 'active': 'add_expense'})


@login_required
def edit_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            messages.success(request, 'Expense updated successfully!')
            return redirect('expense_list')
    else:
        form = ExpenseForm(instance=expense)
    return render(request, 'tracker/add_expense.html', {'form': form, 'edit': True, 'expense': expense, 'active': 'expense_list'})


@login_required
def delete_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == 'POST':
        expense.delete()
        messages.success(request, 'Expense deleted.')
    return redirect('expense_list')


@login_required
def expense_list(request):
    expenses = Expense.objects.filter(user=request.user)
    filter_form = FilterForm(request.GET)

    if filter_form.is_valid():
        cat = filter_form.cleaned_data.get('category')
        date_from = filter_form.cleaned_data.get('date_from')
        date_to = filter_form.cleaned_data.get('date_to')
        if cat:
            expenses = expenses.filter(category=cat)
        if date_from:
            expenses = expenses.filter(date__gte=date_from)
        if date_to:
            expenses = expenses.filter(date__lte=date_to)

    total = expenses.aggregate(t=Sum('amount'))['t'] or 0

    context = {
        'expenses': expenses,
        'filter_form': filter_form,
        'total': total,
        'active': 'expense_list',
    }
    return render(request, 'tracker/expense_list.html', context)


@login_required
def profile(request):
    user = request.user
    user_profile, _ = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=user)
        budget_form = BudgetForm(request.POST, instance=user_profile)
        if form.is_valid() and budget_form.is_valid():
            form.save()
            budget_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = ProfileForm(instance=user)
        budget_form = BudgetForm(instance=user_profile)

    total_spent = Expense.objects.filter(user=user).aggregate(t=Sum('amount'))['t'] or 0
    expense_count = Expense.objects.filter(user=user).count()

    context = {
        'form': form,
        'budget_form': budget_form,
        'total_spent': total_spent,
        'expense_count': expense_count,
        'active': 'profile',
    }
    return render(request, 'tracker/profile.html', context)


@login_required
def generate_pdf(request):
    user = request.user
    today = date.today()

    # Respect the same filters as expense_list
    expenses = Expense.objects.filter(user=user).order_by('-date')
    cat_filter = request.GET.get('category', '')
    date_from  = request.GET.get('date_from', '')
    date_to    = request.GET.get('date_to', '')

    if cat_filter:
        expenses = expenses.filter(category=cat_filter)
    if date_from:
        try:
            from datetime import datetime
            expenses = expenses.filter(date__gte=datetime.strptime(date_from, '%Y-%m-%d').date())
        except ValueError:
            pass
    if date_to:
        try:
            from datetime import datetime
            expenses = expenses.filter(date__lte=datetime.strptime(date_to, '%Y-%m-%d').date())
        except ValueError:
            pass

    total = expenses.aggregate(t=Sum('amount'))['t'] or 0
    cat_summary = expenses.values('category').annotate(total=Sum('amount')).order_by('-total')

    user_profile, _ = UserProfile.objects.get_or_create(user=user)
    budget  = float(user_profile.budget)
    balance = budget - float(total)

    # ── Colour palette ──────────────────────────────────────────────
    NAVY   = colors.HexColor('#0f172a')
    BLUE   = colors.HexColor('#0ea5e9')
    LIGHT  = colors.HexColor('#f0f9ff')
    STRIPE = colors.HexColor('#f8fafc')
    MUTED  = colors.HexColor('#64748b')
    WHITE  = colors.white
    RED    = colors.HexColor('#ef4444')
    GREEN  = colors.HexColor('#10b981')

    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        rightMargin=48, leftMargin=48,
        topMargin=48, bottomMargin=36,
    )
    styles = getSampleStyleSheet()
    story  = []

    # ── Header band ─────────────────────────────────────────────────
    header_style = ParagraphStyle(
        'Header',
        fontSize=22, fontName='Helvetica-Bold',
        textColor=WHITE, alignment=1, spaceAfter=0,
    )
    sub_style = ParagraphStyle(
        'Sub',
        fontSize=10, fontName='Helvetica',
        textColor=colors.HexColor('#bae6fd'), alignment=1,
    )

    header_table = Table(
        [[Paragraph('Spendwise', header_style)],
         [Paragraph('Expense Report', sub_style)]],
        colWidths=[doc.width],
    )
    header_table.setStyle(TableStyle([
        ('BACKGROUND',  (0, 0), (-1, -1), NAVY),
        ('TOPPADDING',  (0, 0), (-1, -1), 18),
        ('BOTTOMPADDING', (0, -1), (-1, -1), 18),
        ('ROUNDEDCORNERS', [8]),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 16))

    # ── Meta info row ────────────────────────────────────────────────
    meta_style = ParagraphStyle('Meta', fontSize=9, fontName='Helvetica', textColor=MUTED)
    name_str  = user.get_full_name() or user.username
    range_str = ''
    if date_from and date_to:
        range_str = f'{date_from}  →  {date_to}'
    elif date_from:
        range_str = f'From {date_from}'
    elif date_to:
        range_str = f'Up to {date_to}'
    else:
        range_str = 'All time'

    meta_table = Table(
        [[Paragraph(f'<b>Account:</b> {name_str}', meta_style),
          Paragraph(f'<b>Period:</b> {range_str}', meta_style),
          Paragraph(f'<b>Generated:</b> {today.strftime("%d %b %Y")}', meta_style)]],
        colWidths=[doc.width / 3] * 3,
    )
    meta_table.setStyle(TableStyle([
        ('BACKGROUND',    (0, 0), (-1, -1), STRIPE),
        ('TOPPADDING',    (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING',   (0, 0), (-1, -1), 12),
        ('BOX',           (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
        ('ROUNDEDCORNERS', [6]),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 18))

    # ── Summary cards row ────────────────────────────────────────────
    card_label = ParagraphStyle('CL', fontSize=8, fontName='Helvetica', textColor=MUTED, alignment=1)
    card_value = ParagraphStyle('CV', fontSize=16, fontName='Helvetica-Bold', textColor=NAVY, alignment=1)
    bal_color  = RED if balance < 0 else GREEN

    def summary_cell(label, value, val_color=NAVY):
        return [Paragraph(label, card_label), Paragraph(value, ParagraphStyle('CV2', fontSize=16, fontName='Helvetica-Bold', textColor=val_color, alignment=1))]

    summary_table = Table(
        [[summary_cell('BUDGET', f'Rs.{budget:,.0f}'),
          summary_cell('TOTAL EXPENSES', f'Rs.{float(total):,.0f}', RED),
          summary_cell('BALANCE LEFT', f'Rs.{balance:,.0f}', bal_color)]],
        colWidths=[doc.width / 3] * 3,
    )
    summary_table.setStyle(TableStyle([
        ('BACKGROUND',    (0, 0), (-1, -1), LIGHT),
        ('TOPPADDING',    (0, 0), (-1, -1), 14),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 14),
        ('INNERGRID',     (0, 0), (-1, -1), 0.5, colors.HexColor('#bae6fd')),
        ('BOX',           (0, 0), (-1, -1), 0.5, colors.HexColor('#bae6fd')),
        ('ROUNDEDCORNERS', [6]),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 20))

    # ── Category breakdown ───────────────────────────────────────────
    if cat_summary:
        section_style = ParagraphStyle('Sec', fontSize=11, fontName='Helvetica-Bold', textColor=NAVY, spaceAfter=8)
        story.append(Paragraph('Category Breakdown', section_style))

        cat_header_style = ParagraphStyle('CH', fontSize=9, fontName='Helvetica-Bold', textColor=WHITE)
        cat_cell_style   = ParagraphStyle('CC', fontSize=9, fontName='Helvetica', textColor=NAVY)
        cat_amt_style    = ParagraphStyle('CA', fontSize=9, fontName='Helvetica-Bold', textColor=NAVY, alignment=2)

        cat_rows = [[
            Paragraph('CATEGORY', cat_header_style),
            Paragraph('TRANSACTIONS', cat_header_style),
            Paragraph('AMOUNT', ParagraphStyle('CAH', fontSize=9, fontName='Helvetica-Bold', textColor=WHITE, alignment=2)),
        ]]
        for item in cat_summary:
            label = dict(Category.choices).get(item['category'], item['category'])
            count = expenses.filter(category=item['category']).count()
            cat_rows.append([
                Paragraph(label, cat_cell_style),
                Paragraph(str(count), ParagraphStyle('CC2', fontSize=9, fontName='Helvetica', textColor=MUTED, alignment=1)),
                Paragraph(f'Rs.{float(item["total"]):,.2f}', cat_amt_style),
            ])

        cat_table = Table(cat_rows, colWidths=[doc.width * 0.5, doc.width * 0.25, doc.width * 0.25])
        row_bg = [STRIPE if i % 2 == 0 else WHITE for i in range(len(cat_rows) - 1)]
        cat_table.setStyle(TableStyle([
            ('BACKGROUND',    (0, 0), (-1, 0), BLUE),
            ('TOPPADDING',    (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING',   (0, 0), (-1, -1), 10),
            ('RIGHTPADDING',  (0, 0), (-1, -1), 10),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [STRIPE, WHITE]),
            ('BOX',           (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
            ('LINEBELOW',     (0, 0), (-1, 0), 0, WHITE),
        ]))
        story.append(cat_table)
        story.append(Spacer(1, 20))

    # ── Transactions table ───────────────────────────────────────────
    section_style = ParagraphStyle('Sec', fontSize=11, fontName='Helvetica-Bold', textColor=NAVY, spaceAfter=8)
    story.append(Paragraph('Transactions', section_style))

    th = ParagraphStyle('TH', fontSize=9, fontName='Helvetica-Bold', textColor=WHITE)
    td = ParagraphStyle('TD', fontSize=8, fontName='Helvetica', textColor=NAVY)
    td_r = ParagraphStyle('TDR', fontSize=8, fontName='Helvetica-Bold', textColor=NAVY, alignment=2)
    td_m = ParagraphStyle('TDM', fontSize=8, fontName='Helvetica', textColor=MUTED)

    rows = [[
        Paragraph('DATE', th),
        Paragraph('DESCRIPTION', th),
        Paragraph('CATEGORY', th),
        Paragraph('AMOUNT', ParagraphStyle('THR', fontSize=9, fontName='Helvetica-Bold', textColor=WHITE, alignment=2)),
    ]]
    for exp in expenses:
        cat_label = dict(Category.choices).get(exp.category, exp.category)
        rows.append([
            Paragraph(exp.date.strftime('%d %b %Y'), td_m),
            Paragraph(exp.description[:55], td),
            Paragraph(cat_label, td_m),
            Paragraph(f'Rs.{float(exp.amount):,.2f}', td_r),
        ])

    # Total row
    rows.append([
        Paragraph('', td),
        Paragraph('', td),
        Paragraph('TOTAL', ParagraphStyle('TOT', fontSize=9, fontName='Helvetica-Bold', textColor=NAVY, alignment=2)),
        Paragraph(f'Rs.{float(total):,.2f}', ParagraphStyle('TOTR', fontSize=9, fontName='Helvetica-Bold', textColor=BLUE, alignment=2)),
    ])

    exp_table = Table(rows, colWidths=[doc.width * 0.15, doc.width * 0.42, doc.width * 0.22, doc.width * 0.21])
    exp_table.setStyle(TableStyle([
        ('BACKGROUND',    (0, 0), (-1, 0), NAVY),
        ('TOPPADDING',    (0, 0), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
        ('LEFTPADDING',   (0, 0), (-1, -1), 8),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 8),
        ('ROWBACKGROUNDS', (0, 1), (-2, -1), [WHITE, STRIPE]),
        ('BACKGROUND',    (0, -1), (-1, -1), LIGHT),
        ('LINEABOVE',     (0, -1), (-1, -1), 1, BLUE),
        ('BOX',           (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
    ]))
    story.append(exp_table)

    # ── Footer ───────────────────────────────────────────────────────
    story.append(Spacer(1, 24))
    footer_style = ParagraphStyle('Foot', fontSize=8, fontName='Helvetica', textColor=MUTED, alignment=1)
    story.append(Paragraph(f'Spendwise  ·  Generated {today.strftime("%d %B %Y")}  ·  {name_str}', footer_style))

    doc.build(story)
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    fname = f'spendwise_{today.strftime("%Y%m%d")}.pdf'
    response['Content-Disposition'] = f'attachment; filename="{fname}"'
    return response
