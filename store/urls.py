from django.urls import path
from . import views

app_name = 'store'
urlpatterns = [
    path('', views.IndexView.as_view(), name="StoreMypage"),
    path('storeRequest/',views.storeRequest,name="storeRequest"),
    path('storeCertification/',views.storeCertification,name="storeCertification"),
    path('addStore/',views.addStore,name="addStore"),
    path('storePassRegister/<str:store>/',views.StorePassRegister,name="storePassRegister"),
    path('storeLogin/',views.storeLogin,name="storeLogin"),
]