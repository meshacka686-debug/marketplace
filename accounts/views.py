from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import RegisterForm, ProfileForm, UserUpdateForm


def register(request):

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save()

            profile = user.profile
            profile.role = form.cleaned_data["role"]
            profile.phone = form.cleaned_data["phone"]
            profile.address = form.cleaned_data["address"]
            profile.save()

            login(request, user)

            return redirect("/")

    else:
        form = RegisterForm()

    return render(
        request,
        "accounts/register.html",
        {
            "form": form
        }
    )


def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            username=username,
            password=password
        )

        if user:

            login(request, user)

            return redirect("/")

        messages.error(
            request,
            "Invalid username or password."
        )

    return render(
        request,
        "accounts/login.html"
    )


@login_required
def become_seller(request):

    profile = request.user.profile

    if profile.role == "seller":

        messages.info(
            request,
            "You are already a seller."
        )

        return redirect("seller_dashboard")

    profile.role = "seller"
    profile.save()

    messages.success(
        request,
        "Congratulations! Your account is now a Seller account."
    )

    return redirect("seller_dashboard")


@login_required
def profile_view(request):

    user = request.user
    profile = user.profile

    if request.method == "POST":

        user_form = UserUpdateForm(
            request.POST,
            instance=user
        )

        profile_form = ProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if user_form.is_valid() and profile_form.is_valid():

            user_form.save()
            profile_form.save()

            messages.success(
                request,
                "Your profile has been updated successfully."
            )

            return redirect("profile")

    else:

        user_form = UserUpdateForm(
            instance=user
        )

        profile_form = ProfileForm(
            instance=profile
        )

    return render(
        request,
        "accounts/profile.html",
        {
            "user_form": user_form,
            "profile_form": profile_form,
            "profile": profile,
        }
    )


def logout_view(request):

    logout(request)

    return redirect("/")