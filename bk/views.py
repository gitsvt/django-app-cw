from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate


def home(request):
    return render(request, 'bk/home.html')


# Create your views here.
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
            
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

def incandexplist(request):
    return render(request, 'bk/incandexplist.html')

