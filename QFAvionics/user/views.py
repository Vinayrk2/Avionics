import random
from django.shortcuts import render, redirect
import math
from .models import CustomUser
from .forms import UserSignUpForm, UserLoginForm
from django.contrib.auth import  authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import  HttpResponse, JsonResponse
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

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

def forgotpassword(request):
    if request.method == "POST":
        try:
            
            if request.POST.get("otp", False):
                otp = request.POST.get("otp")
                if  otp == request.session["otp"]:
                    return render(request, "forgot.html", {"verified":True})
                else:
                    return render(request, "forgot.html", {email:request.session.email})
            email = request.POST.get("email")
            request.session["email"] = email
            user = CustomUser.objects.get(email=email)
            request.session["otp"] = random.randint(100000,999999)
            flag = send_mail(
            subject="QFAvionics @password reset",
            message="Here is the OTP for the password reset. It will expire in 3 minutes<br><h3> OTP : {} </h3>".format(request.session["otp"]),  # This is the plain text version for email clients that can't display HTML
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            html_message="Here is the OTP for the password reset. It will expire in 3 minutes<br><h3> OTP : {} </h3>".format(request.session["otp"]),  # The actual HTML content
            fail_silently=False,
        )
            print("user found")
            if flag:
                messages.add_message(request,  messages.INFO, "OTP has been sent successfully. Check your email.")
            
                return render(request, "forgot.html", {"email": email})
            else:
                messages.add_message(request,  messages.INFO, "Failed to send OTP.")
                return render(request, "forgot.html", {})
        except Exception as e:
            messages.error(request, e)
            print(e)
            return redirect('forgot-password')
    return render(request, "forgot.html",  {})
