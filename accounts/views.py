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
    COUNTRIES = {
        ("USA","USA"),
        ("JAPAN","日本"),
        ("Germany","Deutschland"),
        ("Italy","Italia"),
        ("France","France"),
        ("Spain","España"),
        ("Portuguese","Português"),
        ("China","中国"),
    }
    LANGAGES = {
        ("en","English"),
        ("ja","日本語"),
        ("de","Deutsch"),
        ("it","Italiano"),
        ("fr","Français"),
        ("es","Español"),
        ("pl","Português"),
        ("zh-CN","中国人"),
    }
    if request.method == 'POST':
        initial_data = {
            "username":request.POST.get("username"),
            "MO1_userID":request.POST.get("MO1_userID"),
            "MO1_homeCountry":request.POST.get("MO1_homeCountry"),
            "MO1_language":request.POST.get("MO1_language"),
        }
        form = UserEditForm(request.POST,instance=mydata)
        form.fields['MO1_homeCountry'].choices = COUNTRIES
        form.fields['MO1_language'].choices = LANGAGES
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
        }
        form = UserEditForm(request.POST or initial_data,instance=mydata)
        form.fields['MO1_homeCountry'].choices = COUNTRIES
        form.fields['MO1_language'].choices = LANGAGES
        params = {
            'form':form,
            'message' : '',
        }
        return render(request,"UserInfoEdit.html",params)

@login_required
def UserInfoConfirmation(request):
    mydata = CustomUser.objects.get(MO1_userNumber = request.user.MO1_userNumber)
    if request.method == 'POST':
        COUNTRIES = {
            ("USA","USA"),
            ("JAPAN","日本"),
            ("Germany","Deutschland"),
            ("Italy","Italia"),
            ("France","France"),
            ("Spain","España"),
            ("Portuguese","Português"),
            ("China","中国"),
        }
        LANGAGES = {
            ("en","English"),
            ("ja","日本語"),
            ("de","Deutsch"),
            ("it","Italiano"),
            ("fr","Français"),
            ("es","Español"),
            ("pl","Português"),
            ("zh-CN","中国人"),
        }
        initial_data = {
            "username":request.POST.get("username"),
            "MO1_userID":request.POST.get("MO1_userID"),
            "MO1_homeCountry":request.POST.get("MO1_homeCountry"),
            "MO1_language":request.POST.get("MO1_language"),
        }
        for i in COUNTRIES:
            if i[0] == request.POST.get("MO1_homeCountry"):
                co = i[1]
        for i in LANGAGES:
            if i[0] == request.POST.get("MO1_language"):
                lang = i[1]
        if request.POST.get('next', '') == 'confirm':
            form = UserEditForm(request.POST or initial_data,instance=mydata)
            form.fields['MO1_homeCountry'].choices = COUNTRIES
            form.fields['MO1_language'].choices = LANGAGES
            params = {"message":'',"form":form,"co":co,"lang":lang}
            return render(request,"UserInfoConfirmation.html",params)
        if request.POST.get('next', '') == 'back':
            form = UserEditForm(request.POST or initial_data,instance=mydata)
            form.fields['MO1_homeCountry'].choices = COUNTRIES
            form.fields['MO1_language'].choices = LANGAGES
            params = {"message":'',"form":form}
            return render(request,"UserInfoEdit.html",params)
        if request.POST.get('next', '') == 'next':
            mydata = CustomUser.objects.get(MO1_userNumber = request.user.MO1_userNumber)
            form =  UserEditForm(request.POST or initial_data,instance=mydata)
            form.fields['MO1_homeCountry'].choices = COUNTRIES
            form.fields['MO1_language'].choices = LANGAGES
            print(form.is_valid())
            if form.is_valid():
                mydata.username = request.POST.get("username")
                mydata.MO1_userID = request.POST.get("MO1_userID")
                mydata.MO1_homeCountry = request.POST.get("MO1_homeCountry")
                mydata.MO1_language = request.POST.get("MO1_language")
                mydata.save()
                return redirect("accounts:UserInfoComp")
    params = {
        'form':form,
    }
    return render(request,"UserInfoEdit.html",params)

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
    return redirect('account_signup')

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
        mydata.MO1_openRange = r
        mydata.save()
    params = {"mydata":mydata}
    return render(request,'OpenRangeRegister.html', params)

@login_required
def FavUser(request):
    if request.method == 'POST':
        page_user = CustomUser.objects.get(MO1_userNumber = request.POST.get("user"))
        mydata = CustomUser.objects.get(MO1_userNumber = request.user.MO1_userNumber)
        result, created =MO9_Fav_Custom_user.objects.get_or_create(MO1_userNumber=mydata,MO9_followedUserNumber=page_user)
        if created :
            return OtherMypage(request)
        else:
            result.delete()
            return OtherMypage(request)
    return OtherMypage(request)
