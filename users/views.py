from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages

from .forms import RegisterForm


def register(request):
    """Self-service sign-up.

    GET  -> show the empty RegisterForm
    POST -> validate, create the User, log them straight in and send
            them to the dashboard (same flow students expect everywhere)
    """
    # Already signed in? Nothing to do here.
    if request.user.is_authenticated:
        return redirect("users:dashboard")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Session login — the new account works immediately
            login(request, user)
            messages.success(request, f"Welcome to Dunis LMS, {user.username}! Your account is ready.")
            return redirect("users:dashboard")
        # Invalid → fall through and re-render with the errors shown
    else:
        form = RegisterForm()

    return render(request, "users/register.html", {"form": form})


@login_required
def dashboard(request):
    user = request.user
    return render(request, 'users/dashboard.html', {'user': user})
