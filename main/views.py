from django.shortcuts import render
from django.views import generic
# Create your views here.

class MypageView(generic.TemplateView):
    template_name= "Mypage.html"
class PointView(generic.TemplateView):
    template_name = "Point.html"

class PointConfirmationView(generic.TemplateView):
    template_name = "PointConfirmation.html"


class PointDisplayView(generic.TemplateView):
    template_name = "PointDisplay.html"

class PointInputView(generic.TemplateView):
    template_name = "PointInput.html"

class StoreQRreadView(generic.TemplateView):
    template_name = "StoreQRread.html"

class VisitQRreadView(generic.TemplateView):
    template_name = "VisitQRreadhtml"