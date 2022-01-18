from django.shortcuts import render, redirect
from django.http import HttpResponse
from CLP.forms import UserForm, UserProfileInfoForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib import messages

# Create your views here.


def index(request):
    d = {"insert_me": "This is the view.py file"}
    return render(request, "CLP/index.html", context=d)


def login_(request):
    return render(request, "CLP/home.html")


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


def register(request):
    if request.method == "POST" and "signin" in request.POST:
        username = request.POST.get("Username")
        password = request.POST.get("Password")
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse("home"))
            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")
        else:
            print("SOMEONE TRIED TO LOGIN AND FAILED")
            print("Username: {} and password: {}".format(username, password))
            return redirect("login")
    elif request.method == "POST" and "signup" in request.POST:
        registered = False
        profile_form = UserProfileInfoForm(data=request.POST)
        user_form = UserForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            registered = True
        else:
            print(user_form.errors)
    else:
        profile_form = UserProfileInfoForm()
        user_form = UserForm()
    return render(
        request,
        "CLP/login.html",
        {"user_form": user_form, "profile_form": profile_form},
    )
