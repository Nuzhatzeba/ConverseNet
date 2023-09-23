from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
# Create your views here.

from .models import ConverseNetUser, Profile, Bot_Message, FriendsThread, Requests, FriendsThreadMessage, Diary


# from .forms import ClientForm


def login(request):
    if request.method == 'POST':
        client_email = request.POST['email']
        client_password = request.POST['password']
        if User.objects.filter(email=client_email).exists():
            users = User.objects.filter(email=client_email)
            for user in users:
                if user.password == client_password:
                    messages.success(request, 'Sucessfully Logged In.')
                    return redirect('homepage', user_name=user.username)
                else:
                    messages.error(request, 'Incorrect Password !! ')
        else:
            messages.error(request, 'Username does not exist. ')
    return render(request, 'Home/login.html')


def signup(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        name = first_name + email
        print("here")
        if User.objects.filter(username=name).exists():
            messages.error(request, 'The person with this email is already a member...')
        elif password != confirm_password:
            messages.error(request, 'The passwords do not match...')
        else:
            user = User(password=password, username=name, last_name=last_name, email=email, first_name=first_name)
            user.save()
            user_again = User.objects.all()
            get_user = user_again.get(email=email)
            date_of_birth = request.POST['date_of_birth']
            gender = request.POST['gender']
            client = ConverseNetUser(first_name=first_name, last_name=last_name, email=email, gender=gender,
                                     password=password, Date_Of_Birth=date_of_birth, user_ID=get_user)
            client.save()
            return render(request, 'Home/login.html')
    print("nope here")
    return render(request, 'Home/signup.html')


def chat(request):
    return render(request, 'Home/chat.html')


def botchat(request):
    return render(request, 'Home/bot.html')


def dairy(request):
    return render(request, 'Home/dairy.html', {})


def loadpage(request):
    return render(request, 'Home/loadpage.html', {})
