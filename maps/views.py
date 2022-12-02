from django.shortcuts import render
from django.views import generic
# Create your views here.

class MapView(generic.TemplateView):
    template_name= "Map.html"

class OspotInfoView(generic.TemplateView):
    template_name= "OspotInfo.html"

class OspotVisitRegisterView(generic.TemplateView):
    template_name = "OspotVisitRegister.html"

class DspotInfoView(generic.TemplateView):
    template_name: str = "DspotInfo.html"

class OtherMapView(generic.TemplateView):
    template_name: str = "OtherMap.html"
