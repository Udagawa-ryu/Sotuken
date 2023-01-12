from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.BlogListView.as_view(), name="blogList"),
    path('blogRegister', views.BlogRegister, name="blogRegister"),
    path('blogConfirmation', views.BlogConfirmation, name="blogConfirmation"),
    path('blogCompletion', views.BlogCompletionView.as_view(), name="blogCompletion"),
    # path('blogDetail', views.BlogDetailView.as_view(), name="blogDetail"),
    path('blogDetail/<int:pk>/', views.BlogDetailView.as_view(), name="blogDetail"),
    # path('blogEdit', views.BlogEditView.as_view(), name="blogEdit"),
    path('blogEdit/<int:pk>/', views.BlogEditView.as_view(), name="blogEdit"),
    # path('blogDelete', views.BlogDeleteView.as_view(), name="blogDelete"),
    path('blogDelete/<int:pk>/', views.BlogDeleteView.as_view(), name="blogDelete"),
    path('openRangeRegister', views.OpenRangeRegisterView.as_view(), name="openRangeRegister"),
    path('otherBlogList/<int:pk>/', views.OtherBlogListView.as_view(), name="otherBlogList"),
]