from django.urls import path
from . import views

app_name = 'main'
urlpatterns = [
    path('', views.MypageView.as_view(), name="Mypage"),
    path('point',views.PointView.as_view(), name="Point"),
    path('PointConfirmation',views.PointConfirmationView.as_view(), name="Favorite"),
    path('PointDisplay',views.PointDisplayView.as_view(), name="Blog"),
    path('PointInput',views.PointInputView.as_view(), name="Map"),
    path('StoreQRread',views.StoreQRreadView.as_view(), name="PublicScope"),
    path('VisitQRread',views.VisitQRreadView.as_view(), name="Search"),
]