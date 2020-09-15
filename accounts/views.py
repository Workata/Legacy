from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages

# Create your views here.

def logout(request):
    auth.logout(request)
    return redirect('/')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username = username, password = password)  # returns none when there is no such user in db

        if user is not None:
            auth.login(request, user) # login access to the user
            return redirect('/')
        else:
            messages.info(request,'Invalid credentials')
            return redirect('login')
    else:   # method = GET
        return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']

        if password1 != password2:
            return render(request, 'register.html',{'passNotEqual': True})
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html',{'usernameTaken': True})
        if User.objects.filter(email=email).exists():
            return render(request, 'register.html',{'emailExists': True})

        user = User.objects.create_user(username=username, password= password1, email=email, first_name = first_name, last_name = last_name)
        user.save()

        return  redirect('/')   # back to login (home page)

    else:
        return render(request, 'register.html')