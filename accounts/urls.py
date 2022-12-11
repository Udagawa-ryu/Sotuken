from django.urls import path
from . import views
app_name = 'accounts'
urlpatterns = [
    path('signup/',views.newAccount,name="signup"),
    path('login/',views.login,name="login"),
    path('logout/',views.logout,name="logout"),
    path('signupcompletion/',views.signupcomp,name="SingUpCompletion"),
    path('UserInfoCompletion/',views.UserInfoCompletion,name="UserInfoComp"),
    path('UserInfoEdit/',views.UserInfoEdit,name="UserInfoEdit"),
    path("UserInfoConfirmation/",views.UserInfoConfirmation,name="UserInfoConfirmation"),
    path('UserInfoRegister/',views.UserInfoRegister,name="UserInfoRegister"),
    path('DeleteAccount/',views.deleteAccount,name="DeleteAccount"),
    path('AccountDelete/',views.AccountDelete,name="AccountDelete"),
]