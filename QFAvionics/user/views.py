from django.shortcuts import render, redirect
from .models import CustomUser
from .forms import UserSignUpForm, UserLoginForm
from django.contrib.auth import  authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import  HttpResponse, JsonResponse
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes


def signup(request):
    if request.user.is_authenticated :
        return redirect('/')
    if request.method == 'POST':
        form = UserSignUpForm(request.POST, request.FILES)
        try:
            if form.is_valid():
                user = form.save(commit=False)
                user.is_staff = False
                user.is_active = False
                user.save()
                send_verification_email(user, request)
                messages.success(request, "Registered Successfully.")
                messages.add_message(request, messages.INFO, "We have sent verification link to your email. Please verify your email to login.")

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
            print(user)
            if user is None:
                user = CustomUser.objects.filter(email=username).first()
                print("user found with email")
                if user:
                    if user.check_password(password):   
                        user = user
                    else:
                        user = None 
            
            if user is not None:
                if user.is_superuser == True:
                    messages.add_message(request, messages.WARNING, "Admin cannot login to user login")
                    return redirect("/")
                elif not user.is_active:
                    send_verification_email(user, request)
                    raise Exception("Please Verify your email first, we have sent you email on your registered email") 
                    return redirect("login")
                    
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


def send_verification_email(user, req):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    verification_link = "{}://{}/verify/{}/{}/".format( req.scheme,  req.get_host(), uid, token)
    send_mail(
        "Email Verification",
        f"Click here to verify your email: {verification_link}",
        "no-reply@qfavionics.com",
        [user.email],
    )



User = get_user_model()

def verify_email(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('login')
    else:
        return render(request, 'registration/verification_failed.html')
