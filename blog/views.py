from django.shortcuts import render
from django.views import generic
# Create your views here.

class BlogListView(generic.View):
    template_name = "BlogList.html"

class BlogRegisterView(generic.View):
    template_name = "BlogRegister.html"

class BlogConfirmationView(generic.View):
    template_name = "BlogConfirmation.html"

class BlogCompletionView(generic.View):
    template_name = "BlogCompletion.html"

class BlogDetailView(generic.View):
    template_name = "BlogDetail.html"

class BlogEditView(generic.View):
    template_name = "BlogEdit.html"

class BlogDeleteView(generic.View):
    template_name = "BlogDelete.html"

class OpenRangeRegisterView(generic.View):
    template_name = "OpenRangeRegister.html"

class OtherBlogListView(generic.View):
    template_name = "OtherBlogList.html"

class FavoriteBlogListView(generic.View):
    template_name = "FavoriteBlogList.html"