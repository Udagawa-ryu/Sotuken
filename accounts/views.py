from django.shortcuts import render,redirect
from .models import *
from .forms import *
from allauth.account.utils import *
from samuraiwalk.settings_common import *
from django.contrib.auth.decorators import login_required

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

@login_required
def UserInfoEdit(request):
    mydata = CustomUser.objects.get(MO1_userNumber = request.user.MO1_userNumber)
    if request.method == 'POST':
        initial_data = {
            "username":request.POST.get("username"),
            "MO1_userID":request.POST.get("MO1_userID"),
            "MO1_homeCountry":request.POST.get("MO1_homeCountry"),
            "MO1_language":request.POST.get("MO1_language"),
            "MO1_openRange":request.POST.get("MO1_openRange"),
        }
        form = UserEditForm(request.POST or initial_data)
        params = {
            'form':form,
            'message' : '',
        }
        return render(request,"UserInfoEdit.html",params)
    else :
        initial_data = {
            "username":mydata.username,
            "MO1_userID":mydata.MO1_userID,
            "MO1_homeCountry":mydata.MO1_homeCountry,
            "MO1_language":mydata.MO1_language,
            "MO1_openRange":mydata.MO1_openRange,
        }
        form = UserEditForm(request.POST or initial_data)
        params = {
            'form':form,
            'message' : '',
        }
        return render(request,"UserInfoEdit.html",params)

@login_required
def UserInfoConfirmation(request):
    if request.method == 'POST':
        initial_data = {
            "username":request.POST.get("username"),
            "MO1_userID":request.POST.get("MO1_userID"),
            "MO1_homeCountry":request.POST.get("MO1_homeCountry"),
            "MO1_language":request.POST.get("MO1_language"),
            "MO1_openRange":request.POST.get("MO1_openRange"),
        }
        if request.POST.get('next', '') == 'confirm':
            form = UserEditForm(initial_data)
            params = {"message":'',"form":form}
            return render(request,"UserInfoConfirmation.html",params)
        if request.POST.get('next', '') == 'back':
            form = UserEditForm(initial_data)
            params = {"message":'',"form":form}
            return render(request,"UserInfoEdit.html",params)
        if request.POST.get('next', '') == 'next':
            form =  UserEditForm(initial_data)
            if form.is_valid():
                mydata = CustomUser.objects.get(MO1_userNumber = request.user.MO1_userNumber)
                mydata.username = request.POST.get("username")
                mydata.MO1_userID = request.POST.get("MO1_userID")
                mydata.MO1_homeCountry = request.POST.get("MO1_homeCountry")
                mydata.MO1_language = request.POST.get("MO1_language")
                mydata.MO1_openRange = request.POST.get("MO1_openRange")
                mydata.save()
                return redirect("accounts:UserInfoComp")

def UserInfoRegister(request):
    return render(request, 'userinforegister.html')

def logout(request):
    return render(request,'logout.html')

def signupcomp(request):
    return render(request,'SingUpCompletion.html')

def UserInfoCompletion(request):
    return render(request,'UserInfoCompletion.html')

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

@login_required
def deleteAccount(request):
    return render(request,'DeleteAccount.html')

@login_required
def AccountDelete(request):
    mydata = CustomUser.objects.get(MO1_userNumber = request.user.MO1_userNumber)
    mydata.is_active = False
    mydata.save()
    return redirect('account_logout')

@login_required
def UserSearch(request):
    params = {'message': '', 'form': None}
    form = UserSearchForm()
    params['form'] = form
    return render(request,"UserSearch.html",params)

@login_required
def UserSearchResult(request):
    if request.method == 'POST':
        users = CustomUser.objects.filter(MO1_userID__contains = request.POST.get("s_user"),is_active=True,is_staff=False)
        params = {'message': '', 'form': None,'users':users}
        return render(request,"UserSearchResult.html",params)

@login_required
def OtherMypage(request):
    if request.method == 'POST':
        page_user = CustomUser.objects.get(MO1_userNumber = request.POST.get("user"))
        mydata = CustomUser.objects.get(MO1_userNumber = request.user.MO1_userNumber)
        if MO9_Fav_Custom_user.objects.filter(MO1_userNumber = mydata.MO1_userNumber,MO9_followedUserNumber = page_user.MO1_userNumber).exists():
            fav = 1
        else :
            fav = 0
        params = {"page_user":page_user,"mydata":mydata,"fav":fav}
        return render(request,"OtherMypage.html",params)

@login_required
def OpenRangeRegister(request):
    mydata = CustomUser.objects.get(MO1_userNumber = request.user.MO1_userNumber)
    if request.method == 'POST':
        range = request.POST.get("demo-priority")
        if range == "0":
            r = 0
        elif range == "1":
            r = 1
        else:
            r = 2
        mydata.MO1_openRange = r
        mydata.save()
    params = {"mydata":mydata}
    return render(request,'OpenRangeRegister.html', params)

@login_required
def FavUser(request):
    if request.method == 'POST':
        print(request.POST.get("fav"))
        if request.POST.get("fav") == "0":
            # page_user = CustomUser.objects.get(MO1_userNumber = request.POST.get("user"))
            page_user = CustomUser.objects.get(MO1_userNumber = request.POST.get("user"))
            mydata = CustomUser.objects.get(MO1_userNumber = request.user.MO1_userNumber)
            initial_data = {
                "MO1_userNumber":mydata,
                "MO9_followedUserNumber":page_user,
            }
            form = FavUserForm(request.POST or initial_data)
            print(form)
            if form.is_valid():
                form.save()
        else :
            mydata = request.POST.get("mydata")
            page_user = request.POST.get("page_user")
            fav_data = MO9_Fav_Custom_user.objects.filter(MO1_userNumber = mydata.MO1_userNumber,MO9_followedUserNumber = page_user.MO1_userNumber)
            fav_data.delete()
    return OtherMypage(request)
