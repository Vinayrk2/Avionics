from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from django.shortcuts import render
from .forms import UserSignUpForm, UserLoginForm
from django.contrib.auth import  authenticate, login, logout
from django.contrib.auth.decorators import login_required


# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = UserSignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = False
            if 'image' in request.FILES:
                user.image = request.FILES['image']
            user.save()
            return HttpResponsePermanentRedirect("/login")
    else:
        form = UserSignUpForm()
        return render(request, "signup.html", {"form": form})
    
def userlogin(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect("/")
            else:
                raise Exception("Invalid User")
        except Exception as e:
            print(e)
            form = UserLoginForm()
            return render(request, "login.html", {"form":form , "message":e})
    else:
        form = UserLoginForm()
        return render(request, "login.html", {"form": UserLoginForm})
    
@login_required(login_url='/login')
def userprofile(request):
    return render(request, "profile.html")

@login_required(login_url='/login')
def usercart(request):
    return render(request, "cart.html")

@login_required(login_url='/login')
def userlogout(request):
    logout(request)
    return HttpResponseRedirect("/")