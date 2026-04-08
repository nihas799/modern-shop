from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,authenticate
from .models import *


def register(request):
    if request.method == "POST":
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {
                'error': 'Username already exists.'
            })
        if not email:
            messages.error(request, "Email is required.")
            return redirect("register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect("register")

        # If username empty → create from email
        if not username:
            username = email.split("@")[0]

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        login(request, user)
        return redirect("product_list")

    return render(request, "register.html")
# Create your views here.
def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")


        auth_user = authenticate(
            request,
            username=username,
            password=password
        )
        if auth_user:
            login(request, auth_user)
            return redirect("product_list")

        messages.error(request, "Invalid email or password")

    return render(request, "login.html")
def profile(request):
    return render(request, 'profile.html')

