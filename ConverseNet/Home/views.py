from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
# Create your views here.

from .models import ConverseNetUser, Profile, Bot_Message, FriendsThread, Requests, FriendsThreadMessage, Diary
# from .forms import ClientForm


def index(request):
    return render(request, "Home/index.html", {})

def login(request):
    return render(request, 'Home/login.html',{})
def signin(request):
    return render(request,'Home/signin.html',{})

def dairy(request):
    return render(request,'Home/dairy.html',{})

def loadpage(request):
    return render(request,'Home/loadpage.html',{})