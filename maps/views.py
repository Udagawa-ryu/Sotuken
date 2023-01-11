from django.shortcuts import render
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
    form = OspotCreateForm()
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
        'form':form,
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
        }
        form = OspotCreateForm(request.POST or initial_data)
        if form.is_valid():
            form.save()
