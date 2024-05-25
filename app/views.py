from django.shortcuts import redirect, render

def home (request):
    return render(request, 'home.html')

def login(request):
    if request.method == 'GET':
        return render(request, 'home.html')