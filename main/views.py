from django.shortcuts import render
from django.views import generic
# Create your views here.

class MypageView(generic.TemplateView):
    template_name= "Mypage.html"
class PointView(generic.TemplateView):
    template_name = "Point.html"




# class FavoriteView(generic.TemplateView):
#     template_name = "Favorite.html"


# class BlogView(generic.TemplateView):
#     template_name = "Blog.html"

# class MapView(generic.TemplateView):
#     template_name = "Map.html"

# class PublicScopeView(generic.TemplateView):
#     template_name = "Point.html"

# class SearchView(generic.TemplateView):
#     template_name = "Point.html"