# from django.db.models.base import Model
# from django.forms import ModelForm, TypedChoiceField, fields, widgets
from .models import Expense, Income, WishesList
from django import forms

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['amount', 'date', 'description', 'category']

        widgets = {
            'amount': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['amount', 'date', 'description', 'source']

        widgets = {
            'amount': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'source': forms.Select(attrs={'class': 'form-control'}),
        }

class WishesForm(forms.ModelForm):
    class Meta:
        model = WishesList
        fields = ['amount', 'description']

        widgets = {
            'amount': forms.TextInput(attrs={'class': 'form-control'}),        
            'description': forms.TextInput(attrs={'class': 'form-control'}),
        }
# class ExpenseForm(forms.Form):
#     amount = forms.FloatField(label='Сумма:')
#     date = forms.DateField(label='Дата', widget = forms.SelectDateWidget)
#     description = forms.CharField(label='Описание:')
#     category = forms.ModelChoiceField(label='Категория:', queryset=Category.objects.all())

# class AddExpenseForm(ModelForm):
#     class Meta:
#         model = Expense
#         categories = Category.objects.all()
#         #fields = [categories]