from django.shortcuts import redirect,render
from django.views import generic
from .models import *
from .froms import *
from accounts.models import *
from maps.models import MO3_Default_spot
from .decorators import *
from django.conf import settings
from django.contrib.auth.hashers import make_password,check_password
from django.core.mail import send_mail
from PIL import Image
from django.utils import timezone
import matplotlib.pyplot as plt
import qrcode
from django.db.models import Sum,Count
import base64
from io import BytesIO
from maps.models import MO5_Tag
from django.db import connection
import os
from samuraiwalk.settings import MEDIA_URL,MEDIA_ROOT
import datetime

# Create your views here.

# 店舗用スポット登録申請画面
def storeRequest(request):
    params = {'message': '仮登録が完了しました。メールが届くまでお待ちください。', 'form': None,}
    if request.method == 'POST':
        form = StoreCreateForm(request.POST,request.FILES)
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
            i.is_auth = True
            i.save()
            result, created =MO3_Default_spot.objects.get_or_create(MO2_storeNumber=i)
            if created:
                # url = "http://localhost:8000/store/storePassRegister/"+str(i.MO2_mailAdress)
                url = "https://samuraiwalk.sytes.net/store/storePassRegister/"+str(i.MO2_mailAdress)
                subject = "認証が完了しました。以下のURLよりパスワードを設定してください。"
                message = url
                from_email = "admin@mail.com"  # 送信者
                recipient_list = [i.MO2_mailAdress]  # 宛先リスト
                send_mail(subject, message, from_email, recipient_list)
                lngs = ["en","de","it","fr","es","pl","zh-CN"]
                for lng in lngs:
                    t=translator.translate(str(i.MO2_storeName),dest=lng, src="auto").text
                    MO12_storeEng.objects.create(MO2_storeNumber=i,MO12_storeNameLng=lng,MO12_storeNameEng=t)
            else:
                subject = "認証に失敗しました。"
                message = "登録されたメールアドレスはすでに使用されている可能性がございます。"
                from_email = "admin@mail.com"  # 送信者
                recipient_list = [i.MO2_mailAdress]  # 宛先リスト
                send_mail(subject, message, from_email, recipient_list)
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
                return redirect("store:storeQR")
            else:
                params['message'] = '再入力して下さい'
                params['form'] = StorePassCreateForm()
                return render(request, 'StorePassRegister.html', params)
    else:
        params['form'] =  StorePassCreateForm()
        params['message'] = ''
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
                    return render(request,'StoreMypage.html',{'mystore':user})
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

def storeChangePasswordresister(request):
    params = {'message': '', 'form': None}
    if request.method == 'POST':
        if MO2_store.objects.filter(MO2_mailAdress=request.POST.get("mail")).exists():
            store = MO2_store.objects.get(MO2_mailAdress=request.POST.get("mail"))
            if store.is_active == False:
                params['message'] = "店舗登録が解除されています。"
                return render(request,'StorePassChange.html',params)
            else:
                # url = "http://localhost:8000/store/storePassform/"+str(store.MO2_mailAdress)
                url = "https://samuraiwalk.sytes.net/store/storePassform/"+str(store.MO2_mailAdress)
                subject = "以下より新しいパスワードを設定してください。"
                message = url
                from_email = "admin@mail.com"  # 送信者
                recipient_list = [store.MO2_mailAdress]  # 宛先リスト
                send_mail(subject, message, from_email, recipient_list)
                params['message'] = "メールアドレスにパスワード再設定用リンクを送りました。"
                return render(request,'storepassmail.html',params)
        else:
            params['form'] = StorePassCreateForm()
            params['message'] = "そのメールアドレスは登録されていません。"
            return render(request,'StorePassChange.html',params)
    else:
        params['form'] = None
        params['message'] = "メールアドレスを入力してください"
        return render(request,'StorePassChange.html',params)

