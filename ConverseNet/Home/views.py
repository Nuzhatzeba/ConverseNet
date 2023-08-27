from django.shortcuts import render

# Create your views here.

def login(request):
    return render(request, 'Home/login.html',{})
def signin(request):
    return render(request,'Home/signin.html',{})

def dairy(request):
    return render(request,'Home/dairy.html',{})

def loadpage(request):
    return render(request,'Home/loadpage.html',{})