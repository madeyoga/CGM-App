from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate, login
from authentication.forms import LoginForm


# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("/webclient/")

    if request.POST:
        post_form = LoginForm(request.POST)
        if not post_form.is_valid():
            messages.error(request, "Invalid form input, please check username and password!")
            return HttpResponseRedirect("/login/")

        user = authenticate(username=post_form.cleaned_data['input_username'],
                            password=post_form.cleaned_data['input_password'])
        # If valid username and password
        if user is not None:
            login(request, user)
            request.session.set_expiry(86400)
            messages.success(request, "Logged in as " + user.username)
            return HttpResponseRedirect("/webclient/")

        messages.error(request, "Invalid username or password")
        return HttpResponseRedirect("/login/")

    return render(request, "authentication/authentication_login.html")
