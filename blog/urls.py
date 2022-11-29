from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('blogList', views.BlogListView.as_view(), name="blogList"),
    path('blogRegister', views.BlogRegisterView.as_view(), name="blogRegister"),
    path('blogConfirmation', views.BlogConfirmationView.as_view(), name="blogConfirmation"),
    path('blogCompletion', views.BlogCompletionView.as_view(), name="blogCompletion"),
    path('blogDetail', views.BlogDetailView.as_view(), name="blogDetail"),
    path('blogEdit', views.BlogEditView.as_view(), name="blogEdit"),
    path('blogDelete', views.BlogDeleteView.as_view(), name="blogDelete"),
    path('openRangeRegister', views.OpenRangeRegisterView.as_view(), name="openRangeRegister"),
    path('otherBlogList', views.OtherBlogListView.as_view(), name="otherBlogList"),
    path('favoriteBlogList', views.FavoriteBlogListView.as_view(), name="favoriteBlogList"),
]