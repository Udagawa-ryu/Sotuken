from django.urls import path
from . import views

app_name = 'maps'
urlpatterns = [
    path('', views.IndexView.as_view(), name="Map"),
    path('OspotInfo/', views.OspotInfoView.as_view(), name="OspotInfo"),
    path('OspotInfo/', views.OspotVisitRegisterView.as_view(), name="OspotVisitRegister"),
    path('OspotInfo/', views.DspotInfoView.as_view(), name="DspotInfo"),
    path('OspotInfo/', views.OtherMapView.as_view(), name="OtherMap"),
]