from django.shortcuts import redirect,render
from django.views import generic
from .models import *
from .froms import *
from accounts.models import *
# import cryptocode
from samuraiwalk.settings_dev import *
from django.contrib.auth.hashers import make_password,check_password
# Create your views here.

class IndexView(generic.TemplateView):
    template_name= "StoreMypage.html"


def storeRequest(request):
    params = {'message': '仮登録が完了しました。メールが届くまでお待ちください。', 'form': None,}
    if request.method == 'POST':
        form = StoreCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'StoreRequest.html', params)
        else:
            params['message'] = '再入力して下さい'
            params['form'] = form
            return render(request, 'StoreRequest.html', params)
    else:
        params['form'] =  StoreCreateForm()
        params['message'] = ''
        return render(request, 'StoreRequest.html', params)

def storeCertification(request):
    if request.user.is_superuser == True:
        nocompstore = MO2_store.objects.filter(is_auth=False)
        compstore = MO2_store.objects.filter(is_auth=True)
        params = {
            "noauth" : nocompstore,
            "auth" : compstore,
        }
        return render(request, 'StoreCertification.html', params)
    else:
        return redirect('admin:login')

def addStore(request):
    storeNums = request.POST.getlist('add')
    if storeNums != []:
        for num in storeNums:
            i = MO2_store.objects.get(MO2_storeNumber=num)
            # str_encoded = cryptocode.encrypt(str(i.MO2_storeNumber),"samurai")
            # url = "http://localhost:8000/store/storePassRegister/"+str_encoded+"/"
            url = "http://localhost:8000/store/storePassRegister/"+str(i.MO2_mailAdress)
            subject = "認証が完了しました。以下のURLよりパスワードを設定してください。"
            message = url
            from_email = DEFAULT_FROM_EMAIL  # 送信者
            recipient_list = [i.MO2_mailAdress]  # 宛先リスト
            send_mail(subject, message, from_email, recipient_list)
            i.is_auth = True
            i.save()
    return redirect('store:storeCertification')


def StorePassRegister(request,store):
    mystore = MO2_store.objects.get(MO2_mailAdress=store)
    params = {'message': '', 'form': None,'store':mystore}
    if request.method == 'POST':
        form = StorePassCreateForm(request.POST)
        if request.POST['password1'] != request.POST['password2']:
            params['message'] = "入力された二つのパスワードが違います。再入力してください。"
            params['form'] =  StorePassCreateForm()
            return render(request, 'StorePassRegister.html', params)
        else :
            if form.is_valid():
                en_pass = make_password(request.POST['password1'])
                mystore.MO2_password = en_pass
                mystore.is_active = True
                mystore.save()
                params['message'] = "入力が完了しました。"
                return render(request, 'index.html', params)
            else:
                params['message'] = '再入力して下さい'
                params['form'] = StorePassCreateForm()
                return render(request, 'StorePassRegister.html', params)
    else:
        params['form'] =  StorePassCreateForm()
        params['message'] = 'getされました'
        return render(request, 'StorePassRegister.html', params)

def storeLogin(request):
    params = {'message': '', 'form': None}
    if request.method == 'POST':
        ma = request.POST['MO2_mailAdress']
        ps = request.POST['MO2_password']
        if MO2_store.objects.filter(MO2_mailAdress = ma).exists():
            user = MO2_store.objects.get(MO2_mailAdress = ma)
            if check_password(ps,user.MO2_password):
                params['form'] = StoreLoginForm()
                params['message'] = "ログイン可能セッション処理記述中"
                return render(request,'StoreLogin.html',params)
            else:
                params['form'] = StoreLoginForm()
                params['message'] = "パスワードが違います"
                return render(request,'StoreLogin.html',params)
        else:
            params['form'] = StoreLoginForm()
            params['message'] = "そのメールアドレスは登録されていません。"
            return render(request,'StoreLogin.html',params)
    else:
        params['form'] = StoreLoginForm()
        params['message'] = ''
        return render(request,'StoreLogin.html',params)
    return render(request,'StoreLogin.html',params)

def storeinfocompletion(request):
    template_name = "StoreInfoCompletion.html"