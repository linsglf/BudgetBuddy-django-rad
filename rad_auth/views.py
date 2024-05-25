from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate 
from django.contrib.auth import login as auth_login

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
            return redirect('/home')
        else:
            error_message = 'Usuário ou senha inválidos'
            return render(request, 'login.html', {'error_message': error_message, 'username':username})
        

