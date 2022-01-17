from django.shortcuts import render
from django.http import HttpResponse
from CLP.forms import UserForm, UserProfileInfoForm
# Create your views here.


def index(request):
    d = {
        'insert_me': 'This is the view.py file'
    }
    return render(request, 'CLP/index.html', context=d)


def login(request):
    return render(request, 'CLP/login.html')


def register(request):
    registered = False
    if(request.method == 'POST'):
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

    return render(request, 'CLP/login.html', {'user_form': user_form, 'profile_form': profile_form})
