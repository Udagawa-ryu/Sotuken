from django.urls import path
from . import views

app_name = 'store'
urlpatterns = [
    # path('', views.IndexView.as_view(), name="StoreMypage"),
    path('', views.IndexView, name="StoreMypage"),
    path('storeRequest/',views.storeRequest,name="storeRequest"),
    path('storeCertification/',views.storeCertification,name="storeCertification"),
    path('addStore/',views.addStore,name="addStore"),
    path('storePassRegister/<str:store>/',views.StorePassRegister,name="storePassRegister"),
    path('storeLogin/',views.storeLogin,name="storeLogin"),
    path('storeInfoEdit',views.storeInfoEditView,name="storeInfoEdit"),
    path('storeInfoConfirmation/',views.storeInfoConfirmationView,name="storeInfoConfirmation"),
    path('storeinfocompletion/',views.storeinfocompletionView.as_view(),name="storeinfocomp"),
    path('storeLogout/',views.storeLogoutView.as_view(),name="storeLogout"),
    path('storeInfoDeleteConfirmation/',views.storeinfodeleteconfView,name="storeinfodeleteconf"),
    path('storeQR/',views.storeQRView,name="storeQR"),
    path('storeLogoutCheck/',views.storeLogout,name="storeLogoutCheck"),
    path('storeInfoDelete/',views.storeinfodelete,name="StoreInfoDelete"),
    path('statistics/',views.statistics,name="Statictics"),
    # path('kari/',views.plt_leq,name="kari"),
]