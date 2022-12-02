from django.shortcuts import render
from django.views import generic
from blog.models import *
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
    model = MO10_Fav_blog


# お気に入りユーザ一覧画面
class FavoriteUserListView(generic.TemplateView):
    template_name = "FavoriteUserList.html"