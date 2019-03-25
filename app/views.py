from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.views import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from  .models import Petition

def index(request):
    petition_list = Petition.objects.all()
    return render(request, 'index.html', {
        "petition_list": petition_list
    })


# AUTH

@login_required
def logout(request):
    auth_logout(request)
    return redirect('index')


class LoginPage(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('index')
        else:
            return render(request, 'login.html', {
                "form": AuthenticationForm,
            })

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('index')
        else:
            messages.error(request, 'Invalid log-in form!')
            return render(request, 'login.html', {
                "form": AuthenticationForm,
            })


class SignupPage(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('index')
        else: 
            return render(request, 'signup.html', {
                "form": UserCreationForm,
            })

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
        else:
            messages.error(request, 'Invalid sign-up form!')
            return render(request, 'signup.html', {
                "form": UserCreationForm,
            })
