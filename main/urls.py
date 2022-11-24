from django.urls import path
from . import views

app_name = 'main'
urlpatterns = [
    path('', views.MypageView.as_view(), name="Mypage"),
]