from django.urls import path
from . import views
app_name = 'accounts'
urlpatterns = [
    path('signup/',views.newAccount,name="signup"),
    path('login/',views.login,name="login"),
    # path('logout/',views.name="logout"),
    path('UserInfoRegister/',views.UserInfoRegister,name="UserInfoRegister")
]