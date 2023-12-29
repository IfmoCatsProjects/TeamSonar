from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect


def auth(request):
    return redirect('login')


def log_view(request):
    return render(request, 'auth/login.html')


def reg_view(request):
    return render(request, 'auth/register.html')


def register(request):
    username = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('password')
    new_user = User.objects.create(username, email, password)
    new_user.save()
    return HttpResponseRedirect('/')


def log(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect('/')
    else:
        return HttpResponse("U don't exist")
