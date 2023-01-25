from django.shortcuts import render,redirect
from django.views import generic
from blog.models import MO7_Blog,MO10_Fav_Blog,MO9_Fav_Custom_user
from maps.models import MO3_Default_spot
from accounts.models import CustomUser,MO6_Visit_record
from django.urls import reverse_lazy
from .forms import *
from django.contrib.auth.decorators import login_required

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
    params["object"] = mydata

    return render(request, "Point.html", params)

# 使用ポイント画面
@login_required
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
@login_required

def PointDisplayView(request):
    return render(request, "PointDisplay.html")

# 使用ポイント入力画面
@login_required
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
def visitrecordcreate(request,pk):
    user = CustomUser.objects.get(MO1_userNumber=request.user.MO1_userNumber)
    d_spot = MO3_Default_spot.objects.get(MO2_storeNumber = pk)
    record = MO6_Visit_record.objects.create(MO1_userNumber=user,MO3_DspotNumber=d_spot)
    user.MO1_point += 10
    user.save()
    return redirect("main:Mypage")
