from django.urls import path
from . import views

app_name = 'main'
urlpatterns = [
    path('', views.MypageView.as_view(), name="Mypage"),
    path('point',views.PointView.as_view(), name="Point"),


    # path('',views.FavoriteView.as_view(), name="Favorite"),
    # path('',views.BlogView.as_view(), name="Blog"),
    # path('',views.MapView.as_view(), name="Map"),
    # path('',views.PublicScopeView.as_view(), name="PublicScope"),
    # path('',views.SearchView.as_view(), name="Search"),
]