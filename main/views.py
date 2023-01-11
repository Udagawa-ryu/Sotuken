from django.shortcuts import render,redirect
from django.views import generic
from blog.models import MO7_Blog,MO10_Fav_Blog,MO9_Fav_Custom_user
from accounts.models import CustomUser
from django.urls import reverse_lazy
from .forms import *
from django.contrib.auth.decorators import login_required

# Create your views here.

# マイページ画面
def MypageView(request):
    return render(request, 'Mypage.html')

# ポイント画面
# class PointView(generic.TemplateView):
def PointView(request):
    params = {}
    mydata = CustomUser.objects.get(MO1_userNumber=request.user.MO1_userNumber)
    params["object"] = mydata

    return render(request, "Point.html", params)

# 使用ポイント画面
def PointConfirmationView(request):
    mydata = CustomUser.objects.get(MO1_userNumber=request.user.MO1_userNumber)
    if request.method == 'POST':
        subpoint = request.POST.get("point")
        data = {"point": subpoint}
        form = PointForm(data)
        params = {"form": form, "mydata":mydata}
        if request.POST.get('next', '') == 'comfirm':
            return render(request, 'PointConfirmation.html', params)
        if request.POST.get('next', '') == 'back':
            return render(request, 'PointInput.html', params)
        if request.POST.get('next', '') == 'next':
            mypoint = mydata.MO1_point
            mydata.MO1_point = mypoint - int(subpoint)
            mydata.save()
            return render(request, "PointDisplay.html", params)


# 使用ポイント提示画面
def PointDisplayView(request):
    return render(request, "PointDisplay.html")

# 使用ポイント入力画面
def PointInputView(request):
    mydata = CustomUser.objects.get(MO1_userNumber=request.user.MO1_userNumber)
    # post
    if request.method== 'POST':
        subpoint = request.POST.get("point")
        data = {"point": subpoint}
        form = PointForm(data)
        params = {"form": form, "mydata":mydata}
        return render(request, "PointInput.html", params)
    # get
    else :
        form = PointForm()
        params = {"form": form, "mydata":mydata}
        return render(request, "PointInput.html", params)

# 店舗用QRコード読み取り画面
def StoreQRreadView(request):
    return render(request, "StoreQRread.html")

# 訪問記録用QRコード読み取り画面
def VisitQRreadView(request):
    return render(request, "VisitQRreadhtml")

# お気に入りブログ一覧画面
def FavoriteBlogListView(request):
    params = {}
    mydata = CustomUser.objects.get(MO1_userNumber=request.user.MO1_userNumber)
    filter= MO10_Fav_Blog.objects.filter(MO1_userNumber=mydata)
    params["object_list"] = filter

    return render(request, "FavoriteBlogList.html", params)

# お気に入りユーザ一覧画面
def FavoriteUserListView(request):
    params = {}
    mydata = CustomUser.objects.get(MO1_userNumber=request.user.MO1_userNumber)
    filter= MO9_Fav_Custom_user.objects.filter(MO1_userNumber=mydata)
    params["favUser_list"] = filter
    return render(request, "FavoriteUserList.html", params)


@login_required
def visitrecordcreate(request,pk):
    user = CustomUser.objects.get(MO1_userNumber=request.user.MO1_userNumber)
    d_spot = MO3_Default_spot.objects.get(MO2_storeNumber = pk)
    record = MO6_Visit_record(MO1_userNumber=user,MO3_Default_spot=d_spot)
    record.save()
    return redirect("main:Mypage")
