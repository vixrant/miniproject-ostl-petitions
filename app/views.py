from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import FormView
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.views import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from .models import Petition, Signature
from .forms import PetitionForm, SignatureForm


def index(request):
    if not request.user.is_authenticated:
        messages.info(request, "You are not logged in!")
    petition_list = Petition.objects.all()
    return render(request, "index.html", {"petition_list": petition_list})


class PetitionPage(View):
    def render(self, request, petition):

        try:
            if request.user.is_authenticated:
                user_sign = petition.signatures.get(signer=request.user)
                user_has_signed: bool = True
            else:
                user_has_signed: bool = False
        except Signature.DoesNotExist:
            user_has_signed: bool = False

        signs = list(petition.signatures.all())

        return render(
            request,
            "petition-details.html",
            {
                "petition": petition,
                "signature_form": SignatureForm,
                "user_has_signed": user_has_signed,
                "signs": signs,
            },
        )

    def get(self, request, pk):
        petition = get_object_or_404(Petition, pk=pk)
        return self.render(request, petition)

    def post(self, request, pk):
        if not request.user.is_authenticated:
            messages.warning(request, "How the fuck did you sign without logging in?")
            return redirect("login")

        petition = get_object_or_404(Petition, pk=pk)
        form = SignatureForm(data=request.POST)
        if form.is_valid():
            signature = form.save(commit=False)
            signature.petition = petition
            signature.signer = request.user
            signature.save()
            messages.success(request, "You have signed the petition!")
        else:
            messages.error(request, "Error in signature")

        return self.render(request, petition)


class NewPetitionPage(FormView):
    template_name = "new_petition.html"
    form_class = PetitionForm
    success_url = "/"

    def form_valid(self, form):
        if not self.request.user.is_authenticated:
            messages.error(request, "User not logged in!")
            return render(request, "login.html", {"form": AuthenticationForm})
        petition = form.save(commit=False)
        petition.poster = self.request.user
        petition.save()
        messages.success(self.request, "New petition successfully created")
        return super().form_valid(form)

    def form_invlaid(self, form):
        pass


# AUTH


@login_required
def logout(request):
    auth_logout(request)
    return redirect("index")


class LoginPage(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("index")
        else:
            return render(request, "login.html", {"form": AuthenticationForm})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect("index")
        else:
            messages.error(request, "Invalid log-in form!")
            return render(request, "login.html", {"form": AuthenticationForm})


class SignupPage(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("index")
        else:
            return render(request, "signup.html", {"form": UserCreationForm})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect("index")
        else:
            messages.error(request, "Invalid sign-up form!")
            messages.error(request, "Invalid sign-up form!")
            messages.error(request, "Invalid sign-up form!")
            return render(request, "signup.html", {"form": UserCreationForm})
