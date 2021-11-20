from django.shortcuts import redirect,render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render
from .forms import ApplicationForm,LogInForm

#from .helpers import login_prohibited

def home(request):
    return render(request, 'home.html')

def feed(request):
    return render(request, 'feed.html')

def Application(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('feed')
    else:
        form = ApplicationForm()
    return render(request, 'Application.html', {'form': form})