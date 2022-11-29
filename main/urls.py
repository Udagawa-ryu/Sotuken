from django.urls import path
from . import views

app_name = 'main'
urlpatterns = [
    path('', views.MypageView.as_view(), name="Mypage"),
    path('Point/',views.PointView.as_view(), name="Point"),
    path('PointConfirmation/',views.PointConfirmationView.as_view(), name="PointConfirmation"),
    path('PointDisplay/',views.PointDisplayView.as_view(), name="PointDisplay"),
    path('PointInput/',views.PointInputView.as_view(), name="PointInput"),
    path('StoreQRread/',views.StoreQRreadView.as_view(), name="StoreQRread"),
    path('VisitQRread/',views.VisitQRreadView.as_view(), name="VisitQRread"),
]