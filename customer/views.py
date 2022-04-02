from django.shortcuts import render,redirect
from owner.models import Books
from django.views.generic import View,CreateView,ListView
from customer.forms import UserRegistrationForm,LoginForm,PasswordResetForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from customer.models import Carts
from customer.decorators import sign_in_required
from django.utils.decorators import method_decorator
from django.contrib import messages


# Create your views here.
@method_decorator(sign_in_required,name="dispatch")
class CustomerIndex(ListView):
    model=Books
    template_name = "custhome.html"
    context_object_name = "books"
    # def get(self,request,*args,**kwargs):
    #     qs=Books.objects.all()
    #     return render(request,"custhome.html",{"books":qs})
class SignupView(CreateView):
    model=User
    template_name = "signup.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy("signin")
    # def get(self,request,*args,**kwargs):
    #     form=UserRegistrationForm()
    #     return render(request,"signup.html",{"form":form})
    # def post(self,request,*args,**kwargs):
    #     form=UserRegistrationForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return redirect("signin")
    #     else:
    #         return render(request,"signup.html",{"form":form})
class SignInView(View):
    def get(self,request,*args,**kwargs):
        form=LoginForm()
        return render(request,"signin.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            user=authenticate(request,username=username,password=password)
            if user:
                print('login success')
                login(request,user)
                return redirect('custhome')
            else:
                print('login failed')
            return render(request,'signin.html',{'form':form})
def signout(request):
    logout(request)
    return redirect('signin')
@method_decorator(sign_in_required,name="dispatch")
class PasswordResetView(View):
    def get(self,request):
        form=PasswordResetForm()
        return render(request,'password_reset.html',{"form":form})
    def post(self,request):
        form=PasswordResetForm(request.POST)
        if form.is_valid():
            currentpassword=form.cleaned_data.get('currentpassword')
            newpassword=form.cleaned_data.get('newpassword')
            user=authenticate(request,username=request.user,password=currentpassword)
            if user:
                user.set_password(newpassword)
                user.save()
                return redirect('signin')
            else:
                return render(request,'password_reset.html')
        else:
            return render(request, 'password_reset.html')

@sign_in_required
def add_to_carts(request,*args,**kwargs):
    book=Books.objects.get(id=kwargs["id"])
    user=request.user
    cart=Carts(product=book,
               user=user)
    cart.save()
    messages.success(request,"Item has been added to the cart")
    return redirect("custhome")
@method_decorator(sign_in_required,name="dispatch")
class ViewMycart(ListView):
    model = Carts
    template_name = "mycart.html"
    context_object_name = "carts"
    def get_queryset(self):
        return Carts.objects.filter(user=self.request.user).exclude(status="ordercancelled").order_by("date")
def remove_from_carts(request,*args,**kwargs):
        cart=Carts.objects.get(id=kwargs["id"])
        cart.status="ordercancelled"
        cart.save()
        messages.error(request,"Item has been removed from the cart")
        return redirect("custhome")



