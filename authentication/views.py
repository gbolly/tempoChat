import logging
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect

from .forms import SignUpForm


logger = logging.getLogger("authentication")
api_logger = logging.getLogger("api")


def signup_view(request):
    api_logger.info(f"HTTP {request.method} {request.path}")
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.first_name = form.cleaned_data.get("first_name")
            user.last_name = form.cleaned_data.get("last_name")
            user.email = form.cleaned_data.get("email")
            user.save()
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            logger.info(f"User {user.username} signed up successfully.")
            return redirect("home")
        else:
            logger.error(f"Error occurred during signup: {form.errors}")
    else:
        form = SignUpForm()
    return render(request, "signup.html", {"form": form})


def login_view(request):
    api_logger.info(f"HTTP {request.method} {request.path}")
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                logger.info(f"User {user.username} logged in successfully.")
                return redirect("home")
            else:
                logger.error("Invalid username or password.")
        else:
            logger.error(f"Error occurred during login: {form.errors}")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})
