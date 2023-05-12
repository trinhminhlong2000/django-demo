from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import *
from django.core.mail import send_mail, BadHeaderError
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.db.models.query_utils import Q
from django.contrib.auth import views as auth_views


def dashboard(request):
    user = request.user
    if user.is_authenticated:
        form = DweetForm(request.POST or None)

        if request.method == "POST":
            form = DweetForm(request.POST)
            if form.is_valid():
                dweet = form.save(commit=False)
                dweet.user = request.user
                dweet.save()
                return redirect("dwitter:dashboard")

        followed_dweets = Dweet.objects.filter(
            user__profile__in=request.user.profile.follows.all()
        ).order_by("-created_at")
        return render(request, "dwitter/dashboard.html", {"formz": form, "dweets": followed_dweets, "user": user})
    else:
        return redirect("dwitter:login")


def profile_list(request):
    profiles = Profile.objects.exclude(user=request.user)
    return render(request, "dwitter/profile_list.html", {"profiles": profiles})


def profile(request, xc):
    if not hasattr(request.user, 'profile'):
        missing_profile = Profile(user=request.user)
        missing_profile.save()
    profile = Profile.objects.get(id=xc)
    if request.method == "POST":
        current_user_profile = request.user.profile
        data = request.POST
        action = data.get("follow")
        if action == "follow":
            current_user_profile.follows.add(profile)
        elif action == "unfollow":
            current_user_profile.follows.remove(profile)
        current_user_profile.save()

    return render(request, "dwitter/profile.html", {"profile": profile})


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("dwitter:dashboard")
        else:
            return redirect("dwitter:login")
    else:
        if request.user.is_authenticated:
            return redirect("dwitter:dashboard")
        else:
            form = LoginForm(request.POST or None)
            return render(request, "registration/login.html", {"form": form})


def logout_user(request):
    logout(request)
    return redirect("dwitter:login")


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "password/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'trinhminhlongad@gmail.com',
                                  [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect("password_reset_done")
    password_reset_form = PasswordResetForm()
    return render(request, "registration/password_reset.html", {"password_reset_form": password_reset_form})