def storePassChangeform(request,mail):
    store = MO2_store.objects.get(MO2_mailAdress=mail)
    params = {'message': '', 'form': None,'store':store,"flg":0}
    if request.method == 'POST':
        form = StorePassCreateForm(request.POST)
        if request.POST['password1'] != request.POST['password2']:
            params['message'] = "入力された二つのパスワードが違います。再入力してください。"
            params['form'] =  StorePassCreateForm()
            return render(request, 'StorePassform.html', params)
        else:
            if form.is_valid():
                en_pass = make_password(request.POST['password1'])
                store.MO2_password = en_pass
                store.save()
                params['message'] = "パスワード変更が完了しました。"
                params['flg'] = 1
                return render(request, 'StorePassform.html', params)
            else:
                params['message'] = '再入力して下さい'
                params['form'] = StorePassCreateForm()
                return render(request, 'StorePassRegister.html', params)
    else:
        params['form'] = StorePassCreateForm()
        params['message'] = '新しいパスワードを入力してください'
        return render(request,'StorePassform.html',params)

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
        if mystore.MO2_storeName != request.POST.get("MO2_storeName"):
            namechange(mystore.MO2_storeNumber,request.POST.get("MO2_storeName"))
        form = StoreUpdateForm(request.POST,request.FILES,instance=mystore)
        if form.is_valid():
            form.save()
            return redirect("store:storeinfocomp")
        else:
            initial_data = {
                "MO2_storeName":mystore.MO2_storeName,
                "MO2_storeInfo":mystore.MO2_storeInfo,
                "MO2_phoneNumber":mystore.MO2_phoneNumber,
                "MO2_address":mystore.MO2_address,
                "MO2_images1":mystore.MO2_images1,
                "MO2_images2":mystore.MO2_images2,
                "MO2_images3":mystore.MO2_images3,
            }
            form = StoreUpdateForm(initial_data,instance=mystore)
            params = {
                'form':form,
                'message' : '編集できませんでした',
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
        form = StoreUpdateForm(initial_data,instance=mystore)
        params = {
            'form':form,
            'message' : '',
        }
        return render(request,"StoreInfoEdit.html",params)

def namechange(store,n_name):
    mystore = MO2_store.objects.get(MO2_storeNumber = store)
    new_add = MEDIA_ROOT[0]+"/store_images/"+n_name
    old_add = MEDIA_ROOT[0]+"/store_images/"+mystore.MO2_storeName
    os.rename(old_add,new_add)
    mystore.save()
    item = MO12_storeEng.objects.filter(MO2_storeNumber=mystore)
    for i in item:
        new_trance = translator.translate(str(n_name),dest=i.MO12_storeNameLng, src="auto").text
        i.MO12_storeNameEng = new_trance
        i.save()

class storeinfocompletionView(generic.TemplateView):
    template_name = "StoreInfoCompletion.html"

@login_required_store
def storeQRView(request,mail):
    qr = store_visit_QRCreate(mail)
    qr2 = store_point_QRCreate(mail)
    return render(request,"StoreQR.html",{"qr":qr,"qr2":qr2})

def store_visit_QRCreate(num):
    dt_now = datetime.datetime.now()
    date = dt_now.strftime('%Y-%m-%d')
    # qr_str = "http://localhost:8000/visitrecord/"+str(num)+"/"+date
    qr_str = "https://samuraiwalk.sytes.net/visitrecord/"+str(num)+"/"+date
    img = qrcode.make(qr_str)
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    qr = base64.b64encode(buffer.getvalue()).decode().replace("'", "")
    return qr
def store_point_QRCreate(num):
    dt_now = datetime.datetime.now()
    date = dt_now.strftime('%Y-%m-%d')
    # qr_str = "http://localhost:8000/PointInput/"+str(num)+"/"+date
    qr_str = "https://samuraiwalk.sytes.net/PointInput/"+str(num)
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

@login_required_store
def statistics(request,mail):
    mystore = MO2_store.objects.get(MO2_mailAdress = mail)
    dspot = MO3_Default_spot.objects.get(MO2_storeNumber=mystore.MO2_storeNumber)
    print("dspot = ",dspot)
    visiter_country = MO6_Visit_record.objects.filter(MO3_DspotNumber=dspot).select_related().values(
        'MO1_userNumber__MO1_homeCountry'
    ).annotate(
        total=Count('MO1_userNumber__MO1_homeCountry')
    ).order_by('total')
    image2 = plt_circle(visiter_country)
    datedata=get_datedata()
    count = []
    date_f = []
    for i in datedata:
        visiter_count = MO6_Visit_record.objects.filter(
            MO3_DspotNumber=dspot,MO6_visitDate__gte=i[0],MO6_visitDate__lt=i[1],
        ).count()
        count.append(visiter_count)
        date_f.append("{:02}月{:02}日".format(i[0].month,i[0].day))
    count = list(reversed(count))
    date_f = list(reversed(date_f))
    image = Plot_Graph(date_f,count)
    params = {
        'store':mystore,
        'image':image,
        'image2':image2
    }
    return render(request,"Statistics.html",params)


import datetime 
from dateutil.relativedelta import relativedelta
def get_datedata():
    now = timezone.now()
    # date = [[now+1,now-6],[2023-01-15,2023-01-21]]
    # 今日の日時を取得   
    current_day = timezone.now() + relativedelta(hours=+9)
    # 今週の日曜日の日時を取得    
    current_day_of_sunday = current_day + relativedelta(days=6-datetime.date.today().weekday())
    array = []
    for i in range(8):
        one_week_ago = current_day_of_sunday + relativedelta(weeks=-1)
        array.append([one_week_ago,current_day_of_sunday-relativedelta(days=1)])
        current_day_of_sunday = one_week_ago
    return array

def plt_circle(visiter):
    data = []
    labels = []
    for i in visiter:
        data.append(i['total'])
        labels.append(i['MO1_userNumber__MO1_homeCountry'])
    # create figure
    fig, ax = plt.subplots()
    plt.rcParams['font.family'] = 'Yu Gothic'
    ax.pie(data, #データ
                 startangle=90, #円グラフ開始軸を指定
                 labels=labels, #ラベル
                 autopct="%1.1f%%",#パーセント表示
                 counterclock=False, #逆時計回り
                )
    ax.axis("equal")
    image = Output_Graph()
    return image

def Plot_Graph(x,y):
	plt.switch_backend("AGG")        #スクリプトを出力させない
	plt.figure(figsize=(10,5))       #グラフサイズ
	plt.bar(x,y)                     #グラフ作成
	plt.xticks(rotation=45)          #X軸値を45度傾けて表示
	plt.xlabel("beginning of the week")               #xラベル
	plt.ylabel("visiter")             #yラベル
	plt.tight_layout()               #レイアウト
	graph = Output_Graph()           #グラフプロット
	return graph

def Output_Graph():
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    img = buffer.getvalue()
    graph = base64.b64encode(img)
    graph = graph.decode("utf-8")
    buffer.close()
    return graph

@login_required_store
def store_tag(request,mail):
    store = MO2_store.objects.get(MO2_mailAdress=mail)
    dspot = MO3_Default_spot.objects.get(MO2_storeNumber=store)
    mytags = dspot.MO5_tagNumber.all()
    mytags_id = dspot.MO5_tagNumber.all().values_list('MO5_tagNumber', flat=True)
    alltags = MO5_Tag.objects.all().exclude(MO5_tagNumber__in=mytags_id)
    params = {
        "store":store,
        "mytags":mytags,
        "tags":alltags,
        "now":dspot,
    }
    return render(request,"Storetag.html",params)

@login_required_store
def addtag(request,mail):
    tagnum = request.POST.getlist("add")
    taglist = MO5_Tag.objects.filter(MO5_tagNumber__in=tagnum)
    store = MO2_store.objects.get(MO2_mailAdress=mail)
    dspot = MO3_Default_spot.objects.get(MO2_storeNumber=store)
    for i in taglist:
        dspot.MO5_tagNumber.add(i)
    store.save()
    return store_tag(request)

@login_required_store
def subtag(request,mail):
    tagnum = request.POST.getlist("sub")
    taglist = MO5_Tag.objects.filter(MO5_tagNumber__in=tagnum)
    store = MO2_store.objects.get(MO2_mailAdress=mail)
    dspot = MO3_Default_spot.objects.get(MO2_storeNumber=store)
    for i in taglist:
        dspot.MO5_tagNumber.remove(i)
    store.save()
    return store_tag(request)

# 翻訳APIをインポート
from googletrans import Translator
# Translatorクラスのインスタンスを生成
translator = Translator()

@login_required_store
def kari(request,mail):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM store_mo12_storeeng;")
    cursor.execute("TRUNCATE TABLE store_mo12_storeeng RESTART IDENTITY;")
    d_spot = list(MO3_Default_spot.objects.values_list("MO2_storeNumber",flat=True))
    print(d_spot)
    store = MO2_store.objects.filter(MO2_storeNumber__in=d_spot)
    lngs = ["en","de","it","fr","es","pl","zh-CN"]
    for i in store:
        for lng in lngs:
            t=translator.translate(str(i.MO2_storeName),dest=lng, src="auto").text
            MO12_storeEng.objects.create(MO2_storeNumber=i,MO12_storeNameLng=lng,MO12_storeNameEng=t)
    return render(request,"karioki.html")