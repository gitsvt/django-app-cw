from django.core.checks import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from bk.models import Expense
from .forms import ExpenseForm 
from .models import Expense
from django.contrib.auth.decorators import login_required

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
                Expense.objects.create(owner=owner, amount=amount, date=date, category=category, description=description)
                return redirect('incandexplist')
        except ValueError:
            return render(request, 'bk/addexpenses.html', {'form':ExpenseForm(), 'error':'Введены неверные данные. Попробуйте снова!'})
@login_required
def incandexplist(request):
    expenses = Expense.objects.filter(owner=request.user)
    return render(request, 'bk/incandexplist.html', {'expenses':expenses})

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
def deleteexpense(request, pk):
    exp = get_object_or_404(Expense, pk=pk, owner=request.user)
    if request.method == 'POST':
        exp.delete()
        return redirect('incandexplist')
