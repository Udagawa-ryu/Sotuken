from django.urls import path
from . import views

app_name = 'main'
urlpatterns = [
    path('', views.MypageView, name="Mypage"),
    path('Point/',views.PointView, name="Point"),
    path('PointConfirmation/',views.PointConfirmationView, name="PointConfirmation"),
    path('PointDisplay/',views.PointDisplayView, name="PointDisplay"),
    # path('PointInput/',views.PointInputView, name="PointInput"),
    path('PointInput/<str:mail>/<str:date>/',views.PointInputView, name="PointInput"),
    path('StoreQRread/',views.StoreQRreadView, name="StoreQRread"),
    path('VisitQRread/',views.VisitQRreadView, name="VisitQRread"),
    path('favoriteBlogList/', views.FavoriteBlogListView, name="favoriteBlogList"),
    path('favoriteUserList/', views.FavoriteUserListView, name="favoriteUserList"),
    path('visitrecord/<str:mail>/<str:date>/',views.visitrecordcreate,name="visitrecord"),
    path('Countact/',views.Countact,name="countact"),
]