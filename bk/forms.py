# from django.db.models.base import Model
# from django.forms import ModelForm, TypedChoiceField, fields, widgets
from .models import Expense, Category
from django import forms

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['amount', 'date', 'description', 'category']

        widgets = {
            'amount': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Сумма'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Дата'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Описание'}),
            'category': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Категория'}),
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