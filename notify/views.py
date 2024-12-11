from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import User
from django.contrib import auth
from django.contrib import messages
from .forms import RegistrationForm, LoginForm
def index(request):
    return render(request, "index.html")

# Create your views here.
def register(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            passwd = form.cleaned_data['password']

            user = User.objects.create_user(username=username, email=email, first_name=first_name,
                                            last_name=last_name, password=passwd)
                
            user.save()
                
            messages.success(request, 'user created with success!')
            return redirect('login')
            
            
    return render(request, "register.html", {'form': form} )


def login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            print('inside if')
            username = form.cleaned_data['username']
            passwd = form.cleaned_data['password']

            try:
                print('inside try\n')
                user = auth.authenticate(request, username=username, password=passwd)
                if user:
                    auth.login(request, user)
                    messages.success(request, 'Login success!')
                    return redirect('index')
            
            except Exception as error:
                print(f'[*] Log Error: {error}')
                messages.error(request, 'Login error')
                return render(request, 'login.html', {'form': form})
        else:
            print(f'[*] form error: {form.errors}')
    return render(request, 'login.html', {'form': form})

def get_all_users(request):
    users = User.objects.all()
    
    response = {
        'users': users.first().username
    }

    return JsonResponse(response)