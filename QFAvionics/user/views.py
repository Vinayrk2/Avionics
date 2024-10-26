from django.shortcuts import render, redirect
from .forms import UserSignUpForm, UserLoginForm
from django.contrib.auth import  authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import  HttpResponse, JsonResponse
from django.contrib import messages
import requests

def signup(request):
    if request.user.is_authenticated :
        return redirect('/')
    if request.method == 'POST':
        form = UserSignUpForm(request.POST, request.FILES)
        try:
            if form.is_valid():
                user = form.save(commit=False)
                user.is_staff = False
                user.save()
                messages.success(request, "Registered Successfully")
                return redirect('login')
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field.capitalize()}: {error}")
                
                return render(request, "signup.html", {"form": form})
                
        except Exception as e:
            return HttpResponse(content=e)

    else:
        form = UserSignUpForm()
        return render(request, "signup.html", {"form": form})
    
def userlogin(request):
    if request.user.is_authenticated :
        return redirect('/')
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_superuser == True:
                    messages.add_message(request, messages.WARNING, "Admin cannot login to user login")
                    return redirect("/")
                messages.add_message(request, messages.WARNING, "Logged in successfully.")
                login(request, user)
                request.session["currency"] = "CAD"
                return redirect("/")
            else:
                raise Exception("Invalid User")
        except Exception as e:
            form = UserLoginForm()
            return render(request, "login.html", {"form":form , "message":e})
    else:
        form = UserLoginForm()
        return render(request, "login.html", {"form": UserLoginForm})
    
@login_required(login_url='/login')
def userprofile(request):
    return render(request, "profile.html")


def userlogout(request):
    logout(request)
    print(request.user)
    return redirect("/")
