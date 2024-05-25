from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .models import Expenses
from .forms import ExpensesForm
from django.utils import timezone
from datetime import datetime

def index(request):
    return render(request, 'index.html')

@login_required(login_url='/auth/login')
def home(request):
    now = timezone.now()
    start_of_month = datetime(now.year, now.month, 1)
    expenses = Expenses.objects.filter(user=request.user, date__gte=start_of_month)
    total_expenses = expenses.aggregate(total=Sum('amount'))['total'] or 0
    return render(request, 'home.html', {'expenses': expenses, 'total_expenses': total_expenses})

@login_required(login_url='/auth/login')
def add_expense(request):
    if request.method == 'POST':
        form = ExpensesForm(request.POST)
        if form.is_valid():
            new_expense = form.save(commit=False)
            new_expense.user = request.user
            new_expense.save()
            return redirect('home')
    else:
        form = ExpensesForm()
    return render(request, 'add_expense.html', {'form': form})

@login_required(login_url='/auth/login')
def edit_expense(request, expense_id):
    expense = get_object_or_404(Expenses, id=expense_id, user=request.user)
    if request.method == 'POST':
        form = ExpensesForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ExpensesForm(instance=expense)
    return render(request, 'edit_expense.html', {'form': form})

@login_required(login_url='/auth/login')
def delete_expense(request, expense_id):
    expense = get_object_or_404(Expenses, id=expense_id, user=request.user)
    if request.method == 'POST':
        expense.delete()
    return redirect('home')
