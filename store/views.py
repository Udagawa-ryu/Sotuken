from django.shortcuts import redirect,render
from django.views import generic
from .models import *
from .froms import *
from accounts.models import *
from .decorators import *
from django.conf import settings
from django.contrib.auth.hashers import make_password,check_password
from PIL import Image
import qrcode
import base64
from io import BytesIO
# Create your views here.

# 店舗用スポット登録申請画面
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

# 店舗認証
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

# 店舗追加
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

# 店舗用パスワード設定画面
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
                request.session['storeLogin'] = mystore.MO2_mailAdress
                request.session.set_expiry(settings.SESSION_COOKIE_AGE)
                qr = storeQRCreate(mystore.MO2_mailAdress)
                params = {'qr':qr}
                return render(request,'StoreQR.html',params)
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
            if user.is_active == False:
                params['form'] = StoreLoginForm()
                params['message'] = "店舗登録が解除されています。"
                return render(request,'StoreLogin.html',params)
            else:
                if check_password(ps,user.MO2_password):
                    request.session['storeLogin'] = user.MO2_mailAdress
                    request.session.set_expiry(settings.SESSION_COOKIE_AGE)
                    return render(request,'storeMypage.html',{'mystore':user})
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

@login_required_store
def IndexView(request,mail):
    mystore = MO2_store.objects.get(MO2_mailAdress = mail)
    params = {
        'mystore':mystore,
        'message':''
    }
    return render(request,'StoreMypage.html',params)

@login_required_store
def storeInfoEditView(request,mail):
    mystore = MO2_store.objects.get(MO2_mailAdress = mail)
    if request.method == 'POST':
        initial_data = {
            "MO2_storeName":request.POST.get('MO2_storeName'),
            "MO2_storeInfo":request.POST.get('MO2_storeInfo'),
            "MO2_phoneNumber":request.POST.get('MO2_phoneNumber'),
            "MO2_address":request.POST.get('MO2_address'),
            "MO2_images1":request.POST.get('MO2_images1'),
            "MO2_images2":request.POST.get('MO2_images2'),
            "MO2_images3":request.POST.get('MO2_images3'),
        }
        form = StoreUpdateForm(request.POST or initial_data)
        params = {
            'form':form,
            'message' : '',
        }
        return render(request,"StoreInfoEdit.html",params)
    else :
        initial_data = {
            "MO2_storeName":mystore.MO2_storeName,
            "MO2_storeInfo":mystore.MO2_storeInfo,
            "MO2_phoneNumber":mystore.MO2_phoneNumber,
            "MO2_address":mystore.MO2_address,
            "MO2_images1":mystore.MO2_images1,
            "MO2_images2":mystore.MO2_images2,
            "MO2_images3":mystore.MO2_images3,
        }
        form = StoreUpdateForm(request.POST or initial_data)
        params = {
            'form':form,
            'message' : '',
        }
        return render(request,"StoreInfoEdit.html",params)
# 店舗用情報編集画面
@login_required_store
def storeInfoConfirmationView(request,mail):
    if request.method == 'POST':
        initial_data = {
            "MO2_storeName":request.POST.get('MO2_storeName'),
            "MO2_storeInfo":request.POST.get('MO2_storeInfo'),
            "MO2_phoneNumber":request.POST.get('MO2_phoneNumber'),
            "MO2_address":request.POST.get('MO2_address'),
            "MO2_images1":request.POST.get('MO2_images1'),
            "MO2_images2":request.POST.get('MO2_images2'),
            "MO2_images3":request.POST.get('MO2_images3'),
        }
        if request.POST.get('next', '') == 'confirm':
            form = StoreUpdateForm(initial_data)
            params = {"message":'',"form":form}
            return render(request,"StoreInfoConfirmation.html",params)
        if request.POST.get('next', '') == 'back':
            form = StoreUpdateForm(initial_data)
            params = {"message":'',"form":form}
            return render(request,"StoreInfoEdit.html",params)
        if request.POST.get('next', '') == 'next':
            form = StoreUpdateForm(initial_data)
            if form.is_valid():
                mystore = MO2_store.objects.get(MO2_mailAdress = mail)
                mystore.MO2_storeName = request.POST.get('MO2_storeName')
                mystore.MO2_storeInfo = request.POST.get('MO2_storeInfo')
                mystore.MO2_phoneNumber = request.POST.get('MO2_phoneNumber')
                mystore.MO2_address = request.POST.get('MO2_address')
                mystore.MO2_images1 = request.POST.get('MO2_images1')
                mystore.MO2_images2 = request.POST.get('MO2_images2')
                mystore.MO2_images3 = request.POST.get('MO2_images3')
                mystore.save()
                return redirect("store:storeinfocomp")

class storeinfocompletionView(generic.TemplateView):
    template_name = "StoreInfoCompletion.html"

@login_required_store
def storeQRView(request,mail):
    qr = storeQRCreate(mail)
    return render(request,"StoreQR.html",{"qr":qr})

def storeQRCreate(mail):
    qr_str = "store:"+mail
    img = qrcode.make(qr_str)
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    qr = base64.b64encode(buffer.getvalue()).decode().replace("'", "")
    return qr

@login_required_store
def storeLogout(request,mail):
    request.session.pop('storeLogin')
    return redirect('store:storeLogin')
class storeLogoutView(generic.TemplateView):
    template_name = "StoreLogout.html"

# class storeinfodeleteconfView(generic.TemplateView):
#     template_name = 'StoreInfoDeleteConfirmation.html'

@login_required_store
def storeinfodeleteconfView(requset,mail):
    mystore = MO2_store.objects.get(MO2_mailAdress = mail)
    return render(requset,"StoreInfoDeleteConfirmation.html",{"mystore":mystore})

@login_required_store
def storeinfodelete(request,mail):
    mystore = MO2_store.objects.get(MO2_mailAdress = mail)
    mystore.is_active = False
    mystore.save()
    request.session.pop('storeLogin')
    return redirect('store:storeRequest')