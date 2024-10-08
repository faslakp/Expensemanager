from django import forms
from budget.models import Expense


class ExpenseForm(forms.ModelForm):
    class Meta:
        model=Expense
        # fields="__all__"
        exclude=("created_date","user")

        widgets={
            "title":forms.TextInput(attrs={"class":"form-control"}),
            "amount":forms.NumberInput(attrs={"class":"form-control"}),
            "category":forms.Select(attrs={"class":"form-control form-select"}),
            # "user":forms.TextInput(attrs={"class":"form-control"})
        }


from django.contrib.auth.models import User
class RegistrationForm(forms.ModelForm):

    class Meta:

        model=User

        fields=["username","email","password"]

        widgets={
            "username":forms.TextInput(attrs={"class":"form-control"}),
            "email":forms.EmailInput(attrs={"class":"form-control"}),
            "password":forms.PasswordInput(attrs={"class":"form-control"}),
        }
class SignInForm(forms.Form):

     username=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))

     password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))




        
