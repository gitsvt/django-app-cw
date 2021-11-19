from typing import ItemsView
from django.core.checks import messages
from django.db.models import query, Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from bk.models import Expense, Income
from .forms import ExpenseForm, IncomeForm, WishesForm 
from .models import Expense, Income, WishesList
from django.contrib.auth.decorators import login_required
import datetime

def home(request):
    return render(request, 'bk/home.html')

def signupuser(request):
    if request.method == 'GET':
        return render(request, 'bk/signupuser.html', {'form':UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            #create new user
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('incandexplist')
            except IntegrityError:
                return render(request, 'bk/signupuser.html', {'form':UserCreationForm(), 'error':'Это имя пользователя уже используется!'})
        else:
            #сообщить что пароли не совпадают
            return render(request, 'bk/signupuser.html', {'form':UserCreationForm(), 'error':'Пароли не совпадают!'})

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'bk/loginuser.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'bk/loginuser.html', {'form':AuthenticationForm(), 'error':'Имя пользователя и пароль не совпадают!'})
        else:
            login(request, user)
            return redirect('incandexplist')
@login_required            
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

@login_required
def addexpenses(request):
    if request.method == 'GET':
        return render(request, 'bk/addexpenses.html', {'form':ExpenseForm()})
    else:
        try:
            form = ExpenseForm(request.POST)
            if form.is_valid():
                print(form.cleaned_data)
                amount = form.cleaned_data['amount']
                description = form.cleaned_data['description']
                date = form.cleaned_data['date']
                category = form.cleaned_data['category']
                owner = request.user
                print("\n\n\t", amount, description, date, category, owner)
                
                print(category)
                Expense.objects.create(owner=owner, amount=amount, date=date, category=category, description=description)
                return redirect('incandexplist')
        except ValueError:
            return render(request, 'bk/addexpenses.html', {'form':ExpenseForm(), 'error':'Введены неверные данные. Попробуйте снова!'})

@login_required
def addincomes(request):
    if request.method == 'GET':
        return render(request, 'bk/addincomes.html', {'form':IncomeForm()})
    else:
        try:
            form = IncomeForm(request.POST)
            if form.is_valid():
                print(form.cleaned_data)
                amount = form.cleaned_data['amount']
                description = form.cleaned_data['description']
                date = form.cleaned_data['date']
                source = form.cleaned_data['source']
                owner = request.user
                print("\n\n\t", amount, description, date, source, owner)
                Income.objects.create(owner=owner, amount=amount, date=date, source=source, description=description)
                return redirect('incandexplist')
        except ValueError:
            return render(request, 'bk/addincomes.html', {'form':IncomeForm(), 'error':'Введены неверные данные. Попробуйте снова!'})


@login_required
def addnewwishes(request):
    if request.method == 'GET':
        return render(request, 'bk/addwishes.html', {'form':WishesForm()})
    else:
        try:
            form = WishesForm(request.POST)
            if form.is_valid():
                print(form.cleaned_data)
                amount = form.cleaned_data['amount']
                description = form.cleaned_data['description']
                owner = request.user
                WishesList.objects.create(owner=owner, amount=amount, description=description)
                return redirect('incandexplist')
        except ValueError:
            return render(request, 'bk/addwishes.html', {'form':WishesForm(), 'error':'Введены неверные данные. Попробуйте снова!'})

@login_required    
def deletewish(request, pk):
    wish = get_object_or_404(WishesList, pk=pk, owner=request.user)
    wish.delete()
    return redirect('incandexplist')

@login_required
def incandexplist(request):
    expenses = Expense.objects.filter(owner=request.user).order_by('-date')
    incomes = Income.objects.filter(owner=request.user).order_by('-date')
    whishes = WishesList.objects.filter(owner=request.user)
    return render(request, 'bk/incandexplist.html', {'expenses':expenses, 'incomes':incomes, 'whishes':whishes})

@login_required
def viewexpense(request, pk):
    #expense = Expense.objects.get(pk=pk)
    exp = get_object_or_404(Expense, pk=pk, owner=request.user)
    if request.method == 'GET':
        form = ExpenseForm(instance=exp)
        return render(request, 'bk/viewexpense.html', {'exp':exp, 'form':form})
    else:
        try:
            form = ExpenseForm(request.POST, instance=exp)
            form.save()
            return redirect('incandexplist')
        except ValueError:
           return render(request, 'bk/viewexpense.html', {'exp':exp, 'form':form, 'error':'Введены неверные данные. Попробуйте снова!'})

@login_required
def viewincome(request, pk):
    #expense = Expense.objects.get(pk=pk)
    inc = get_object_or_404(Income, pk=pk, owner=request.user)
    if request.method == 'GET':
        form = IncomeForm(instance=inc)
        return render(request, 'bk/viewincome.html', {'inc':inc, 'form':form})
    else:
        try:
            form = IncomeForm(request.POST, instance=inc)
            form.save()
            return redirect('incandexplist')
        except ValueError:
           return render(request, 'bk/viewincome.html', {'inc':inc, 'form':form, 'error':'Введены неверные данные. Попробуйте снова!'})

#@login_required
# def viewwhish(request, pk):
#     #expense = Expense.objects.get(pk=pk)
#     wish = get_object_or_404(WishesList, pk=pk, owner=request.user)
#     if request.method == 'GET':
#         form = WishesForm(instance=wish)
#         return render(request, 'bk/viewwish.html', {'wish':wish, 'form':form})
#     else:
#         try:
#             form = WishesForm(request.POST, instance=wish)
#             form.save()
#             return redirect('incandexplist')
#         except ValueError:
#            return render(request, 'bk/viewwish.html', {'wish':wish, 'form':form, 'error':'Введены неверные данные. Попробуйте снова!'})


@login_required    
def deleteincome(request, pk):
    inc = get_object_or_404(Income, pk=pk, owner=request.user)
    inc.delete()
    return redirect('incandexplist')


@login_required    
def deleteexpense(request, pk):
    exp = get_object_or_404(Expense, pk=pk, owner=request.user)
    exp.delete()
    return redirect('incandexplist')

@login_required 
def incomestats(request):
    return render(request, 'bk/incomestats.html')

@login_required 
def stats(request):
    labels = []
    data = []
    labels_3 = []
    data_3 = []

    amount_exp_today = []
    amount_exp_week = []

    labels_month_income = []
    data_month_income = []

    labels_week_income = []
    data_week_income = []

    data_sixmon_income = []

    query_wishes = []
    
    todays_date = datetime.date.today()
    day = todays_date-datetime.timedelta(days=1)
    query_exp_today = Expense.objects.filter(owner=request.user,
                                      date__gte=day, date__lte=todays_date)

    for exptoday in query_exp_today:
        amount_exp_today.append(exptoday.amount)

    this_week = todays_date-datetime.timedelta(days=7)
    query_exp_week = Expense.objects.filter(owner=request.user,
                                      date__gte=this_week, date__lte=todays_date)
    
    for expweek in query_exp_week:
        amount_exp_week.append(expweek.amount)

    print('За неделю РАСХОДЫ: ', amount_exp_week)

    month_ago = todays_date-datetime.timedelta(days=30)
    query_sec = Expense.objects.filter(owner=request.user,
                                      date__gte=month_ago, date__lte=todays_date)

    three_month_ago = todays_date-datetime.timedelta(days=30*3)
    query_fst = Expense.objects.filter(owner=request.user,
                                      date__gte=three_month_ago, date__lte=todays_date)
    
    for d in query_sec:
        labels.append(d.description)
        data.append(d.amount)

    for d in query_fst:
        labels_3.append(d.description)
        data_3.append(d.amount)


    three_sixmonth_ago = todays_date-datetime.timedelta(days=30*6)
    query_sixmon_income = Income.objects.filter(owner=request.user,
                                      date__gte=three_sixmonth_ago, date__lte=todays_date)
    
    for item in query_sixmon_income:
        data_sixmon_income.append(item.amount)


    query_month_income = Income.objects.filter(owner=request.user,
                                      date__gte=month_ago, date__lte=todays_date)
    
    for item in query_month_income:
        labels_month_income.append(item.description)
        data_month_income.append(item.amount)

    this_week = todays_date-datetime.timedelta(days=7)
    query_week_income = Income.objects.filter(owner=request.user,
                                      date__gte=this_week, date__lte=todays_date)
    
    for item in query_week_income:
        labels_week_income.append(item.description)
        data_week_income.append(item.amount)

    print('INCOME WEEK: ',data_week_income)
    exptoday = sum(amount_exp_today)
    exppm = sum(data)
    exppw = sum(amount_exp_week)

    incmon = sum(data_month_income)
    incweek = sum(data_week_income)
    incsixmon = sum(data_sixmon_income)

    incomepermonth = sum(data_month_income)
    expensepermonth = sum(data)
    res = incomepermonth - expensepermonth
    print('Свободные деньги за месяц:', res)
    query_wishess = WishesList.objects.filter(owner=request.user, amount__lte = res)
    print('Какие можно купить: ', query_wishess)
    return render(request, 'bk/stats.html', {
        'labels': labels,
        'data': data,
        'labels_3': labels_3,
        'data_3': data_3,
        'labels_month_income': labels_month_income,
        'data_month_income': data_month_income,
        'labels_week_income': labels_week_income,
        'data_week_income': data_week_income,
        'query_wishes': query_wishess,
        'exptoday': exptoday,
        'expweek': exppw,
        'exppermon': exppm,
        'incmon': incmon,
        'incweek': incweek,
        'incsixmon': incsixmon
    })
   