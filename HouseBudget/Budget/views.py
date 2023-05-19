from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegistrationForm

# Create your views here.
def main_page(request: HttpRequest) -> HttpResponse:
    return render(request, "main_page.html")

def home(request):
    return render(request, 'users/home.html')

def home_1(request):
    return render(request, 'users/main_page_1.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()

            messages.success(request, f'Your account has been created. You can log in now!')
            return redirect('login')
    else:
        form = UserRegistrationForm()

    context = {'form': form}
    return render(request, 'users/register.html', context)