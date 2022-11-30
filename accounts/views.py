from django.shortcuts import render
from .models import *
from .forms import *
from allauth.account.utils import *
from samuraiwalk.settings_common import *


# Create your views here.
def newAccount(request):
    params = {'message': '', 'form': None}
    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            user = form.signup(request)
            return complete_signup(request, user, ACCOUNT_EMAIL_VERIFICATION, ACCOUNT_LOGOUT_REDIRECT_URL)
        else:
            params['message'] = '再入力して下さい'
            params['form'] = form
    else:
        params['form'] = CustomSignupForm()
    return render(request, 'account/signup.html', params)

def UserInfoRegister(request):
    return render(request, 'userinforegister.html')

def logout(request):
    return render(request,'logout.html')

def signupcomp(request):
    return render(request,'SingUpCompletion.html')

def login(request):
    params = {'message':'', 'form': None}
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            user = form.login(request)
        else:
            params['message'] = '再入力して下さい'
            params['form'] = form
    else:
        params['form'] = CustomLoginForm()
    return render(request, 'account/login.html',params)