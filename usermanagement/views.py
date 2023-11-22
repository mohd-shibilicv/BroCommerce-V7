from django.shortcuts import render
from django.urls import reverse
from django.views import generic

from .forms import CustomUserCreationForm


def user_account(request):
    return render(request, "usermanagement/user_account.html")


class SignUpView(generic.CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse("usermanagement:login")
