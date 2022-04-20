from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.http import HttpResponse, JsonResponse
from CLP.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib import messages
from django.views import generic
from django.core.exceptions import ObjectDoesNotExist
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
from pygame import mixer
from django.http.response import StreamingHttpResponse
from CLP.camera import Detect
import winsound
import json
from .models import MeetingInfo, Room, Message, Notes, RewardInfo
import random
import string
from datetime import datetime


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def cam(request):
    return render(request, 'CLP/cam.html')


def gen(camera):
    t = 0
    mixer.init()
    mixer.music.load("CLP/Top-Touches-Wow.mp3")
    while True:
        frame, locs = camera.get_frame()
        if len(locs) == 0 and t == 0:
            mixer.music.play(-1)
            t = 1
        if len(locs) != 0 and t == 1:
            mixer.music.stop()
            t = 0
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def mask_feed(request):
    return StreamingHttpResponse(gen(Detect()),
                                 content_type='multipart/x-mixed-replace; boundary=frame')


def chat(request):
    content = False
    data = list(Room.objects.values())
    if len(data) != 0:
        content = True
    return render(request, 'CLP/chat.html', context={'data': data, 'content': content})


def room(request, room):
    username = request.GET.get('username')
    room_details = Room.objects.get(name=room)
    return render(request, 'CLP/chat_room.html', {'username': username, 'room': room, 'room_details': room_details})


def checkview(request):
    room = request.POST['room_name']
    username = request.POST['username']
    if Room.objects.filter(name=room).exists():
        return redirect(room + '/?username='+username)
    else:
        new_room = Room.objects.create(name=room, username=username)
        new_room.save()
        return redirect('/CLP/chat')


def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']
    print(message, username, room_id)
    new_message = Message.objects.create(
        value=message, user=username, room=room_id)
    new_message.save()
    return HttpResponse('Message sent successfully')


def getMessages(request, room):
    room_details = Room.objects.get(name=room)
    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages": list(messages.values())})


def index(request):
    rewardPts = 0
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    userObj = User.objects.get(username=request.user)
    try:
        userProf = UserProfileInfo.objects.get(user=userObj)
        rewardPts = userProf.rewardpoints
    except ObjectDoesNotExist:
        rewardPts = 0
    data = list(MeetingInfo.objects.values())
    popup = True
    content = False
    data_id = []
    if len(data) != 0:
        content = True
    if request.method == 'POST' and is_ajax(request):
        popup = True
        id_ele = request.POST['id']
        data_id = list(MeetingInfo.objects.filter(slug=id_ele))
    return render(request, 'CLP/dashboard.html', context={'page_title': 'CLP | Dashboard', 'data': data, 'content': content, 'popup': popup, 'rewardPts': rewardPts})


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


