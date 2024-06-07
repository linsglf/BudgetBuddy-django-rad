import os
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate 
from django.contrib.auth import login as auth_login
from datetime import datetime


def logging(filename, message):
    file = open(filename, 'a')
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file.write(f"{now} - {message}\n")
    file.close()

def cadastro(request):
    if request.method == 'GET':
        return render(request, 'cadastro.html')
    else:
        name = request.POST.get('name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = User.objects.filter(username=username).first()

        if user:
            return HttpResponse('Usuário já cadastrado')

        user = User.objects.create_user(username=username, email=email, password=password, first_name=name)
        user.save()

        logging('registration_log.txt', f"User Registered: {username}, Email: {email}, Name: {name}")

        return redirect('/auth/login')


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            auth_login(request, user)
            logging('login_attempts.txt', f"SUCCESS - Username: {username}")
            return redirect('/home')
        else:
            logging('login_attempts.txt', f"FAILURE - Username: {username}")
            error_message = 'Usuário ou senha inválidos'
            return render(request, 'login.html', {'error_message': error_message, 'username':username})
        

