from django.shortcuts import render,redirect
from django.views import generic
from accounts.models import CustomUser,MO6_Visit_record
from .models import MO3_Default_spot,MO4_Original_spot,MO5_Tag
from .forms import *
import json
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def Map(request):
    user = CustomUser.objects.get(MO1_userNumber=request.user.MO1_userNumber)
    o_spotform = OspotCreateForm()
    searchform = SpotSearchForm()
    tag_list = MO5_Tag.objects.all()
    d_spot = MO3_Default_spot.objects.all()
    o_spot = MO4_Original_spot.objects.filter(MO1_userNumber = request.user.MO1_userNumber)
    d_list = []
    o_list = []
    for i in d_spot:
        d_list.append([i.MO2_storeNumber.MO2_address,i.MO2_storeNumber.MO2_storeName])
    for i in o_spot:
        o_list.append([i.MO4_OspotAdress,i.MO4_OspotName])
    params = {
        'd_list': json.dumps(d_list),
        'o_list': json.dumps(o_list),
        'o_form':o_spotform,
        's_form':searchform,
        'tag_list':tag_list,
        'user':user,
    }
    return render(request,"Map.html",params)


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

@login_required
def OspotCreate(request):
    if request.method == 'POST':
        initial_data = {
            "MO1_userNumber":request.POST.get("MO1_userNumber"),
            "MO4_OspotName":request.POST.get("MO4_OspotName"),
            "MO4_OspotAdress":request.POST.get("MO4_OspotAdress"),
            "MO4_OspotInfo":request.POST.get("MO4_OspotInfo")
        }
        form = OspotCreateForm(request.POST or initial_data)
        if form.is_valid():
            # form.save()
            return redirect("maps:Map")
    return redirect("maps:Map")

@login_required
def SpotSearch(request):
    if request.method == 'POST':
        tags_id = request.POST.getlist('tags')
        keword = request.POST.get('keyword')
    for i in tags_id:
        print("tag=",i)
    print("keyword=",keword)
    return Map(request)
