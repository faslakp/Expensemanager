from django.shortcuts import render,redirect

# Create your views here.

from django.views.generic import View
from budget.forms import ExpenseForm,RegistrationForm,SignInForm
from django.contrib import messages
from budget.models import Expense


from budget.decorators import signin_required
from django.utils.decorators import method_decorator

from django.views.decorators.cache import never_cache

decs=[signin_required,never_cache]

@method_decorator(decs,name="dispatch")
class ExpenseCreateView(View):

    def get(self,request,*args,**kwargs):

        form_instance=ExpenseForm()

        return render(request,"expense_create.html",{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        form_instance=ExpenseForm(request.POST)

        if form_instance.is_valid():

            form_instance.instance.user=request.user

            form_instance.save()

            messages.success(request,"expense added")

            return redirect("expense-list")
        
        else:

            messages.error(request,"failed")
            
            return render(request,"expense_create.html",{"form":form_instance})
        


@method_decorator(decs,name="dispatch")

class ExpenseListView(View):
    def get(self,request,*args,**kwargs):
        selected_category=request.GET.get("category","all")
        if selected_category == "all":
            qs=Expense.objects.filter(user=request.user)
        else:
            qs=Expense.objects.filter(category=selected_category,user=request.user)
        return render(request,"expense_list.html",{"expense":qs,"selected":selected_category})

        # # qs=Expense.objects.all()
        # qs=Expense.objects.filter(user=request.user)

        # if "category" in request.GET:
        #     category_value=request.GET.get("category")
        #     qs=qs.filter(category=category_value)
        #     if category_value=="all":
        #         qs=Expense.objects.filter(user=request.user)


        # return render(request,"expense_list.html",{"expense":qs,
        #                                            "selected":request.GET.get("category","all")})
    

    
@method_decorator(decs,name="dispatch")
class ExpenseDetailView(View):
    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        qs=Expense.objects.get(id=id)

        return render(request,"expense_deatail.html",{"expense":qs})
    


@method_decorator(decs,name="dispatch")
   
class ExpenseUpdateView(View):

        def get(self,request,*args,**kwargs):

            id=kwargs.get("pk")

            expense_obj=Expense.objects.get(id=id)

            form_instance=ExpenseForm(instance=expense_obj)

            return render(request,"expense_edit.html",{"form":form_instance})
        
        def post(self,request,*args,**kwargs):

            id=kwargs.get("pk")

            expense_obj=Expense.objects.get(id=id)


            form_instance=ExpenseForm(request.POST,instance=expense_obj)

            if form_instance.is_valid():

               form_instance.save()

               messages.success(request,"updated")

               return redirect("expense-list")
            
            else:
               
               messages.error(request,"error")
               return render(request,"expense_edit.html",{"form":form_instance})
            
            
@method_decorator(decs,name="dispatch")

class ExpenseDeleteView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        Expense.objects.get(id=id).delete()

        messages.success(request,"deleted")

        return redirect("expense-list")
    
from django.db.models import Count
from django.db.models import Sum
class SummaryView(View):
    def get(self,request,*args,**kwargs):

        qs=Expense.objects.filter(user=request.user)


        total_expense=qs.values("amount").aggregate(sum_expense=Sum("amount"))

        category_summary=qs.values("category").annotate(cat_count=Count("category"))
        context={
            "category_summary":category_summary,
            
        }
        return render(request,"dash_board.html",context)

    

from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
class SignUpView(View):

    template_name="register.html"

    def get(self,request,*args,**kwargs):

        form_instance=RegistrationForm()

        return render(request,self.template_name,{"form":form_instance})
    
    def post(self,request,*args,**kwargs):


        form_instance=RegistrationForm(request.POST)

        if form_instance.is_valid():

            data=form_instance.cleaned_data

            User.objects.create_user(**data)

            return redirect("expense-signin")
        
        else:

            return render(request,self.template_name,{"form":form_instance})
        

class SignInView(View):

    template_name="login.html"

    def get(self,request,*args,**kwargs):

        form_instance=SignInForm()

        return render(request,self.template_name,{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        form_instance=SignInForm(request.POST)

        if form_instance.is_valid():

            uname=form_instance.cleaned_data.get("username")

            pword=form_instance.cleaned_data.get("password")

            user_object=authenticate(request,username=uname,password=pword)

            if user_object:

                login(request,user_object)

                return redirect("expense-list")
            
        return render(request,self.template_name,{"form":form_instance})
    

@method_decorator(decs,name="dispatch")
class SignoutView(View):

    def get(self,request,*args,**kwargs):

        logout(request)

        return redirect("expense-signin")


class DashboardView(View):

    template_name="dash_board.html"
    def get(self,request,*args,**kwargs):
        return render(request,self.template_name)
    
    
            








    












