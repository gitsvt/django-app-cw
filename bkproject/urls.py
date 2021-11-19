from django.contrib import admin
from django.urls import path
from bk import views

urlpatterns = [
    #Admin
    path('admin/', admin.site.urls),

    #Auth
    path('signup/', views.signupuser, name='signupuser'),
    path('login/', views.loginuser, name='loginuser'),
    path('logout/', views.logoutuser, name='logoutuser'),
    
    # home
    path('', views.home, name='home'),
    
    path('incandexp/', views.incandexplist, name='incandexplist'),
    
    #expense
    path('addexpense/', views.addexpenses, name='addexpenses'),
    path('expense/<int:pk>/', views.viewexpense, name='viewexpense'),
    path('expense/<int:pk>/delete', views.deleteexpense, name='deleteexpense'),
    path('stats/', views.stats, name='stats'),

    #income
    path('addincome/', views.addincomes, name='addincomes'),
    path('income/<int:pk>/', views.viewincome, name='viewincome'),
    path('income/<int:pk>/delete', views.deleteincome, name='deleteincome'),
    path('incomestats/', views.incomestats, name='incomestats'),

    path('addwishes/', views.addnewwishes, name='addnewwish'),
    path('deletewishes/<int:pk>', views.deletewish, name='deletewish'),
    #path('stats/', views.stats, name='stats'),

]