def meeting(request, id):
    randomstr = ''.join(random.choices(
        string.ascii_letters+string.digits, k=8))

    if request.method == 'POST' and is_ajax(request):

        roomName = request.POST['roomName']
        req = request.POST['info'][1:-1]

        l = list()
        temp = ''

        for ch in req:
            if ch == '{':
                temp = '{'
            elif ch == '}':
                temp += '}'
                l.append(temp)
                temp = ''
            else:
                temp += ch

        if request.POST['type'] == 'part_join':
            for info in l:
                obj = json.loads(info)
                print()
                print(obj)
                print()
                name = obj['displayName']
                userID = obj['participantId']
                print('User ID: ', userID)
                user = User.objects.get(username=name)
                meeting = MeetingInfo.objects.get(slug=roomName)
                userProfInfo = UserProfileInfo.objects.get(user=user)
                userProfInfo.userId = userID
                userProfInfo.save()
                try:
                    reward = RewardInfo.objects.select_related().filter(
                        roomName=meeting, username=user)
                    if len(list(reward)) == 0:
                        raise ObjectDoesNotExist
                    else:
                        reward.userId = userID
                except ObjectDoesNotExist:
                    newReward = RewardInfo(
                        roomName=meeting, username=user, lastJoined=datetime.now(), userId=userID)
                    newReward.save()

        elif request.POST['type'] == 'part_left':
            curr_time = datetime.now()

            partId = request.POST['userID[id]']

            leftPart = UserProfileInfo.objects.get(userId=partId)
            leftPartReward = RewardInfo.objects.get(userId=partId)
            leftPartLastJoined = leftPartReward.lastJoined.replace(tzinfo=None)

            leftPartTimeInMeet = curr_time - leftPartLastJoined

            if leftPartTimeInMeet.seconds >= 600:
                rewardPts = (leftPartTimeInMeet.seconds/600)*5
                leftPart.rewardpoints = rewardPts
                leftPart.save()
            leftPartReward.delete()

            for info in l:
                obj = json.loads(info)
                name = obj['displayName']
                user = User.objects.get(username=name)
                meeting = MeetingInfo.objects.get(slug=roomName)
                userProfInfo = UserProfileInfo.objects.get(user=user)
                rewardinfo = list(RewardInfo.objects.select_related().filter(
                    roomName=meeting, username=user))

                for rewInfo in rewardinfo:
                    lastJoined = rewInfo.lastJoined.replace(tzinfo=None)

                    time_in_meet = curr_time - lastJoined
                    print(time_in_meet)
                    if time_in_meet.seconds < 600:
                        continue
                    else:
                        rewardPts = (time_in_meet.seconds/600)*5
                        userProfInfo.rewardpoints = rewardPts
                        userProfInfo.save()


# do an update on the reward info for a user instead of creating a new one.
    return render(request, 'CLP/meeting.html', context={'page_title': 'CLP | Meeting'})


def showDetails(request, id):
    print("THE ID IS: ", id)
    return render(request, 'CLP/dashboardPopup.html')


def notes(request):

    if request.method == 'POST':
        form = NotesForm(request.POST)
        if form.is_valid():
            notes = Notes(
                user=request.user, title=request.POST['title'], description=request.POST['description'])
            notes.save()
        messages.success(
            request, f"Notes Added from {request.user.username} Successfully!")
    else:
        form = NotesForm()
    notes = Notes.objects.filter(user=request.user).values()
    data = list(Notes.objects.values())
    content = False
    if len(data) != 0:
        content = True
    context = {'notes': notes, 'content': content, 'form': form}
    return render(request, 'CLP/student/notes.html', context)


def delete_note(request, pk=None):
    Notes.objects.get(id=pk).delete()
    return redirect("notes")


class NotesDetailView(generic.detail.DetailView):
    model = Notes
    template_name = 'CLP/student/notes_detail.html'


def homework(request):
    if request.method == 'POST':
        form = HomeworkForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            homeworks = Homework(
                user=request.user,
                subject=request.POST['subject'],
                title=request.POST['title'],
                description=request.POST['description'],
                due=request.POST['due'],
                is_finished=finished
            )
            homeworks.save()
        messages.success(
            request, f"Homeworks Added from {request.user.username} !!")
    else:
        form = HomeworkForm()
    homework = Homework.objects.filter(user=request.user)
    if len(homework) == 0:
        returnhomework_done = True
    else:
        homework_done = False
    context = {'homeworks': homework,
               'homeworks_done': homework_done, 'form': form}
    return render(request, 'CLP/student/homework.html')


def update_homework(request, pk=None):
    homework = Homework.objects.get(id=pk)
    if homework.is_finished == True:
        homework.is_finished = False
    else:
        homework.is_finished = True
    homework.save()
    return redirect('homework')


def delete_homework(request, pk=None):
    Homework.objects.get(id=pk).delete()
    return redirect("homework")


def relax(request):
    rewardPts = 0
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    userObj = User.objects.get(username=request.user)
    try:
        userProf = UserProfileInfo.objects.get(user=userObj)
        rewardPts = userProf.rewardpoints
    except ObjectDoesNotExist:
        rewardPts = 0
    return render(request, 'CLP/relax.html', context={'page_title': 'CLP | Relax', 'rewardPts': rewardPts})


def bubbleshooter(request):
    return render(request, 'CLP/bubbleshooter.html')


def wordle(request):
    return render(request, 'CLP/wordle.html')
