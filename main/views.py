from django.shortcuts import render,redirect
from django.views import generic
from blog.models import MO7_Blog,MO10_Fav_Blog,MO9_Fav_Custom_user
from maps.models import MO3_Default_spot
from store.models import MO2_store
from accounts.models import CustomUser,MO6_Visit_record
from main.models import MO11_Pointrecord
from django.urls import reverse_lazy
from .forms import *
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
# Create your views here.

# マイページ画面
def MypageView(request):
    return render(request, 'Mypage.html')

# ポイント画面
# class PointView(generic.TemplateView):
@login_required
def PointView(request):
    params = {}
    mydata = CustomUser.objects.get(MO1_userNumber=request.user.MO1_userNumber)
    record = MO11_Pointrecord.objects.filter(MO1_userNumber=request.user.MO1_userNumber).order_by("MO11_createDate").reverse()
    page_obj = paginate_queryset(request, record,3)
    params["object"] = mydata
    params["record"] = page_obj.object_list
    params["page_obj"] = page_obj
    return render(request, "Point.html", params)

def paginate_queryset(request, queryset, count):
    """Pageオブジェクトを返す。

    ページングしたい場合に利用してください。

    countは、1ページに表示する件数です。
    返却するPgaeオブジェクトは、以下のような感じで使えます。

        {% if page_obj.has_previous %}
          <a href="?page={{ page_obj.previous_page_number }}">Prev</a>
        {% endif %}

    また、page_obj.object_list で、count件数分の絞り込まれたquerysetが取得できます。s
    """
    paginator = Paginator(queryset, count)
    page = request.GET.get('page')
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return page_obj


# 使用ポイント画面
@login_required
def PointConfirmationView(request):
    mydata = CustomUser.objects.get(MO1_userNumber=request.user.MO1_userNumber)
    if request.method == 'POST':
        print("num =",request.POST.get("store"))
        store = MO2_store.objects.get(MO2_storeNumber=request.POST.get("store"))
        subpoint = request.POST.get("point")
        data = {"point": subpoint}
        form = PointForm(data)
        params = {"form": form, "mydata":mydata,"store":store}
        if request.POST.get('next', '') == 'comfirm':
            return render(request, 'PointConfirmation.html', params)
        if request.POST.get('next', '') == 'back':
            return render(request, 'PointInput.html', params)
        if request.POST.get('next', '') == 'next':
            mypoint = mydata.MO1_point
            mydata.MO1_point = mypoint - int(subpoint)
            MO11_Pointrecord.objects.create(MO1_userNumber=mydata,MO2_storeNumber=store,MO11_pointSize=0-int(subpoint))
            mydata.save()
            return render(request, "PointDisplay.html",params)


# 使用ポイント提示画面
@login_required
def PointDisplayView(request):
    return render(request, "PointDisplay.html")

# 使用ポイント入力画面
@login_required
def PointInputView(request,mail):
    mydata = CustomUser.objects.get(MO1_userNumber=request.user.MO1_userNumber)
    store = MO2_store.objects.get(MO2_mailAdress=mail)
    # post
    if request.method== 'POST':
        subpoint = request.POST.get("point")
        data = {"point": subpoint}
        form = PointForm(data)
        params = {"form": form, "mydata":mydata,"store":store}
        return render(request, "PointInput.html", params)
    # get
    else :
        form = PointForm()
        params = {"form": form, "mydata":mydata,"store":store}
        return render(request, "PointInput.html", params)

# 店舗用QRコード読み取り画面
@login_required
def StoreQRreadView(request):
    return render(request, "StoreQRread.html")

# 訪問記録用QRコード読み取り画面
@login_required
def VisitQRreadView(request):
    return render(request, "VisitQRread.html")

# お気に入りブログ一覧画面
@login_required
def FavoriteBlogListView(request):
    params = {}
    mydata = CustomUser.objects.get(MO1_userNumber=request.user.MO1_userNumber)
    filter= MO10_Fav_Blog.objects.filter(MO1_userNumber=mydata)
    params["object_list"] = filter

    return render(request, "FavoriteBlogList.html", params)

# お気に入りユーザ一覧画面
@login_required
def FavoriteUserListView(request):
    params = {}
    mydata = CustomUser.objects.get(MO1_userNumber=request.user.MO1_userNumber)
    filter= MO9_Fav_Custom_user.objects.filter(MO1_userNumber=mydata)
    params["favUser_list"] = filter
    return render(request, "FavoriteUserList.html", params)


@login_required
def visitrecordcreate(request,mail):
    user = CustomUser.objects.get(MO1_userNumber=request.user.MO1_userNumber)
    store = MO2_store.objects.get(MO2_mailAdress=mail)
    d_spot = MO3_Default_spot.objects.get(MO2_storeNumber = store)
    record = MO6_Visit_record.objects.create(MO1_userNumber=user,MO3_DspotNumber=d_spot)
    user.MO1_point += 10
    user.save()
    MO11_Pointrecord.objects.create(MO1_userNumber=user,MO2_storeNumber=store,MO11_pointSize=10)
    return redirect("main:Mypage")

def Countact(request):
    params = {"message":""}
    if request.method== 'POST':
        subject = request.POST.get("subjectname")
        message = request.POST.get("subjectdetail")
        from_email = request.POST.get("email")
        recipient_list = ["admin@mail.com"]
        send_mail(subject, message, from_email, recipient_list)
        params["message"] = "Your inquiry has been received"
    return render(request,"ContactUs.html",params)