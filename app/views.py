from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import FormView
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.views import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from  .models import Petition
from .forms import PetitionForm, SignatureForm

def index(request):
    petition_list = Petition.objects.all()
    return render(request, 'index.html', {
        "petition_list": petition_list
    })


def petition_details(request, pk):
    petition = get_object_or_404(Petition, pk=pk)
    return render(request, 'petition-details.html', {
        "petition": petition,
        "signature_form": SignatureForm,
    })


class NewPetitionPage(FormView):
    template_name = 'new_petition.html'
    form_class = PetitionForm
    success_url = '/'

    def form_valid(self, form):
        if not self.request.user.is_authenticated:
            messages.error(request, 'User not logged in!')
            return render(request, 'login.html', {
                "form": AuthenticationForm,
            })
        petition = form.save(commit=False)
        petition.poster = self.request.user
        petition.save()
        messages.success(self.request, 'New petition successfully created')
        return super().form_valid(form)

    def form_invlaid(self, form):
        pass


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
