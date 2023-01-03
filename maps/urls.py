from django.urls import path
from . import views

app_name = 'maps'
urlpatterns = [
    # path('', views.MapView.as_view(), name="Map"),
    path('',views.Map,name="Map"),
    path('OspotInfo/', views.OspotInfoView.as_view(), name="OspotInfo"),
    path('OspotVisitRegister/', views.OspotVisitRegisterView.as_view(), name="OspotVisitRegister"),
    path('DspotInfo/', views.DspotInfoView.as_view(), name="DspotInfo"),
    path('OspotInfo/', views.OtherMapView.as_view(), name="OtherMap"),
]