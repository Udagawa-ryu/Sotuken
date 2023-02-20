from django.urls import path
from . import views

app_name = 'maps'
urlpatterns = [
    # path('', views.MapView.as_view(), name="Map"),
    path('',views.Map,name="Map"),
    path('OspotVisitRegister/', views.OspotVisitRegister, name="OspotVisitRegister"),
    path('OspotVisitCreate/', views.OspotVisitcreate, name="OspotVisitCreate"),
    path('DspotInfo/<int:spot_num>/', views.DspotInfo, name="defalutspotinfo"),
    path('OspotInfo/<int:spot_num>/', views.OspotInfo, name="originalspotinfo"),
    path('usersmap/<int:num>',views.OtherMap,name="OtherMap"),
    path('SpotSearch/',views.SpotSearch,name="SpotSearch"),
    path('OpotCreate/',views.OspotCreate,name="OspotCreate"),
]