from django.shortcuts import render, redirect
from users import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


def registration_view(request):
    if request.method == 'GET':
        context = {
            'form': forms.RegistrationForm()
        }
        return render(request, 'users/registration.html', context)
    elif request.method == 'POST':
        form = forms.RegistrationForm(request.POST)
        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)
            return redirect('/users/login/')
        else:
            context = {
                'form': form
            }
            return render(request, 'users/registration.html', context)


def login_view(request):
    if request.method == 'GET':
        context = {
            'form': forms.LoginForm()
        }
        return render(request, 'users/authentication.html', context)
    elif request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/users/profile/')
            else:
                form.add_error('username', 'ERROR!!!')
                return render(request, 'users/authentication.html', {'form': form})


def profile_view(request):
    context = {
        'user': request.user
    }
    return render(request, 'users/profile.html', context)


def logout_view(request):
    logout(request)
    return redirect('/anime/')