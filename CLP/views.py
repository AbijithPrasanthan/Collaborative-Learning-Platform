from django.shortcuts import render, redirect
from django.http import HttpResponse
from CLP.forms import UserForm, UserProfileInfoForm, ResetPassword
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from Collaborative_Learning_Platform.settings import EMAIL_HOST_USER
from django.template.defaultfilters import slugify
# Create your views here.
from .models import MeetingInfo
import random
import string


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def index(request):
    data = list(MeetingInfo.objects.values())
    popup = False
    content = False
    if len(data) != 0:
        content = True
    if request.method == 'POST' and is_ajax(request):
        popup = True
        id_ele = request.POST['id']
        data_id = MeetingInfo.objects.get(slug=id_ele)
        print(data_id)

    return render(request, 'CLP/dashboard.html', context={'page_title': 'CLP | Dashboard', 'data': data, 'content': content})


def login_(request):
    return render(request, 'CLP/dashboard.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))


def register(request):
    auth_user = False
    profile_form = UserProfileInfoForm()
    user_form = UserForm()
    if request.method == 'POST' and 'signin' in request.POST:
        username = request.POST.get('Username')
        password = request.POST.get('Password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('home'))
            else:
                return HttpResponse('ACCOUNT NOT ACTIVE')
        else:
            auth_user = True
    elif request.method == 'POST' and 'signup' in request.POST:
        registered = False
        profile_form = UserProfileInfoForm(data=request.POST)
        user_form = UserForm(data=request.POST)
        password = request.POST.get('password')
        password1 = request.POST.get('password1')

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
            print(profile_form.errors)
            print('error occured while registeration')
    return render(request, 'CLP/login.html', {'user_form': user_form, 'profile_form': profile_form, 'auth_user': auth_user})


def password_reset_request(request):
    email_sent = False
    if request.method == "POST":
        password_reset_form = ResetPassword(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['Email']
            user = User.objects.filter(email=data)
            if user.exists():
                subject = "Password Reset Requested"
                email_template_name = "CLP/password/password_reset_email.txt"
                c = {
                    "email": user[0].email,
                    'domain': '127.0.0.1:8000',
                    'site_name': 'Collaborative Learning Platform',
                    "uid": urlsafe_base64_encode(force_bytes(user[0].pk)),
                    "user": user[0],
                    'token': default_token_generator.make_token(user[0]),
                    'protocol': 'http',
                }
                email = render_to_string(email_template_name, c)
                try:
                    send_mail(subject, email, EMAIL_HOST_USER, [
                              user[0].email], fail_silently=False)
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
                return redirect("/password_reset/done/")
    password_reset_form = ResetPassword()
    return render(request=request, template_name="CLP/password/password_reset.html", context={"password_reset_form": password_reset_form, 'email_sent': email_sent})


def newMeeting(request):
    if request.method == 'POST':
        topic = request.POST.get('Topic')
        subject = request.POST.get('Subject')
        time = request.POST.get('Time')
        m = min((16-len(topic), 5))
        if m == 0:
            m = 5
        randVal = ''.join(random.choice(
            string.ascii_lowercase + string.digits) for _ in range(m))
        slug = slugify(topic.lower()[:8] + " " + str(randVal))
        meeting = MeetingInfo(topic=topic, sub=subject, time=time, slug=slug)
        meeting.save()
        return redirect('index')

    return render(request, 'CLP/newMeeting.html', context={'page_title': 'CLP | New Meeting'})


def meeting(request):
    randomstr = ''.join(random.choices(
        string.ascii_letters+string.digits, k=8))
    return render(request, 'CLP/meeting.html', context={'page_title': 'CLP | Meeting'})


def showDetails(request, id):
    print("THE ID IS: ", id)
    return render(request, 'CLP/dashboardPopup.html')
