from django.shortcuts import render,redirect
from django.views import generic
from blog.models import MO10_Fav_Blog
from accounts.models import CustomUser,MO6_Visit_record
from maps.models import MO3_Default_spot,MO4_Original_spot
from django.contrib.auth.decorators import login_required
# Create your views here.

# マイページ画面
class MypageView(generic.TemplateView):
    template_name= "Mypage.html"

# ポイント画面
class PointView(generic.TemplateView):
    template_name = "Point.html"

# 使用ポイント画面
class PointConfirmationView(generic.TemplateView):
    template_name = "PointConfirmation.html"

# 使用ポイント提示画面
class PointDisplayView(generic.TemplateView):
    template_name = "PointDisplay.html"

# 使用ポイント入力画面
class PointInputView(generic.TemplateView):
    template_name = "PointInput.html"

# 店舗用QRコード読み取り画面
class StoreQRreadView(generic.TemplateView):
    template_name = "StoreQRread.html"

# 訪問記録用QRコード読み取り画面
class VisitQRreadView(generic.TemplateView):
    template_name = "VisitQRreadhtml"

# お気に入りブログ一覧画面
class FavoriteBlogListView(generic.TemplateView):
    template_name = "FavoriteBlogList.html"
    model = MO10_Fav_Blog


# お気に入りユーザ一覧画面
class FavoriteUserListView(generic.TemplateView):
    template_name = "FavoriteUserList.html"

@login_required
def visitrecordcreate(request,pk):
    user = CustomUser.objects.get(MO1_userNumber=request.user.MO1_userNumber)
    d_spot = MO3_Default_spot.objects.get(MO2_storeNumber = pk)
    record = MO6_Visit_record(MO1_userNumber=user,MO3_Default_spot=d_spot)
    record.save()
    return redirect("main:Mypage")
