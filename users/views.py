from django.contrib.auth.decorators import login_required
from django.contrib import auth, messages
# from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from users.forms import UserLoginForm, UserRegistrationForm, ProfileForm

def login(request):
    form = UserLoginForm()
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password) # check in db
            if user:
                auth.login(request, user)
                messages.success(request, '{{user.username}} successfully logged in')
                
                if request.POST.get('next', None): # if not authorized user try to visit profile
                    return redirect(request.POST.get('next')) # '/user/profile/'

                return redirect(reverse('main:index'))
    else:
        form = UserLoginForm()
        
    context = {
        'title': 'Log in',
        'form': form
    }
    return render(request, 'users/login.html', context)

def registration(request):
    form = UserRegistrationForm()
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = form.instance
            auth.login(request, user)
            messages.success(request, f'{user.username} successfully signed up')
            return redirect(reverse('main:index'))
    else:
        form = UserRegistrationForm()
        
    context = {
        'title': 'Registration',
        'form': form
    }
    return render(request, 'users/registration.html', context)

@login_required
def profile(request):
    form = ProfileForm()
    if request.method == 'POST':
        form = ProfileForm(data=request.POST, instance=request.user, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, f'Profile successfully updated')
            return redirect(reverse('user:profile'))
    else:
        form = ProfileForm(instance=request.user)
        
    context = {
        'title': 'Profile',
        'form': form
    }
    return render(request, 'users/profile.html', context)

@login_required
def logout(request):
    messages.warning(request, f'{request.user.username} logged out')
    auth.logout(request)
    return redirect(reverse('main:index'))
