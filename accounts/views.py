#from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login

from .forms import SignUpForm

# def signup(request):
#     form = UserCreationForm()
#     return render(request, 'signup.html', {'form': form})

# def signup(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             auth_login(request, user)
#             return redirect('home')
#     else:
#         form = UserCreationForm()
#     return render(request, 'signup.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})